import argparse
from subprocess import Popen, PIPE
import json
import time
import os

def execute_shell_command(cmd=None, max_time=None, debug_=False):
    retcode = 0
    sleep_interval = 60
    if debug_:
        print("Executing shell command:- {}".format(str(cmd)))
    if not cmd:
        return retcode
    try:
        time_ = 0.0
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        if max_time:
            time.sleep(5)
            while p.poll() is None and time_ < max_time:
                time.sleep(sleep_interval)
                time_ += sleep_interval
            if time_ < max_time:
                retcode = p.returncode
                if retcode:
                    print("Error {} when executing - {}".format(str(retcode), str(cmd)))
            else:
                retcode = -1
                print(cmd + "{}: command timed out !!".format(str(cmd)))
                p.kill()
    except Exception as e:
        print("{}: command failed for unknown reason {}".format(str(cmd), str(e)))
        retcode = -1
    return retcode


def create_parser():
    parser = argparse.ArgumentParser(description="Run training or serving docker containers")
    parser.add_argument("--mode",
                        default="train",
                        choices=['train', 'serve'],
                        help="Mode for docker to run in: train or serve",
                        required=True)
    parser.add_argument('--source_docker_image', help="name of base docker image", required=True)
    parser.add_argument('--dest_docker_image', help="name of destination docker image")
    parser.add_argument('--datasets', help="name of the directory where the dataset resides")
    parser.add_argument('--run_data', help="name of the directory where runtime data created by the container is stored")
    parser.add_argument("--run_params_path", help="Full path location of the run_params_file")
    parser.add_argument("--gpu", type=bool, default=False, help="use Gpu for processing")
    parser.add_argument("--debug", type=bool, default=False, help="print debugs") 
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    shell_cmd = ""
    if args.mode == "train":
        container_name = "face_train_" + str(int(time.time()))
        shell_cmd = "docker run " 
        if not args.dest_docker_image:
            shell_cmd += " --rm "
        if args.gpu:
            shell_cmd += " --gpus all "
        shell_cmd += " -e mode='train'"
        if not args.run_data:
            if not os.path.exists("./run_data"):
                os.makedirs("./run_data", exist_ok=True)
            args.run_data = "\"$(pwd)\"/run_data"
        shell_cmd += " --mount type=bind,source={},destination=/app/run_data".format(str(args.run_data))

        if not args.datasets:
            if not os.path.exists("./datasets"):
                print("Didn't find dataset directory. Terminating prematurely !!")
                exit(1)
            args.datasets = "\"$(pwd)\"/datasets"
        shell_cmd += " --mount type=bind,source={},destination=/app/datasets".format(str(args.datasets))

        if args.run_params_path:
            shell_cmd += " --mount type=bind,source={},destination=/app/run_params.json ".format(str(args.run_params_path))
        shell_cmd += " --name " + container_name + " " + args.source_docker_image

        retcode = execute_shell_command(shell_cmd, max_time=3600, debug_=args.debug)
        if retcode != 0:
            print("Shell command execution failed! Terminating prematurely !!")
            exit(1)

        if args.dest_docker_image:
            shell_cmd = "docker commit " + container_name + " " + args.dest_docker_image
            execute_shell_command(shell_cmd, max_time=60, debug_=args.debug)

    elif args.mode == "serve":
        container_name = "face_test_" + str(int(time.time()))
        shell_cmd = "docker run -d --rm " 
        shell_cmd += " -e mode='serve'"
        if args.gpu:
            shell_cmd += " --gpus all " 
        if not args.run_data:
            if not os.path.exists("./run_data"):
                os.makedirs("./run_data", exist_ok=True)
            args.run_data = "\"$(pwd)\"/run_data"
        shell_cmd += " --mount type=bind,source={},destination=/app/run_data".format(str(args.run_data))
        if args.run_params_path:
            shell_cmd += " --mount type=bind,source={},destination=/app/run_params.json".format(str(args.run_params_path))
            run_params_path = args.run_params_path
        else:
            run_params_path = "./serve_run_params.json"

        with open(run_params_path, "r") as f:
            temp = json.loads(f.read())
            if "server_mode" in temp and temp["server_mode"] == "local_server":
                port = temp["serve_details"]["port"]
                shell_cmd += " -p {}:{}".format(str(port), str(port))

        shell_cmd += " --name " + container_name + " " + args.source_docker_image
        retcode = execute_shell_command(shell_cmd, debug_=args.debug)
        if retcode != 0:
            print("Shell command execution failed! Terminating prematurely !!")
            exit(1)
