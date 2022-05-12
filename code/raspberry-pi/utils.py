import os
import boto3
from botocore.exceptions import NoCredentialsError
import base64
import json
import requests
import time

##AWS credentials
AWSAccessKeyId = 'AKIAUHKO4UFWYORI5MXO'
AWSSecretKey = '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'

api = 'https://5pp7zbuxs7mvmbtxp27hz4bhyi0bltqe.lambda-url.us-east-1.on.aws/'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

s3_client = boto3.client('s3', aws_access_key_id=AWSAccessKeyId, aws_secret_access_key=AWSSecretKey)
s3_bucket_name = 'cc-p2-recordings'

def createDirectoryIfNotExists(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def upload_files_to_S3(file_path, fileName):
	#print("Sending to s3 " + file_path)
	try:
		s3_client.upload_file(file_path, s3_bucket_name, fileName)
		#print("Uploaded to S3 Successfully")
	except FileNotFoundError:
		print('File was not found')
	except NoCredentialsError:
		print('Credentials are not available')

def post_call(path, image_no):
	st = time.time() 
	with open(path, "rb") as f:
		im_bytes = f.read()
	im_b64 = base64.b64encode(im_bytes).decode("utf8")
	payload = json.dumps({"image": im_b64})
	response = requests.post(api, data=payload, headers=headers)
	try:
		data = response.json()
		if response.status_code != 200:
		    print(f"Not able to fetch predictions at the moment: {data}")
		else:            
			en = time.time()
			academic_info = data["body"]["Items"][0]
			print(f'The {image_no} person recognized: \"{str(academic_info["Name"])}\", \"{str(academic_info["Major"])}\", \"{str(academic_info["Year"])}\"' )
			print(f"Latency: {en - st} seconds")
	except requests.exceptions.RequestException:
		print(response.text)
