# AWS_EC2_S3_Automated

# Description
This programme is a Python3 script that utilizes Boto3 to automate the process of creating an AWS EC2 instance with an Apache web server installed on it and a S3 bucket configured for static web hosting. This script is designed for use in a Linux based operating system. This script only requires one other file to run successfully; the pre-built index.html page included in this repository. Upon completetion, the script will have launched the Apache web sebver, which will be set to display the instance's metadata, and the S3 static website, which will have uploaded the pre-built index.html page along with an image of the Waterford Institute of Technology logo that the script will have downloaded, which will display the Waterford Institute of Technology logo. The instance key pair will automatically be created and downloaded and the other instance settings such as the security group will be automatically be configured. The only input needed from the user is when they are asked to enter a name for the S3 bucket.

# How To Use
Python3 must be downloaded and installed on the user's Linux machine in orfer to run this programme. The pre-built index.html file must be in the same directory as the main script. In the Linux terminal, navigate to the directory containing the script and simply enter 'Python3 AWS_EC2_S3_Automated.py' and the program will run successfully.

# Author
Niall Crowe
ncrowe2000@gmail.com
