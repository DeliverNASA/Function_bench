from time import time
import gzip
import os
import shutil
import numpy as np

# 测量压缩的延迟
def lambda_handler(event, context):
    file_size = event['file_size']
    file_write_path = './dataset/file/test_disk_compress'

    start = time()
    with open(file_write_path, 'wb') as f:
        f.write(os.urandom(file_size * 1024 * 1024))
    disk_latency = time() - start

    f.close()

    with open(file_write_path, 'rb') as f:
        start = time()
        with gzip.open('./dataset/file/test_disk_compress_result.gz', 'wb') as gz:
            # gz.writelines(f)
            shutil.copyfileobj(f, gz)
        compress_latency = time() - start

    # print(compress_latency)

    # return {'disk_write': disk_latency, "compress": compress_latency}
    return compress_latency


if __name__ == "__main__":
    event = dict()
    event['file_size'] = 8
    lambda_handler(event, context=None)

    print()
    print("#### test: gzip_cpmpression ####")
    total = list()
    for i in range(10):
        total.append(lambda_handler(event=event, context=None))
    print("mean: " + str(np.mean(total)))
    print("std:  " + str(np.std(total)))