import os
import boto3
from boto3.session import Session
from datetime import datetime

session = Session(
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy',
    region_name='us-east-1'
)

if os.getenv('LOCALSTACK_HOSTNAME') is None:
    endpoint = 'http://localhost:4566'
else:
    endpoint=f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566"

s3 = session.resource(
    service_name='s3', 
    endpoint_url=endpoint
)

def lambda_handler(event, context):

    bucket = 'test-bucket'    # バケット名を指定
    key = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.txt'
    file_contents = 'Lambda Save File'

    s3.Bucket(bucket).put_object(Key=key, Body=file_contents)

    return 'create file'+ key
