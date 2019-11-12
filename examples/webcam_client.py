import cv2
import socket
import struct
import pickle
import argparse


def create_parser():
    parser = argparse.ArgumentParser(description='Process some webcam paramters')
    parser.add_argument('--port', type=int, default=48041, help='port to connect to')
    parser.add_argument('--host', default='', help='ip to connect to')
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((args.host, args.port))
    connection = client_socket.makefile('wb')

    cam = cv2.VideoCapture(0)
    cam.set(3, 320)
    cam.set(4, 240)

    img_counter = 0
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    payload_size = struct.calcsize(">L")
    recv_data = b""
    while True:
        # read data from the cam
        ret, frame = cam.read()

        # prepare data for transmission
        result, frame1 = cv2.imencode('.jpg', frame, encode_param)
        # data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame1, 0)
        size = len(data)

        # send data
        client_socket.sendall(struct.pack(">L", size) + data)

        #get data from the server
        while len(recv_data) < payload_size:
            print("Recv: {}".format(len(recv_data)))
            recv_data += client_socket.recv(4096)

        print("Done Recv: {}".format(len(recv_data)))
        packed_msg_size = recv_data[:payload_size]
        recv_data = recv_data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))
        while len(recv_data) < msg_size:
            recv_data += client_socket.recv(4096)
        actual_data = pickle.loads(recv_data[:msg_size], fix_imports=True, encoding="bytes")

        for d in actual_data:
            cv2.rectangle(frame,
                          (d["boundary"]["x_min"], d["boundary"]["y_min"]),
                          (d["boundary"]["x_max"], d["boundary"]["y_max"]),
                          (0, 255, 0),
                          2)
            cv2.putText(frame, d["label"],
                        (d["boundary"]["x_min"] + 10, d["boundary"]["y_min"] + 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=4,
                        color=(0, 255, 0))

        # print the data obtained
        cv2.imshow('ImageWindow', frame)
        cv2.waitKey(1)
        recv_data = recv_data[msg_size:]

    cam.release()
