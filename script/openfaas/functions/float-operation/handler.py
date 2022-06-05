import math
from time import time

def float_operations(n):
    start = time()
    for i in range(0, n):
        sin_i = math.sin(i)
        cos_i = math.cos(i)
        sqrt_i = math.sqrt(i)
    latency = time() - start
    return latency


def handle(req):
    n = int(req)
    result = float_operations(n)
    # print(result)
    return result


if __name__ == '__main__':
    # print()
    # print("#### test: float_operation ####")
    handle(1000000)
