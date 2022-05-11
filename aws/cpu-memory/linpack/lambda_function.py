from numpy import matrix, linalg, random
from time import time
import numpy as np
import argparse

from time_limit import set_time_limit


parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, default=1000)
args = parser.parse_args()

def linpack(n):
    # LINPACK benchmarks
    ops = (2.0 * n) * n * n / 3.0 + (2.0 * n) * n

    # Create AxA array of random numbers -0.5 to 0.5
    A = random.random_sample((n, n)) - 0.5
    B = A.sum(axis=1)

    # Convert to matrices
    A = matrix(A)
    B = matrix(B.reshape((n, 1)))

    # Ax = B
    start = time()
    x = linalg.solve(A, B)
    latency = time() - start

    mflops = (ops * 1e-6 / latency)
    result = latency

    return result

@set_time_limit()
def lambda_handler(event, context):
    n = int(event['n'])
    result = linpack(n)
    # print(result)
    return result


if __name__ == '__main__':
    event = dict()
    event['n'] = args.n

    # print()
    # print("#### test: linpack ####")
    total = list()
    for i in range(1):
        total.append(lambda_handler(event=event, context=None))
    # 这里在测试的时候会出现有一组数据极大的偏离
    # total.remove(max(total))
    # print("mean: " + str(np.mean(total)))
    # print("std:  " + str(np.std(total)))