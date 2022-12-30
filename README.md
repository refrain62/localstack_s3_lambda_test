# WSL2上のLocalStackの S3 に lambdaを使ってファイルをアップロードするテスト

参考：

https://qiita.com/yasomaru/items/fa708a1f21a79e637868 
https://iti.hatenablog.jp/entry/2022/08/26/133944
https://github.com/localstack/localstack/issues/3311
https://qiita.com/sam_eng3336/items/fb67751ff1fb80b3b509


## ◆WSL2にUbuntu 22.04.1 LTS のインストール
```
Microsoft Store から 「22.04.1 LTS」をインストール
```

バージョンの確認
```
# cat /etc/os-release

PRETTY_NAME="Ubuntu 22.04.1 LTS"
```

## rootで操作
```
# sudo su - 
```

## 一応WSL2でsystemdを動かす設定
書き込んだらWSL環境を再起動。
```
# vi /etc/wsl.conf
[boot]
systemd=true
```
```
powershell > wsl --shutdown
```

## ◆Python3が入っていることの確認
```
# python3 --version
Python 3.10.6
``` 

## ◆pipが入っていない事の確認
```
# pip --version
Command 'pip' not found, but can be installed with:
apt install python3-pip
```

## ◆dockerが入っていない事の確認
```
# docker --version
Command 'docker' not found, but can be installed with:
apt install docker.io      # version 20.10.12-0ubuntu4, or
apt install podman-docker  # version 3.4.4+ds1-1ubuntu1
```

## ◆python3-pip のインストール
```
# apt install python3-pip
<中略>
# pip --version
pip 22.0.2 from /usr/lib/python3/dist-packages/pip (python 3.10)
```

## ◆docker のインストール
```
# curl https://get.docker.com | sh
<中略>
# docker --version
Docker version 20.10.21, build baeda1f

# service docker start
 * Starting Docker: docker      [ OK ]
```

## zip のインストール
```
# apt install zip
```

## ◆LocalStack導入
```
# pip install localstack
<中略>
root@DPC-01:~# localstack --version
1.3.0
```
スタートさせ、ステータスの確認
```
# localstack start -d

     __                     _______ __             __
    / /   ____  _________ _/ / ___// /_____ ______/ /__
   / /   / __ \/ ___/ __ `/ /\__ \/ __/ __ `/ ___/ //_/
  / /___/ /_/ / /__/ /_/ / /___/ / /_/ /_/ / /__/ ,<
 /_____/\____/\___/\__,_/_//____/\__/\__,_/\___/_/|_|

 💻 LocalStack CLI 1.3.0
<中略>

# localstack status services
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Service                  ┃ Status      ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ acm                      │ ✔ available │
│ apigateway               │ ✔ available │
│ cloudformation           │ ✔ available │
│ cloudwatch               │ ✔ available │
│ config                   │ ✔ available │
│ dynamodb                 │ ✔ available │
│ dynamodbstreams          │ ✔ available │
│ ec2                      │ ✔ available │
│ es                       │ ✔ available │
│ events                   │ ✔ available │
│ firehose                 │ ✔ available │
│ iam                      │ ✔ available │
│ kinesis                  │ ✔ available │
│ kms                      │ ✔ available │
│ lambda                   │ ✔ available │
│ logs                     │ ✔ available │
│ opensearch               │ ✔ available │
│ redshift                 │ ✔ available │
│ resource-groups          │ ✔ available │
│ resourcegroupstaggingapi │ ✔ available │
│ route53                  │ ✔ available │
│ route53resolver          │ ✔ available │
│ s3                       │ ✔ available │
│ s3control                │ ✔ available │
│ secretsmanager           │ ✔ available │
│ ses                      │ ✔ available │
│ sns                      │ ✔ available │
│ sqs                      │ ✔ available │
│ ssm                      │ ✔ available │
│ stepfunctions            │ ✔ available │
│ sts                      │ ✔ available │
│ support                  │ ✔ available │
│ swf                      │ ✔ available │
│ transcribe               │ ✔ available │
└──────────────────────────┴─────────────┘
```
ブラウザでアクセスして確認することも可能  
http://localhost:4566/health  
&nbsp;

