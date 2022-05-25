# define the priority of tasks
import heapq
import queue
import sys
import os
import threading
import time

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
from tools.cmd_parser2 import parse_cmd

# all_functions
functions = ["chameleon", "feature_extractor", "float_operation", "image_processing", "linpack", "matmul",
            "ml_lr_prediction", "ml_video_face_detection", "model_training", "pyaes", "video_processing"]
# priority
priority1 = ["chameleon", "float_operation", "linpack", "matmul", "pyaes"]
priority2 = ["feature_extractor", "image_processing"]
priority3 = ["ml_lr_prediction", "ml_video_face_detection", "model_training", "video_processing"]

cpu_log_file = "./script/application/log/cpu.txt"


class Task:
    # input: func_info like [func_id, arg1, arg2, ...]
    def __init__(self, func):
        # self.func_name = func_name
        # self.func_args = func_args
        self.func = func
        self.priority = self.set_priority(functions[func[0]], func[1:])
        self.command = parse_cmd(functions[func[0]], func[1:])
    
    def get_func(self):
        return self.func

    def get_command(self):
        return self.command

    def get_priority(self):
        return self.priority
    
    def set_priority(self, func_name, func_args):
        func_type = 0
        if func_name in priority1:
            func_type = 1
        elif func_name in priority2:
            func_type = 2
        else:
            func_type = 3
        return func_type * 2000000 + func_args[0]


class CPU_Monitor:
    def __init__(self, period):
        self.period = period
    def run(self):
        while True:
            time.sleep(self.period)
            cmd = "docker stats --no-stream --no-trunc --format \"{{.Name}},{{.ID}},{{.CPUPerc}}\" > " + cpu_log_file
            os.system(cmd)



if __name__ == "__main__":
    # tt = Task("chameleon", [400])
    # tt = Task([1,10])
    # bind monitor process on cores 1-7 (core 0 only for containers)
    os.system("taskset -pc 1-7 " + str(os.getpid()))
    cpu_m = CPU_Monitor(period=3)
    cpu_m.run()