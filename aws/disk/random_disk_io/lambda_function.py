from time import time
import subprocess
import os
import random
import numpy as np

def lambda_handler(event, context):
    file_size = event['file_size']
    byte_size = int(event['byte_size'])
    file_write_path = './dataset/file/test_disk_random'
    
    # 随机生成要写入的内容
    block = os.urandom(byte_size) 
    total_file_bytes = file_size * 1024 * 1024 - byte_size
    
    start = time()
    # 在文件的随机位置写入数据
    with open(file_write_path, 'wb') as f:
        for _ in range(int(total_file_bytes/byte_size)):
            f.seek(random.randrange(total_file_bytes))
            f.write(block)
        f.flush()
        os.fsync(f.fileno())
    disk_write_latency = time() - start
    disk_write_bandwidth = file_size / disk_write_latency 

    # output = subprocess.check_output(['ls', '-alh', '/tmp/'])
    # print(output)
    
    start = time()
    with open(file_write_path, 'rb') as f:
        for _ in range(int(total_file_bytes/byte_size)):
            f.seek(random.randrange(total_file_bytes))
            f.read(byte_size)
    disk_read_latency = time() - start
    disk_read_bandwidth = file_size / disk_read_latency 

    rm = subprocess.Popen(['rm', '-rf', file_write_path])
    rm.communicate()
    
    # print(disk_write_bandwidth)
    # print(disk_write_latency)
    # print(disk_read_bandwidth)
    # print(disk_read_latency)
    
    return {
        'disk_write_bandwidth':disk_write_bandwidth, 
        'disk_write_latency':disk_write_latency,
        'disk_read_bandwidth':disk_read_bandwidth, 
        'disk_read_latency':disk_read_latency
    }



if __name__ == "__main__":
    event = dict()
    event['file_size'] = 8
    event['byte_size'] = 512

    print()
    print("#### test: random_disk_io ####")
    disk_write_bandwidth = list()
    disk_write_latency = list()
    disk_read_bandwidth = list()
    disk_read_latency = list()
    for i in range(10):
        result = lambda_handler(event=event, context=None)
        disk_write_bandwidth.append(result['disk_write_bandwidth'])
        disk_write_latency.append(result['disk_write_latency'])
        disk_read_bandwidth.append(result['disk_read_bandwidth'])
        disk_read_latency.append(result['disk_read_latency'])
    print("**** disk_write_bandwidth ****")
    print("mean: " + str(np.mean(disk_write_bandwidth)))
    print("std:  " + str(np.std(disk_write_bandwidth)))
    print("**** disk_write_latency ****")
    print("mean: " + str(np.mean(disk_write_latency)))
    print("std:  " + str(np.std(disk_write_latency)))
    print("**** disk_read_bandwidth ****")
    print("mean: " + str(np.mean(disk_read_bandwidth)))
    print("std:  " + str(np.std(disk_read_bandwidth)))
    print("**** disk_read_latency ****")
    print("mean: " + str(np.mean(disk_read_latency)))
    print("std:  " + str(np.std(disk_read_latency)))