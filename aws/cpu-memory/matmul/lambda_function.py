import numpy as np
from time import time


def matmul(n):
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)

    start = time()
    C = np.matmul(A, B)
    latency = time() - start
    return latency


def lambda_handler(event, context):
    n = int(event['n'])
    result = matmul(n)
    # print(result)
    return result

if __name__ == '__main__':
    event = dict()
    event['n'] = 300

    print()
    print("#### test: matmul ####")
    total = list()
    for i in range(100):
        total.append(lambda_handler(event=event, context=None))
    print("mean: " + str(np.mean(total)))
    print("std:  " + str(np.std(total)))
