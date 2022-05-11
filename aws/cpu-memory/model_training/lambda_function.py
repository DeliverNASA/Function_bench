# import boto3

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np

import pandas as pd
from time import process_time_ns, time
import re
import io
import argparse

from time_limit import set_time_limit

parser = argparse.ArgumentParser()
parser.add_argument('-dataset_object_key', type=str, default="reviews10mb.csv")
args = parser.parse_args()

cleanup_re = re.compile('[^a-z]+')
tmp = "./dataset/model/"


def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence

@set_time_limit()
def lambda_handler(event, context):
    dataset_bucket = event['dataset_bucket']
    dataset_object_key = event['dataset_object_key']
    # model_bucket = event['model_bucket']
    model_object_key = event['model_object_key']  # example : lr_model.pk

    # obj = s3_client.get_object(Bucket=dataset_bucket, Key=dataset_object_key)
    # df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    path = dataset_bucket + "/" + dataset_object_key
    df = pd.read_csv(path)

    start = time()
    df['train'] = df['Text'].apply(cleanup)

    # 忽略出现次数小于100次的单词
    tfidf_vector = TfidfVectorizer(min_df=100).fit(df['train'])
    # print(tfidf_vector.get_feature_names_out())
    # print(tfidf_vector.get_feature_names_out())
    # 计算每一个语句的向量表示
    train = tfidf_vector.transform(df['train'])

    model = LogisticRegression(max_iter=1000)
    model.fit(train, df['Score'])
    latency = time() - start

    # 测试的时候就不保存模型了
    # model_file_path = tmp + model_object_key
    # joblib.dump(model, model_file_path)
    # print(latency)

    # s3_client.upload_file(model_file_path, model_bucket, model_object_key)

    return latency


if __name__ == "__main__":
    event = dict()
    event['dataset_bucket'] = "./dataset/amzn_fine_food_reviews"
    event['dataset_object_key'] = args.dataset_object_key
    # event['model_bucket'] = ""
    event['model_object_key'] = "tmp_lr_model.pk"

    # print()
    # print("#### test: model_training ####")
    total = list()
    for i in range(1):
        total.append(lambda_handler(event=event, context=None))
    # print("mean: " + str(np.mean(total)))
    # print("std:  " + str(np.std(total)))