import boto3

def main() :
    client = boto3.client('s3', aws_access_key_id='dummy', aws_secret_access_key='dummy', region_name='us-east-1', endpoint_url='http://localhost:4566')
    response = client.list_buckets()
    client.upload_file('./test2.txt','test-bucket', 'test2.txt')
    print('upload complate')
    
if __name__ == "__main__": 
    main() 
