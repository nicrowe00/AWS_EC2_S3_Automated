#imports the boto3 Python SDK for AWS.
import boto3

#imports the subprocess command which is used to run commands via the local terminal.
import subprocess

#imports the webbrowser command to open new tabs in the local web broswer
import webbrowser

#imports the time command
import time 

import os

#Creates the required objects.
ec2 = boto3.resource('ec2')
ec2client = boto3.client('ec2')
s3 = boto3.resource("s3")
s31 = boto3.client('s3')
#Creates the instance object

try:
    new_keypair = ec2.create_key_pair(KeyName='InstanceKey')
    with open('./InstanceKey.pem', 'w') as file:
        file.write(new_keypair.key_material)
        
except Exception as error:
    print(error)

subprocess.run("chmod 400 InstanceKey.pem", shell=True)

print ('Please wait while the instance is created')
#Creates the instance with all the desired settings
instances = ec2.create_instances(
 ImageId = 'ami-05cd35b907b4ffe77',
 MinCount=1,
 MaxCount=1,
 InstanceType='t2.nano',
 SecurityGroupIds=["sg-045cbb1164d73d9c4"],
 KeyName='InstanceKey',
 UserData = '''#!/bin/bash
 sudo apt-get update
 sudo yum install httpd -y
 sudo yum systemctl enable httpd
 sudo systemctl start httpd
 sudo chmod 777 /var/www/html
 echo '<html>' > index.html
 echo 'Private IP address: ' >> index.html
 curl http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html
 echo ' Availability Zone: ' >> index.html
 curl http://169.254.169.254/latest/meta-data/placement/availability-zone >>  index.html
cp index.html /var/www/html/index.html
'''
)

instance = ec2.Instance(instances[0].id)

#Adds tags to the created instance
name_tag = {'Key': 'Assignment', 'Value': 'My Assignment'}
instance.create_tags(Tags=[name_tag])


#Stops the script from continuing until the created instance is running
instance.wait_until_running()

#Reloads the created instance
instance.reload()

#Prints the id of the created instance
print ('This is the id of your instance: ')
print (instances[0].id)
time.sleep( 5 )

#Prints the public IPv4 address of the created instance
print ('This is the public ip address of your instance: ')
print(instance.public_ip_address)
time.sleep( 5 )

print('Please wait while the web server is configured.')

waiter = ec2client.get_waiter('instance_status_ok')
waiter.wait(InstanceIds=[instances[0].instance_id])
time.sleep(5) 

#Opens the web server in the local web browser
webbrowser.open_new_tab(instance.public_ip_address)

#Lets the user input their desired bucket name
print ('The program will continue in 30 seconds')
time.sleep( 30 )
bucket_name = input('Enter your desired bucket name (be aware some names might be in use by other users, you are advised to name your bucket something similiar to: name-0000): ')

#Creates the bucket with the user's desired bucket name 
try:
    response = s3.create_bucket(Bucket=bucket_name,
CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
    print (response)
except Exception as error:
    print (error)

#Downloads the WIT logo image file
URL = "http://devops.witdemo.net/assign1.jpg"
try: 
    download = subprocess.run(["curl",URL,"-o","wit1.jpg"])
    download
except Exception as error:
    print (error)    


#Sets the S3 bucket static web host configuration
website_configuration = {
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
}
s31.put_bucket_website(Bucket=bucket_name, WebsiteConfiguration=website_configuration)                     

#Uploads the supplied index file to the bucket and sets it to public
websitefile = "index.html"
try:
    response = s3.Object(bucket_name, websitefile).put(Body=open(websitefile, 'rb'), ACL = 'public-read', ContentType = "text/html")
    print(response)
except Exception as error:
    print (error)
    
#Uploads the Wit logo image file to the bucket and sets it to public
filename = "wit1.jpg"
try:
    response = s3.Object(bucket_name, filename).put(Body=open(filename, 'rb'), ACL = 'public-read', ContentType = 'image/jpeg')
    print(response)
except Exception as error:
    print (error)
    
#Opens the bucket website endpoint in the local web browser    
bucket_url = 'http://{}.s3-website-eu-west-1.amazonaws.com'.format(bucket_name)
webbrowser.open_new_tab(bucket_url)

