import math
from time import time
import numpy as np


def float_operations(n):
    start = time()
    for i in range(0, n):
        sin_i = math.sin(i)
        cos_i = math.cos(i)
        sqrt_i = math.sqrt(i)
    latency = time() - start
    return latency


def lambda_handler(event, context):
    n = int(event['n'])
    result = float_operations(n)
    # print(result)
    return result


if __name__ == '__main__':
    event = dict()
    event['n'] = 1000000

    print()
    print("#### test: float_operation ####")
    total = list()
    for i in range(10):
        total.append(lambda_handler(event=event, context=None))
    print("mean: " + str(np.mean(total)))
    print("std:  " + str(np.std(total)))
