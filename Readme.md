# CSE 546 Project 2 - Real time Distributed Face Recognition system

## Group Members
* Tapan Rajnikant Modi (ASU ID : 1222325026)
* Onkar Pandit (ASU ID: 1222405119)
* Shreemad Sanskarbhai Patel (ASU ID : 1222713687)

## How to run the code
* There are 4 folders in the “code” folder - 1) dynamodb-lambda 2) evaluation-lambda 3) web-tier-lambda 4) raspberry-pi. 
* We have used the SAM CLI provided by AWS to build and deploy the evaluation lambda function. Its codebase includes a samconfig.toml that has all the deployment configs. The docker image for the function can be built using "sam build" command. Before deploying the face-recognition lambda function, we need to train the model first to get a checkpoint file which will be used while testing. To train the model, we can just run "python3 train_face_recognition.py" command. To deploy the docker image to AWS ECR we use the command "sam deploy –guided" which helps deploy the image step by step.
* Since the web tier lambda function and the dynamo db lambda functions are relatively very small and consist of only one file, they can easily be developed, maintained, and deployed directly on the code CLI provided by lambda. We have included the yml file of the web tier and the dynamo db lambda function in the code submission.
* To run the code in Raspberry Pi, first, make sure that python 3.7 is installed and the terminal is currently in the raspberry-pi folder. Then we need to execute the following commands to successfully run the code. 
    ```commandline
    python3 -m venv project-venv
    source project-venv/bin/activate
    pip install requests boto3 picamera
    python main.py 
    ```