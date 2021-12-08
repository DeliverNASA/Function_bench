import json
import boto3
from time import time

# Create S3 session
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

subs = "</title><text>"
computer_language = ["JavaScript", "Java", "PHP", "Python", "C#", "C++",
                     "Ruby", "CSS", "Objective-C", "Perl",
                     "Scala", "Haskell", "MATLAB", "Clojure", "Groovy"]


def lambda_handler(event, context):
    job_bucket = event['job_bucket']
    src_bucket = event['bucket']
    src_keys = event['keys']
    mapper_id = event['mapper_id']

    output = {}

    for lang in computer_language:
        output[lang] = 0

    network = 0
    map = 0
    keys = src_keys.split('/')

    # Download and process all keys
    for key in keys:
        print(key)
        start = time()
        response = s3_client.get_object(Bucket=src_bucket, Key=key)
        contents = response['Body'].read()
        network += time() - start

        start = time()
        for line in contents.split('\n')[:-1]:
            # 找到带有 "</title><text>" 标签的位置
            # text 截取的是标签后面的所有内容
            # 查看是否有lang中的语言名称，统计出现的次数
            idx = line.find(subs)
            text = line[idx + len(subs): len(line) - 16]
            for lang in computer_language:
                if lang in text:
                    output[lang] += 1
        # map 统计的是执行map过程的时间
        map += time() - start

    print(output)

    metadata = {
        'output': str(output),
        'network': str(network),
        'map': str(map)
    }

    start = time()
    s3.Bucket(job_bucket).put_object(Key=str(mapper_id), Body=json.dumps(output), Metadata=metadata)
    # network 网络通信所需要的时间，包括下载和上传
    network += time() - start
    
    return json.dumps(metadata)
