# import boto3
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import pandas as pd
import numpy as np
from time import time
import os
import re

# s3_client = boto3.client('s3')
cleanup_re = re.compile('[^a-z]+')

dataset_path = "./dataset/"
result_path = dataset_path + "video_transform/"

def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence


# 模型训练完成之后的预测
def lambda_handler(event, context):
    x = event['x']
    # print(x)

    dataset_object_key = event['dataset_object_key']
    dataset_bucket = event['dataset_bucket']

    model_object_key = event['model_object_key']  # example : lr_model.pk
    model_bucket = event['model_bucket']

    model_path = model_bucket + model_object_key
    # if not os.path.isfile(model_path):
        # s3_client.download_file(model_bucket, model_object_key, model_path)

    # dataset_path = 's3://'+dataset_bucket+'/'+dataset_object_key
    data_path = dataset_bucket + dataset_object_key
    # 这里读取的是reviews20mv.csv数据集合
    dataset = pd.read_csv(data_path)

    start = time()

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
    # print(y[0])
    print(latency)

    return latency
    # return {'y': y, 'latency': latency}


if __name__ == "__main__":
    event = dict()
    event['dataset_bucket'] = dataset_path + "amzn_fine_food_reviews/"
    event['dataset_object_key'] = "reviews10mb.csv"
    event['model_bucket'] = dataset_path + "model/"
    event['model_object_key'] = "tmp_lr_model.pk"

    # 传入测试集的数据
    test_path = dataset_path + "amzn_fine_food_reviews/reviews20mb.csv"
    test_dataset = pd.read_csv(test_path)
    event['x'] = test_dataset['Text']

    print()
    print("#### test: ml_lr_prediction ####")
    total = list()
    for i in range(10):
        total.append(lambda_handler(event=event, context=None))
    print("mean: " + str(np.mean(total)))
    print("std:  " + str(np.std(total)))