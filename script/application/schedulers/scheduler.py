import queue
import os
import sys
import threading
from queue import Queue, PriorityQueue
from threading import Lock
from time import time

import pandas as pd
import re
import numpy as np
import joblib as jb
from sklearn.preprocessing import StandardScaler

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
from tools.cmd_parser2 import parse_cmd

AVAIALBLE_THRESHOLD = 0.05
REGROUP_PERIOD = 5
GROUP_SIZE = 5
RECORD_INTERVAL = 0.1

cpu_log_file = "./script/application/log/cpu.txt"
latency_record = "./script/application/log/latency.txt"
time_record = "./script/application/log/time_finish.txt"
model_basic_path = "./record/model/"

functions = ["chameleon", "feature_extractor", "float_operation", "image_processing", "linpack", "matmul",
            "ml_lr_prediction", "ml_video_face_detection", "model_training", "pyaes", "video_processing"]


class Scheduler:
    def __init__(self, all_tasks_num, containers, is_dy_alloc) -> None:
        self.queue = Queue()
        self.queue_lock = Lock()
        self.all_tasks_num = all_tasks_num
        self.finished_tasks_num = 0
        self.finished_tasks_num_lock = Lock()

        self.name = "sequential"
        self.containers = containers
        self.is_dy_alloc = is_dy_alloc

        self.time_start = 0
        self.finish_time_list = []
        self.record_interval = int(all_tasks_num * RECORD_INTERVAL)

    def add_task(self, task):
        with self.queue_lock:
            self.queue.put(task.get_command())

    def add_finished_tasks_num(self):
        with self.finished_tasks_num_lock:
            self.finished_tasks_num += 1
            if self.finished_tasks_num % self.record_interval == 0:
                self.finish_time_list.append(int(time() - self.time_start))
            return self.finished_tasks_num

    def get_name(self):
        return self.name

    def get_finished_tasks_num(self):
        # read need't a lock
        return self.finished_tasks_num

    # only for testing
    def get_all_tasks(self):
        with self.queue_lock:
            while not self.queue.empty():
                print(self.queue.get())

    def get_next_task(self):
        # get task when has a lock
        with self.queue_lock:
            if not self.queue.empty():
                cur_task = self.queue.get()
                return cur_task, self.add_finished_tasks_num()
        return None, None
    
    def run_container(self, C):
        print("Info: " + C + " is running...")
        while self.get_finished_tasks_num() < self.all_tasks_num:
            # judge if available
            is_available = False
            with open (cpu_log_file, "r") as file:
                line = file.readline()
                while line:
                    container_info = line.split(",")
                    name = container_info[0]
                    # container name matched
                    if name == C:
                        cpu_perc = float(container_info[2][:-2]) / 100
                        if cpu_perc < AVAIALBLE_THRESHOLD:  # success
                            is_available = True
                        break
                    line = file.readline()
            # distribute task only if container is availble
            if not is_available:
                continue
            T, T_id = self.get_next_task()
            if T:
                cmd = "docker exec " + C + " " + T
                print("Info: " + C + " get task " + str(T_id) + ": " + T)
                os.system(cmd)
        print("Info: " + C + " stop.")
        

    def run(self):
        self.time_start = time()
        try:
            threads = []
            for C in self.containers:
                t = threading.Thread(target=self.run_container, args=(C,))
                t.start()
                threads.append(t)
            print(threads)
            for t in threads:
                t.join()
        except:
            print("Error: unable to start thread")
        time_end = time()
        latency = round(time_end - self.time_start, 3)
        print("Info: Total latency: "+ str(latency))
        # container_num, scheduler, is_dy, latency
        info = str(len(self.containers)) + "," + self.name + "," + str(self.is_dy_alloc) + "," + str(latency)
        os.system("echo " + info + " >> " + latency_record)
        info = (",").join(str(x) for x in self.finish_time_list)
        os.system("echo " + info + " >> " + time_record)
        return latency


class PriorityScheduler(Scheduler):
    def __init__(self, all_tasks_num, containers, is_dy_alloc) -> None:
        self.queue = PriorityQueue()
        self.queue_lock = Lock()
        self.all_tasks_num = all_tasks_num
        self.finished_tasks_num = 0
        self.finished_tasks_num_lock = Lock()

        self.name = "priority"
        self.containers = containers
        self.is_dy_alloc = is_dy_alloc

        self.time_start = 0
        self.finish_time_list = []
        self.record_interval = int(all_tasks_num * RECORD_INTERVAL)

    def add_task(self, task):
        with self.queue_lock:
            self.queue.put((task.get_priority(), task.get_command()))

    # only for testing
    def get_all_tasks(self):
        with self.queue_lock:
            while not self.queue.empty():
                cur_task = self.queue.get()
                print(cur_task[1])

    def get_next_task(self):
        with self.queue_lock:
            if not self.queue.empty():
                cur_task = self.queue.get()
                return cur_task[1], self.add_finished_tasks_num()
        return None, None


