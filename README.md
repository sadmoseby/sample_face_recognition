# Simple Face Recognition

## Prerequisites

Please make sure that the following are installed on your system
* Git, with a valid github account
* Docker, with a valid dockerhub account
* python

## Usage Directions

The code in this repository allows you to 
1. Train models for face recognition based on the provided dataset.
1. Use the trained docker image to recognize faces in real time

The steps to accomplish this are outlined below -

* Clone this git repository into your local workspace

* Download the docker image containing the code and ML models <br/>
    *docker pull mosebyhub/simple_face_recognition:latest*
    
### For Training

* In the _datasets/_ folder, create a folder(**images**) containing your annotated images. 
  This dataset should contain all the faces that need to be recognized.
  For annotation, a tool like _labelImg_, available here - 
  https://github.com/tzutalin/labelImg is recommended.
  The format of the annotation needs to be **exactly** similar to what is present in the _datasets/examples/_ directory
  
* Change the json parameters in the _train_run_params.json_ 
    * Under *"datasets"*, **change the foldername** to the one containing your training images (*images*).
    * Change the debugging level if needed. (logs are dumped into the *run_data* folder)
    * Cache intermediate results of processing so that further experiments can be run using different parameters 
    etcetera. Please look at the **sample_train_run_params.json** for details. (**only if needed**)
    * **Do not** change the experiment type. Only experiment_2 is supported for now.

* Run the run_docker.py command from python with the following parameters -
    *  *--mode="train"*    ## This tells the container to train the model
    *  *--source_docker_image=""* ## This is the docker image downloaded from dockerhub
    *  *--dest_docker_image=""*  ## This is the destination docker image that will be used for serving.
    *  *--run_params="$(pwd)"/train_run_params.json*  ## This is the configuration file that will be used for training
  
  Additional arguments (_datasets_, _run_data_) need to be given to run_docker.py if it is executed outside of this repo.
  This step will end up creating the _dest_docker_image_ image that will be used to serve the model.


###  For Serving (Real Time Detection) 

* Change the json parameters in the _serve_run_params.json_ (**only if needed**) to 
    * Change the debugging level
    * Change the _server-mode_ :- By default, the container runs in **local_server** mode. **This is the only mode available for now **
    * Under *"serve_details"*, if needed, change the port that you want the local server to run on.
    
* Run the run_docker.py command from python with the following parameters -
    *  *--mode="serve"*    ## This tells the container to serve the model
    *  *--source_docker_image="dest_docker_image"* ## This is the docker image that was created AFTER the training phase.
    *  *--run_params="$(pwd)"/serve_run_params.json*  ## This is the configuration file that will be used for serving the model <br/>
    This will start running the container as a background server process for all clients.
    
###  For Testing (Real Time Detection)

#### Web-Cam Client 
   This assumes that you are testing on a device with a webcam that the python cv2 library has access to. 
   Tested on a Macbook Pro.
   * Run python examples/webcam_client.py

## Attribution

This project was possible because of several software and pre-trained ML models available in the public domain. 

Specifically, this project uses a pre-trained Keras FaceNet model provided by Hiroki Taniai (https://github.com/nyoki-mtl) available here :-
https://drive.google.com/drive/folders/1pwQ3H4aJ8a6yyJHZkTwtjcL4wYWQb7bn

This project also uses a pre-trained MTCNN model that is available at https://github.com/ipazc/mtcnn


