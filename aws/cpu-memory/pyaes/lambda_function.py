from time import time
import random
import string
import pyaes
import numpy as np
import argparse

from time_limit import set_time_limit


parser = argparse.ArgumentParser()
parser.add_argument('-length_of_message', type=int, default=1024)
parser.add_argument('-num_of_iterations', type=int, default=32)
args = parser.parse_args()


def generate(length):
    # 随机生成一个长度为length的小写字母和数字的组合字符串
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

@set_time_limit()
def lambda_handler(event, context):
    length_of_message = event['length_of_message']
    num_of_iterations = event['num_of_iterations']

    message = generate(length_of_message)

    # 128-bit key (16 bytes)
    KEY = b'\xa1\xf6%\x8c\x87}_\xcd\x89dHE8\xbf\xc9,'

    start = time()
    for loops in range(num_of_iterations):
        # 这里使用的是pyaes下的一种AES加密算法
        aes = pyaes.AESModeOfOperationCTR(KEY)
        ciphertext = aes.encrypt(message)
        # print(ciphertext)

        aes = pyaes.AESModeOfOperationCTR(KEY)
        plaintext = aes.decrypt(ciphertext)
        # print(plaintext)
        aes = None

    latency = time() - start
    # print(latency)
    return latency


if __name__ == "__main__":
    event = dict()
    event['length_of_message'] = args.length_of_message
    event['num_of_iterations'] = args.num_of_iterations

    # print()
    # print("#### test: pyaes ####")
    total = list()
    for i in range(1):
        total.append(lambda_handler(event=event, context=None))
    # print("mean: " + str(np.mean(total)))
    # print("std:  " + str(np.std(total)))