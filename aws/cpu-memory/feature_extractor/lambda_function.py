# import boto3
import pandas as pd
from time import time
import re
import numpy as np
import argparse

from time_limit import set_time_limit

parser = argparse.ArgumentParser()
parser.add_argument('-input_bucket', type=str, default="./dataset/amzn_fine_food_reviews")
parser.add_argument('-object_key', type=str, default="reviews10mb.csv")
args = parser.parse_args()


# 只匹配a-z之间的字符
cleanup_re = re.compile('[^a-z]+')
file_path = "./dataset/file/"

# 小写化并清除所有的标点符号
def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence

@set_time_limit()
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
    event['input_bucket'] = args.input_bucket
    event['key'] = args.object_key

    # print()
    # print("#### test: feature_extractor ####")
    total = list()
    for i in range(1):
        total.append(lambda_handler(event=event, context=None))
    # print("mean: " + str(np.mean(total)))
    # print("std:  " + str(np.std(total)))