class ML_Scheduler(Scheduler):
    def __init__(self, all_tasks_num, containers, is_dy_alloc) -> None:
        self.queue = []
        self.queue_lock = Lock()
        self.all_tasks_num = all_tasks_num
        self.finished_tasks_num = 0
        self.finished_tasks_num_lock = Lock()

        self.name = "machine_learning"
        self.containers = containers
        self.is_dy_alloc = is_dy_alloc

        self.group_size = GROUP_SIZE
        self.counter = 0
        self.period = REGROUP_PERIOD    # the period to regroup tasks

        self.time_start = 0
        self.finish_time_list = []
        self.record_interval = int(all_tasks_num * RECORD_INTERVAL)

    def add_task(self, task):
        with self.queue_lock:
            self.queue.append(task.get_func())
            self.counter += 1
            if self.counter == self.period:
                print("Info: ml_scheduler is scheduling...")
                self.regroup()
                self.counter = 0
                print("Info: ml_scheduler finished.")

    def get_next_task(self):
        with self.queue_lock:
            if len(self.queue) > 0:
                cur_task = self.queue.pop(0)
                return parse_cmd(functions[cur_task[0]], cur_task[1:]), self.add_finished_tasks_num()
        return None, None

    def get_IPC(self, func1, func2):
        if func1[0] > func2[0]:
            tmp = func1.copy()
            func1 = func2.copy()
            func2 = tmp
        # print("func1: " + str(func1) + "  func2: " + str(func2))
        train_dataset = pd.read_csv("./record/data/%d_%d.csv" % (func1[0], func2[0]))
        cols = list(train_dataset.columns)
        rows = train_dataset.shape[0]

        # reshape: change string type to int type
        train = train_dataset.loc[:, cols[:-1]]     # use loc to copy a dataframe, instead of train_dataset[cols[:-1]]
        regex = re.compile(r'\d+')
        for col_name in cols[:-1]:
            # print(type(train[col_name].iloc[0])) # loc: only string type can be used, iloc: only integer type can be used
            if type(train[col_name].iloc[0]) != np.int64:
                tmp2 = np.zeros(train.shape[0])
                for row in range(rows):
                    tmp2[row] = int(regex.findall(str(train[col_name].iloc[row]))[0])
                train.loc[:, (col_name)] = tmp2

        # use training data to standardize
        sc = StandardScaler()
        sc.fit(train)
        test = pd.DataFrame([func1[1:]+func2[1:]], columns=train.columns)
        test_std = sc.transform(test)

        model = jb.load(model_basic_path + "%d_%d.pk" % (func1[0], func2[0]))
        predict_IPC = model.predict(test_std)
        
        return predict_IPC

    # use IPC to regroup the tasks
    def regroup(self):
        # don't adjust when there are few tasks
        # don't need a lock because "add task" has done it 
        if len(self.queue) < self.group_size:
            return
        max_IPC = 0
        max_IPC_func1 = None
        max_IPC_func2 = None
        for i in range(self.group_size - 1):
            for j in range(i + 1, self.group_size):
                tmp_IPC = self.get_IPC(self.queue[i], self.queue[j])
                if tmp_IPC > max_IPC:
                    max_IPC = tmp_IPC
                    max_IPC_func1 = self.queue[i].copy()
                    max_IPC_func2 = self.queue[j].copy()
        self.queue.remove(max_IPC_func1)
        self.queue.remove(max_IPC_func2)
        self.queue.insert(0, max_IPC_func1)
        self.queue.insert(0, max_IPC_func2)
        print("Info: Bring func1 " + str(max_IPC_func1) + " and func2 " + str(max_IPC_func2) + " to the front.")

if __name__ == "__main__":
    from utils import parse_cmd, functions, Task

    # tasks_list = [[6, 10], [8, 50], [8, 100], [9, 2867, 28], [1, 20], [4, 834], [1, 100], [1, 100], [6, 50], [10, 1]]
    # ss = Scheduler(10, ["container1", "container2"], False)
    # for task in tasks_list:
    #     ss.add_task(Task(task))

    # ss.run()

    tasks_list = [[6, 10], [8, 50], [8, 100], [9, 2867, 28], [1, 20], [4, 834], [1, 100], [1, 100], [6, 50], [10, 1]]
    ss = PriorityScheduler(10, ["container1", "container2"], 0)
    for task in tasks_list:
        ss.add_task(Task(task))

    # ss.run()

    # tasks_list = [[6, 10], [8, 50], [8, 100], [9, 2867, 28], [1, 20], [4, 834], [1, 100], [1, 100], [6, 50], [10, 1]]
    # ss = ML_Scheduler(10, ["container1", "container2"], 0)
    # for task in tasks_list:
    #     ss.add_task(Task(task))

    ss.run()
