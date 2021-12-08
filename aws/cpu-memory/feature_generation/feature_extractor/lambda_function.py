# import boto3
import pandas as pd
from time import time
import re
import numpy as np

# s3 = boto3.client('s3')

# 只匹配a-z之间的字符
cleanup_re = re.compile('[^a-z]+')
file_path = "./dataset/file/"

# 小写化并清除所有的标点符号
def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence


def lambda_handler(event, context):
    bucket = event['input_bucket']
    key = event['key']
    path = bucket + "/" + key
    # # df = pd.read_csv('s3://' + path)
    df = pd.read_csv(path)

    # 统计
    start = time()
    df['Text'] = df['Text'].apply(cleanup)
    text = df['Text'].tolist()
    # 将一个数据集所有的单词添加到字典中
    result = set()
    for item in text:
        result.update(item.split())
    # print("Number of Feature : " + str(len(result)))

    feature = str(list(result))
    feature = feature.lstrip('[').rstrip(']').replace(' ', '')
    latency = time() - start
    # print(latency)

    # write_key = event['key'].split('.')[0] + ".txt"
    # s3.put_object(Body=feature, Bucket=bucket, Key=write_key)
    # file_name = file_path + event['key'].split('.')[0] + ".txt"
    # with open (file_name, "w") as f:
    #     f.write(feature)
    # f.close()
    return latency

if __name__ == "__main__":
    event = dict()
    event['input_bucket'] = "./dataset/amzn_fine_food_reviews"
    event['key'] = "reviews10mb.csv"

    print()
    print("#### test: feature_extractor ####")
    total = list()
    for i in range(10):
        total.append(lambda_handler(event=event, context=None))
    print("mean: " + str(np.mean(total)))
    print("std:  " + str(np.std(total)))