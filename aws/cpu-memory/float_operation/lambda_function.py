import math
from time import time
import numpy as np
import argparse

from time_limit import set_time_limit

parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, default=1000000)
args = parser.parse_args()

def float_operations(n):
    start = time()
    for i in range(0, n):
        sin_i = math.sin(i)
        cos_i = math.cos(i)
        sqrt_i = math.sqrt(i)
    latency = time() - start
    return latency


@set_time_limit()
def lambda_handler(event, context):
    n = int(event['n'])
    result = float_operations(n)
    # print(result)
    return result


if __name__ == '__main__':
    event = dict()
    event['n'] = args.n

    # print()
    # print("#### test: float_operation ####")
    total = list()
    for i in range(1):
        total.append(lambda_handler(event=event, context=None))
    # print("mean: " + str(np.mean(total)))
    # print("std:  " + str(np.std(total)))
