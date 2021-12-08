from time import time
import subprocess
import os
import numpy as np

def lambda_handler(event, context):
    file_size = event['file_size']
    byte_size = int(event['byte_size'])

    file_write_path = './dataset/file/test_disk_sequential'

    # 随机向文件中输入
    start = time()
    with open(file_write_path, 'wb', buffering=byte_size) as f:
        f.write(os.urandom(file_size * 1024 * 1024))
        f.flush()
        os.fsync(f.fileno())    # 确保相关信息写入硬盘
    disk_write_latency = time() - start
    disk_write_bandwidth = file_size / disk_write_latency 

    f.close()

    # 查看tmp目录下的内容
    # output = subprocess.check_output(['ls', '-alh', './dataset/file/'])
    # output = subprocess.check_output(['ls', '-alh', './dataset/file/'])
    # print(output)
    
    # 从文件读取内容
    i = 0
    start = time()
    with open(file_write_path, 'rb', buffering=byte_size) as f:
        byte = f.read(byte_size)
        while byte:
            byte = f.read(byte_size)
    disk_read_latency = time() - start
    disk_read_bandwidth = file_size / disk_read_latency 

    f.close()

    # 测试结束后删除文件内容
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
    print("#### test: sequential_disk_io ####")
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
