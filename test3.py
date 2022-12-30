import os
import boto3

s3_endpoint = 'http://%s:4566' % os.environ['LOCALSTACK_HOSTNAME']
s3_client = boto3.client('s3',endpoint_url=s3_endpoint,aws_access_key_id='dummy', aws_secret_access_key='dummy')

def handler(event, context):
    test_object_key = 'a-object'
    more_binary_data = b'some body'
    s3_client.create_bucket(Bucket='a-bucket')
    s3_client.put_object(
        Bucket='a-bucket',
        Key=test_object_key,
        Body=more_binary_data
    )
    return {
        "message": "{0} placed into S3".format(test_object_key)
    }
    