# import boto3
# import uuid
from time import time
import numpy as np
import cv2
import argparse

from time_limit import set_time_limit


parser = argparse.ArgumentParser()
parser.add_argument('-object_key', type=str, default="testVideo001.mp4")
args = parser.parse_args()


dataset_path = "./dataset/"
result_path = dataset_path + "video_transform/"
FILE_NAME_INDEX = 0
FILE_PATH_INDEX = 2


def video_processing(object_key, video_path, model_path):
    file_name = object_key.split(".")[FILE_NAME_INDEX]
    result_file_path = result_path + file_name + '-detection.avi'

    video = cv2.VideoCapture(video_path)

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    face_cascade = cv2.CascadeClassifier(model_path)

    start = time()
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
            # print("Found {0} faces!".format(len(faces)))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            out.write(frame)
        else:
            break

    latency = time() - start
    print(latency)
    video.release()
    out.release()

    return latency, result_file_path


@set_time_limit()
def lambda_handler(event, context):
    input_bucket = event['input_bucket']
    object_key = event['object_key']
    # output_bucket = event['output_bucket']

    model_bucket = event['model_bucket']
    model_object_key = event['model_object_key'] # example : haarcascade_frontalface_default.xml
    # download_path = tmp+'{}{}'.format(uuid.uuid4(), object_key)
    # s3_client.download_file(input_bucket, object_key, download_path)
    download_path = input_bucket + object_key

    # model_path = tmp + '{}{}'.format(uuid.uuid4(), model_object_key)
    # s3_client.download_file(model_bucket, model_object_key, model_path)
    model_path = model_bucket + model_object_key

    latency, upload_path = video_processing(object_key, download_path, model_path)

    # s3_client.upload_file(upload_path, output_bucket, upload_path.split("/")[FILE_PATH_INDEX])

    return latency


if __name__ == "__main__":
    event = dict()
    event['input_bucket'] = dataset_path + "video/"
    event['object_key'] = args.object_key
    event['model_bucket'] = dataset_path + "model/"
    event['model_object_key'] = "haarcascade_frontalface_default.xml"

    # print()
    # print("#### test: ml_video_face_detection ####")
    total = list()
    for i in range(1):
        total.append(lambda_handler(event=event, context=None))
    # print("mean: " + str(np.mean(total)))
    # print("std:  " + str(np.std(total)))