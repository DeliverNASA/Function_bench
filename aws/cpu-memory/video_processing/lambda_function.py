# import boto3
# import uuid
from time import time
import cv2
import numpy as np
import argparse

from time_limit import set_time_limit


parser = argparse.ArgumentParser()
parser.add_argument('-object_key', type=str, default="testVideo001.mp4")
args = parser.parse_args()

tmp = "/usr/local/test_scripts/dataset/video_transform/"
FILE_NAME_INDEX = 0
FILE_PATH_INDEX = 2


def video_processing(object_key, video_path):
    file_name = object_key.split(".")[FILE_NAME_INDEX]
    result_file_path = tmp+file_name+'-output.avi'

    video = cv2.VideoCapture(video_path)

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    start = time()
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            tmp_file_path = tmp+'tmp.jpg'
            cv2.imwrite(tmp_file_path, gray_frame)
            gray_frame = cv2.imread(tmp_file_path)
            out.write(gray_frame)
        else:
            break

    latency = time() - start

    video.release()
    out.release()
    return latency, result_file_path

@set_time_limit()
def lambda_handler(event, context):
    # input_bucket = event['input_bucket']
    object_key = event['object_key']
    # output_bucket = event['output_bucket']
    download_path = event['download_path']
    # download_path = tmp+'{}{}'.format(uuid.uuid4(), object_key)
    # download_path = './dataset/video/testVideo001.mp4'

    # s3_client.download_file(input_bucket, object_key, download_path)

    latency, upload_path = video_processing(object_key, download_path)
    # print(latency)

    # s3_client.upload_file(upload_path, output_bucket, upload_path.split("/")[FILE_PATH_INDEX])

    return latency


if __name__ == "__main__":
    event = dict()
    event['object_key'] = args.object_key
    event['download_path'] = './dataset/video/' + args.object_key


    # print()
    # print("#### test: video_processing ####")
    total = list()
    for i in range(1):
        total.append(lambda_handler(event=event, context=None))
    # print("mean: " + str(np.mean(total)))
    # print("std:  " + str(np.std(total)))