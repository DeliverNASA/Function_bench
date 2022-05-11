# import boto3
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import pandas as pd
import numpy as np
from time import time
import os
import re
import argparse

from time_limit import set_time_limit


parser = argparse.ArgumentParser()
parser.add_argument('-dataset_bucket', type=str, default="amzn_fine_food_reviews/")
parser.add_argument('-dataset_train_object_key', type=str, default="reviews10mb.csv")
parser.add_argument('-dataset_test_object_key', type=str, default="reviews20mb.csv")
args = parser.parse_args()


cleanup_re = re.compile('[^a-z]+')

dataset_path = "./dataset/"
result_path = dataset_path + "video_transform/"

def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence


# 模型训练完成之后的预测
@set_time_limit()
def lambda_handler(event, context):
    x = event['x']
    # print(x)

    dataset_object_key = event['dataset_train_object_key']
    dataset_bucket = event['dataset_bucket']

    model_object_key = event['model_object_key']  # example : lr_model.pk
    model_bucket = event['model_bucket']

    model_path = model_bucket + model_object_key

    data_path = dataset_bucket + dataset_object_key
    # 这里读取的是reviews20mv.csv数据集合
    dataset = pd.read_csv(data_path)

    start = time()

    # df_input对应的是测试集
    df_input = pd.DataFrame()
    # df_input['x'] = [x]
    df_input['x'] = x
    df_input['x'] = df_input['x'].apply(cleanup)

    dataset['train'] = dataset['Text'].apply(cleanup)

    tfidf_vect = TfidfVectorizer(min_df=100).fit(dataset['train'])
    # # 用相同的处理方法去处理测试集的数据
    X = tfidf_vect.transform(df_input['x'])

    model = joblib.load(model_path)
    y = model.predict(X)

    latency = time() - start

    return latency


if __name__ == "__main__":
    event = dict()
    event['dataset_bucket'] = dataset_path + args.dataset_bucket
    event['dataset_train_object_key'] = args.dataset_train_object_key
    event['model_bucket'] = dataset_path + "model/"
    event['model_object_key'] = "tmp_lr_model.pk"

    # 传入测试集的数据
    test_path = dataset_path + args.dataset_bucket + args.dataset_test_object_key
    test_dataset = pd.read_csv(test_path)
    event['x'] = test_dataset['Text']

    # print()
    # print("#### test: ml_lr_prediction ####")
    total = list()
    for i in range(1):
        total.append(lambda_handler(event=event, context=None))
    # print("mean: " + str(np.mean(total)))
    # print("std:  " + str(np.std(total)))