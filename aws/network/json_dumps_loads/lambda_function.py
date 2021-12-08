import json
from urllib.request import urlopen
from time import time
import numpy as np


def lambda_handler(event, context):
    # 读取的是一个为网页的前端代码
    link = event['link']  # https://github.com/jdorfman/awesome-json-datasets

    start = time()
    f = urlopen(link)
    data = f.read().decode("utf-8")
    # file_write_path = './dataset/file/test_net'
    # with open(file_write_path, 'w') as f:
    #     f.write(data)
    network = time() - start

    # json.loads函数将字符串转化为字典
    # json.dumps将字典序列化为字符串
    start = time()
    json_data = json.loads(data)
    str_json = json.dumps(json_data, indent=4)
    latency = time() - start

    # print(str_json)
    # print(network)
    # print(latency)
    return {"network": network, "serialization": latency}


if __name__ == "__main__":
    event = dict()
    event['link'] = "http://www.vizgr.org/historical-events/search.php?format=json&begin_date=-3000000&end_date=20151231&lang=en"
    
    print()
    print("#### test: json_dump_loads ####")
    network = list()
    serialization = list()
    for i in range(1):
        result = lambda_handler(event=event, context=None)
        network.append(result['network'])
        serialization.append(result['serialization'])
    print("**** network ****")
    print("mean: " + str(np.mean(network)))
    print("std:  " + str(np.std(network)))
    print("**** serialization ****")
    print("mean: " + str(np.mean(serialization)))
    print("std:  " + str(np.std(serialization)))