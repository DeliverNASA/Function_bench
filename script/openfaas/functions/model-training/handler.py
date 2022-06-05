from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

import pandas as pd
from time import time
import re

cleanup_re = re.compile('[^a-z]+')
tmp = "./dataset/model/"


def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence

def handle(req):
    # dataset_bucket = event['dataset_bucket']
    # dataset_object_key = event['dataset_object_key']
    # # model_bucket = event['model_bucket']
    # model_object_key = event['model_object_key']  # example : lr_model.pk

    # obj = s3_client.get_object(Bucket=dataset_bucket, Key=dataset_object_key)
    # df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    # path = dataset_bucket + "/" + dataset_object_key
    path = "/home/app/function/reviews10mb.csv"
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
    return latency


if __name__ == "__main__":
    handle(None)
    # print("mean: " + str(np.mean(total)))
    # print("std:  " + str(np.std(total)))