## ◆awslocalをインストール
aws cliのラッパーであるawslocalをinstall
```
# # pip install awscli-local[ver1]
<中略>

# awslocal --version
aws-cli/1.27.20 Python/3.10.6 Linux/5.15.74.2-microsoft-standard-WSL2 botocore/1.29.20
```

## ◆LocalStackでS3を立ち上げて操作
「test-bucket」バケットの作成
```
# awslocal s3api create-bucket --bucket test-bucket
{
    "Location": "/test-bucket"
}

# awslocal s3 ls
2022-12-02 13:39:30 test-bucket
```
## ◆ファイルを手動でアップロード
ファイルの作成
```
# vi test.txt
test.file
```
ファイルの確認
```
# cat test.txt
test.file
```
バケット内の確認(何もない)
```
# awslocal s3 ls
2022-12-02 13:39:30 test-bucket
```
ファイルをアップロード
```
# awslocal s3 cp test.txt s3://test-bucket
upload: ./test.txt to s3://test-bucket/test.txt
```
ファイルがアップロードされていることを確認
```
# awslocal s3 ls test-bucket
2022-12-02 13:45:42         10 test.txt
```

## ◆ファイルをダウンロード
ローカルファイルを削除
```
# rm test.txt
```
ファイルをS3から取得する
```
# awslocal s3 cp s3://test-bucket/test.txt ./
download: s3://test-bucket/test.txt to ./test.txt
```
ファイルの内容を確認
```
# cat test.txt
test.file
```

&nbsp;<br />
# ここから Lambdaの操作
&nbsp;
## AWS CLIのインストール（実際の運用に近くするため）
```
# apt install awscli
```
インストールされたことの確認
```
aws --version
aws-cli/1.18.69 Python/3.8.10 Linux/5.10.16.3-microsoft-standard-WSL2 botocore/1.16.19
```

## LocalStack用のプロファイルを作成
```
# aws configure --profile localstack
AWS Access Key ID [None]: dummy
AWS Secret Access Key [None]: dummy
Default region name [None]: us-east-1
Default output format [None]: json
```
 id,keyの確認
```
# cat ~/.aws/credentials
[localstack]
aws_access_key_id = dummy
aws_secret_access_key = dummy
```
region,outputの確認確認
```
# cat ~/.aws/config
[profile localstack]
region = us-east-1
output = json
```

## バケットの作成（awslocalで作成した内容のawsコマンド版）
```
# aws --endpoint-url=http://localhost:4566 --profile localstack s3api create-bucket --bucket test-bucket
{
    "Location": "/test-bucket"
}
```

## S3バケットの確認
```
#  aws s3 ls --endpoint-url=http://localhost:4566 --profile localstack
2021-09-17 11:02:26 test-bucket
```

## とりあえずPythonで実行して操作できることを確認
スクリプトを作成
```
import boto3

def main() :
    client = boto3.client('s3', aws_access_key_id='dummy', aws_secret_access_key='dummy', region_name='us-east-1', endpoint_url='http://localhost:4566')
    response = client.list_buckets()
    client.upload_file('./test2.txt','test-bucket', 'test2.txt')
    print('upload complate')
    
if __name__ == "__main__": 
    main() 
```
スクリプトを実行
```
#  python3 test.py
upload complate
```
結果の確認  
test2.txt のファイルが作成されている
```
# awslocal s3 ls s3://test-bucket
2022-12-30 20:48:30         11 test.txt
2022-12-30 23:53:08         12 test2.txt
```


## Lambda関数の作成
```
lambda.py 参照
```

## lambda.pyをzipファイルに圧縮
lambdaに登録する場合はZIPで圧縮しないと登録できないので、一旦固める
```
# zip lambda.zip lambda.py
  adding: lambda.py (deflated 42%)
```

