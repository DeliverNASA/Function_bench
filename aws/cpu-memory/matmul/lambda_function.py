import numpy as np
from time import time
import argparse

from time_limit import set_time_limit


parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, default=1000)
args = parser.parse_args()


def matmul(n):
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)

    start = time()
    C = np.matmul(A, B)
    latency = time() - start
    return latency

@set_time_limit()
def lambda_handler(event, context):
    n = int(event['n'])
    result = matmul(n)
    return result

if __name__ == '__main__':
    event = dict()
    event['n'] = args.n

    # print()
    # print("#### test: matmul ####")
    total = list()
    for i in range(20):
        total.append(lambda_handler(event=event, context=None))
    # print("mean: " + str(np.mean(total)))
    # print("std:  " + str(np.std(total)))
