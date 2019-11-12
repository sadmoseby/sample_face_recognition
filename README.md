# Simple Face Recognition

## Usage Directions

The code in this repository allows you to build a docker image that can be
1. Trained with faces from a training set and
1. Used to serve the trained model to recognize faces in the wild.

The steps to accomplish this are outlined below -

* Clone this git repository into your local workspace

* In the main repository, where your docker file exists, do a docker build :-
    **docker build -t <source_docker_image_name> .**
    
### For Training

* In the _datasets/_ folder, create another folder contaning your annotated images. 
  This dataset should contain all the faces that the serving model needs to recognize.
  For annotation, a tool like _labelImg_, available here - 
  https://github.com/tzutalin/labelImg is recommended.
  The format of the annotation needs to be **exactly** similar to what is present in the _datasets/examples/_ directory
  
* Change the json parameters in the _train_run_params.json_ (**only if needed**) to 
    * Change the ML models used in the backend and their parameters.
    * Change the debugging level
    * Cache intermediate results of processing so that further experiments can be run using different parameters 
    etcetera

* Run the run_docker.py command from python with the following parameters -
    *  *--mode="train"*    ## This tells the container to train the model
    *  *--source_docker_image=""* ## This is the docker image built earlier
    *  *--dest_docker_image=""*  ## This is the destination docker image that will be used for training
    *  *--run_params="$(pwd)"/train_run_params.json*  ## This is the configuration file that will be used for training
  Additional arguments (_datasets_, _run_data_) need to be given if the run_docker.py is executed outside of this repo.
  This will end up creating the _dest_docker_image_ image that will be used to serve the model.


###  For Serving  

* Change the json parameters in the _serve_run_params.json_ (**only if needed**) to 
    * Change the debugging level
    * Change the _server-mode_ :- By default, the container runs in **local_server** mode.
    It listens on a configurable port for frames that are sent to it via AF_INET sockets.
    
* Run the run_docker.py command from python with the following parameters -
    *  *--mode="serve"*    ## This tells the container to serve the model
    *  *--source_docker_image="dest_docker_image"* ## This is the docker image that was created AFTER the training phase.
    *  *--run_params="$(pwd)"/serve_run_params.json*  ## This is the configuration file that will be used for serving the model.

## Attribution

This project was possible because of several software and pre-trained ML models available in the public domain. 

Specifically, this project uses a pre-trained Keras FaceNet model provided by Hiroki Taniai (https://github.com/nyoki-mtl) available here :-
https://drive.google.com/drive/folders/1pwQ3H4aJ8a6yyJHZkTwtjcL4wYWQb7bn

This project also uses a pre-trained MTCNN model that is available at https://github.com/ipazc/mtcnn