## LocalStack上でLambda関数作成
圧縮したZIPファイル内の「[pyファイルの名前].[メソッド名]」をhandlerで指定して、ファンクション名を指定して作成を行う
```
# awslocal lambda create-function --function-name test --runtime python3.8 --handler lambda.lambda_handler --role r1 --zip-file fileb://lambda.zip
or
# aws --endpoint-url=http://localhost:4566 lambda create-function --function-name test  --runtime python3.8 --handler lambda.lambda_handler --role r1  --zip-file fileb://lambda.zip --region us-east-1 --profile localstack
{
    "FunctionName": "test",
    "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:test",
    "Runtime": "python3.8",
    "Role": "r1",
    "Handler": "lambda.lambda_handler",
    "CodeSize": 540,
    "Description": "",
    "Timeout": 3,
    "LastModified": "2022-12-30T13:45:44.859+0000",
    "CodeSha256": "njM7DN7a4MLdGb51ukIsbzG6741qzBmGn/4hTxOkd7c=",
    "Version": "$LATEST",
    "VpcConfig": {},
    "TracingConfig": {
        "Mode": "PassThrough"
    },
    "RevisionId": "e0dd5852-4e9a-4cb0-af18-50306473a1a1",
    "State": "Active",
    "LastUpdateStatus": "Successful",
    "PackageType": "Zip",
    "Architectures": [
        "x86_64"
    ]
}
```
ファンクション名を指定して実行してみる
```
# awslocal lambda invoke --function-name test output.log
or
# aws lambda --endpoint-url=http://localhost:4566 invoke --function-name test  --profile localstack  output.log  
{
    "StatusCode": 200,
    "FunctionError": "Unhandled",
    "LogResult": "",
    "ExecutedVersion": "$LATEST"
}
```
結果を確認する（エラーになっている）
```
# cat ./output.log
{"errorMessage":"Could not connect to the endpoint URL: \"http://localhost:4566/test-bucket/2022-12-30-16-12-33.txt\"","errorType":"EndpointConnectionError","stackTrace":["  File \"/var/task/lambda.py\", line 22, in lambda_handler\n    s3.Bucket(bucket).put_object(Key=key, Body=file_contents)\n","  File \"/var/runtime/boto3/resources/factory.py\", line 520, in do_action\n    response = action(self, *args, **kwargs)\n","  File \"/var/runtime/boto3/resources/action.py\", line 83, in __call__\n    response = getattr(parent.meta.client, operation_name)(*args, **params)\n","  File \"/var/runtime/botocore/client.py\", line 357, in _api_call\n    return self._make_api_call(operation_name, kwargs)\n","  File \"/var/runtime/botocore/client.py\", line 662, in _make_api_call\n    http, parsed_response = self._make_request(\n","  File \"/var/runtime/botocore/client.py\", line 682, in _make_request\n    return self._endpoint.make_request(operation_model, request_dict)\n","  File \"/var/runtime/botocore/endpoint.py\", line 102, in make_request\n    return self._send_request(request_dict, operation_model)\n","  File \"/var/runtime/botocore/endpoint.py\", line 136, in _send_request\n    while self._needs_retry(attempts, operation_model, request_dict,\n","  File \"/var/runtime/botocore/endpoint.py\", line 253, in _needs_retry\n    responses = self._event_emitter.emit(\n","  File \"/var/runtime/botocore/hooks.py\", line 356, in emit\n    return self._emitter.emit(aliased_event_name, **kwargs)\n","  File \"/var/runtime/botocore/hooks.py\", line 228, in emit\n    return self._emit(event_name, kwargs)\n","  File \"/var/runtime/botocore/hooks.py\", line 211, in _emit\n    response = handler(**kwargs)\n","  File \"/var/runtime/botocore/retryhandler.py\", line 183, in __call__\n    if self._checker(attempts, response, caught_exception):\n","  File \"/var/runtime/botocore/retryhandler.py\", line 250, in __call__\n    should_retry = self._should_retry(attempt_number, response,\n","  File \"/var/runtime/botocore/retryhandler.py\", line 277, in _should_retry\n    return self._checker(attempt_number, response, caught_exception)\n","  File \"/var/runtime/botocore/retryhandler.py\", line 316, in __call__\n    checker_response = checker(attempt_number, response,\n","  File \"/var/runtime/botocore/retryhandler.py\", line 222, in __call__\n    return self._check_caught_exception(\n","  File \"/var/runtime/botocore/retryhandler.py\", line 359, in _check_caught_exception\n    raise caught_exception\n","  File \"/var/runtime/botocore/endpoint.py\", line 200, in _do_get_response\n    http_response = self._send(request)\n","  File \"/var/runtime/botocore/endpoint.py\", line 269, in _send\n    return self.http_session.send(request)\n","  File \"/var/runtime/botocore/httpsession.py\", line 283, in send\n    raise EndpointConnectionError(endpoint_url=request.url, error=e)\n"]}
```
解決するには以下の方法らしいが、pipでインストールしたので現状やり方が不明
```
解決策
docker-compose.ymlに LAMBDA_DOCKER_NETWORK=hostを追記
```


