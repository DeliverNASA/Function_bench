from time import time
from PIL import Image
import numpy as np
import ops
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-download_path', type=str, default="./dataset/image/")
parser.add_argument('-object_key', type=str, default="animal-dog.jpg")
args = parser.parse_args()

FILE_NAME_INDEX = 2

def image_processing(file_name, image_path):
    path_list = []
    start = time()
    with Image.open(image_path) as image:
        path_list += ops.flip(image, file_name)
        path_list += ops.rotate(image, file_name)
        path_list += ops.filter(image, file_name)
        path_list += ops.gray_scale(image, file_name)
        path_list += ops.resize(image, file_name)

    latency = time() - start
    return latency, path_list


def lambda_handler(event, context):
    download_path = event['download_path']
    object_key = event['object_key']

    latency, path_list = image_processing(object_key, download_path+object_key)
    return latency


if __name__ == '__main__':
    event = dict()
    event['object_key'] = args.object_key
    event['download_path'] = args.download_path

    print()
    print("#### test: image_processing ####")
    total = list()
    for i in range(5):
        total.append(lambda_handler(event=event, context=None))
    print("mean: " + str(np.mean(total)))
    print("std:  " + str(np.std(total)))