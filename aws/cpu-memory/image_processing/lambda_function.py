# import boto3
# import uuid
from time import time
from PIL import Image
import numpy as np

import ops

# s3_client = boto3.client('s3')
FILE_NAME_INDEX = 2


def image_processing(file_name, image_path):
    path_list = []
    start = time()
    with Image.open(image_path) as image:
        tmp = image
        path_list += ops.flip(image, file_name)
        path_list += ops.rotate(image, file_name)
        path_list += ops.filter(image, file_name)
        path_list += ops.gray_scale(image, file_name)
        path_list += ops.resize(image, file_name)

    latency = time() - start
    return latency, path_list


def lambda_handler(event, context):
    # input_bucket = event['input_bucket']
    object_key = event['object_key']
    # output_bucket = event['output_bucket']

    # download_path = '/tmp/{}{}'.format(uuid.uuid4(), object_key)
    download_path = './dataset/image/animal-dog.jpg'

    # s3_client.download_file(input_bucket, object_key, download_path)

    latency, path_list = image_processing(object_key, download_path)
    # print(latency)
    # print(path_list)

    # for upload_path in path_list:
    #     s3_client.upload_file(upload_path, output_bucket, upload_path.split("/")[FILE_NAME_INDEX])

    return latency


if __name__ == '__main__':
    event = dict()
    event['object_key'] = 'animal-dog.jpg'

    print()
    print("#### test: image_processing ####")
    total = list()
    for i in range(5):
        total.append(lambda_handler(event=event, context=None))
    print("mean: " + str(np.mean(total)))
    print("std:  " + str(np.std(total)))