## 別の形のLambdaを登録(test2)
「os.getenv('LOCALSTACK_HOSTNAME')」を使って解決してみたバージョン
  
スクリプト
```
lambda2.py参照
```
ZIP作成
```
# zip lambda2.zip lambda2.py
```
ファンクション作成
```
# aws --endpoint-url=http://localhost:4566 lambda create-function --function-name test2  --runtime python3.8 --handler lambda2.lambda_handler --role r1  --zip-file fileb://lambda2.zip --region us-east-1 --profile localstack
{
    "FunctionName": "test2",
    "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:test2",
    "Runtime": "python3.8",
    "Role": "r1",
    "Handler": "lambda2.lambda_handler",
    "CodeSize": 623,
    "Description": "",
    "Timeout": 3,
    "LastModified": "2022-12-30T15:07:52.209+0000",
    "CodeSha256": "ODT6dfdPrK8WZmOyk4HDDeNObzrIh6kzt9DNcLBAZXQ=",
    "Version": "$LATEST",
    "VpcConfig": {},
    "TracingConfig": {
        "Mode": "PassThrough"
    },
    "RevisionId": "4c2580cb-8c80-42ca-918e-6b5ad7f60f04",
    "State": "Active",
    "LastUpdateStatus": "Successful",
    "PackageType": "Zip",
    "Architectures": [
        "x86_64"
    ]
}
```
実行
```
# aws lambda --endpoint-url=http://localhost:4566 invoke --function-name test2  --profile localstack  result2.log                                                                                  {
    "StatusCode": 200,
    "LogResult": "",
    "ExecutedVersion": "$LATEST"
}
```
結果の確認
```
# cat result2.log
"create file2022-12-30-15-08-08.txt"
```
作成できたかの確認
```
# awslocal s3 ls s3://test-bucket
2022-12-31 00:08:08         16 2022-12-30-15-08-08.txt
2022-12-30 20:48:30         11 test.txt
2022-12-30 23:53:08         12 test2.txt
```
日付のファイルができた  
&nbsp;  
&nbsp;  


## 別の形のLambdaを登録(test3)
スクリプト
```
test3.py参照
```
ZIP作成
```
# zip lambda3.zip test3.py
```
ファンクション作成  
ZIPファイル名ではなく、pyファイルの名前になるので注意!
```
# aws --endpoint-url=http://localhost:4566 lambda create-function --function-name test3  --runtime python3.8 --handler test3.handler --role r1  --zip-file fileb://lambda3.zip --region us-east-1 -
-profile localstack
{
    "FunctionName": "test3",
    "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:test3",
    "Runtime": "python3.8",
    "Role": "r1",
    "Handler": "test3.handler",
    "CodeSize": 482,
    "Description": "",
    "Timeout": 3,
    "LastModified": "2022-12-30T15:05:27.229+0000",
    "CodeSha256": "czeM0f2836amReNrVJIN7L/TD8w324on8wfKK463bhg=",
    "Version": "$LATEST",
    "VpcConfig": {},
    "TracingConfig": {
        "Mode": "PassThrough"
    },
    "RevisionId": "867b9286-f3a9-418c-a01e-775d21044da8",
    "State": "Active",
    "LastUpdateStatus": "Successful",
    "PackageType": "Zip",
    "Architectures": [
        "x86_64"
    ]
}
```
実行
```
# aws lambda --endpoint-url=http://localhost:4566 invoke --function-name test3  --profile localstack  result3.log
{
    "StatusCode": 200,
    "LogResult": "",
    "ExecutedVersion": "$LATEST"
}
```
結果の確認
```
# cat result3.log
{"message":"a-object placed into S3"}
```
作成できたかの確認
```
# awslocal s3 ls s3://
2022-12-30 20:44:13 test-bucket
2022-12-31 00:05:39 a-bucket
```
バケット内の確認
```
# awslocal s3 ls s3://a-bucket
2022-12-31 00:05:39          9 a-object
```
作成された
