from time import sleep
import sys
import os
import threading


sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))
print(sys.path)
from schedulers.utils import Task
from schedulers.scheduler import Scheduler, PriorityScheduler, ML_Scheduler
from allocators.allocator import Dynamic_allocator


task_path = "./script/application/log/task_"
ALL_TASKS_NUM = 100

# dynamic allocator
PERIOD = 5
STEP = 100000 
MIN_CPU_UTILIZATION=0.1
MAX_CPU_UTILIZATION=0.9

class Simulater():
    def __init__(self, task_num, scheduler) -> None:
        self.task_num = task_num
        self.scheduler = scheduler

    def run_task_manager(self):
        tasks_list = []
        with open(task_path + str(self.task_num) + ".txt", "r") as f:
            for i in range(self.task_num):
                task = f.readline().strip('\n').split(",")
                tmp_l = []
                for i in range(1, len(task)):
                    tmp_l.append(int(task[i]))
                tasks_list.append([float(task[0]), tmp_l])
        # print(tasks_list)

        last_time = 0
        while len(tasks_list) > 0:
            task_info = tasks_list.pop(0)
            print(task_info)
            time_len = float(task_info[0]) - last_time
            # waiting for task's arrival
            sleep(time_len)
            last_time = float(task_info[0])
            self.scheduler.add_task(Task(task_info[1]))    # task arrived

    def run(self):
        t1 = threading.Thread(target=self.run_task_manager, args=(),)
        t2 = threading.Thread(target=self.scheduler.run, args=(),)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
            
if __name__ == "__main__":
    os.system("taskset -pc 1-7 " + str(os.getpid()))

    da = Dynamic_allocator(period=PERIOD, step=STEP, min_cpu_utilization=MIN_CPU_UTILIZATION, max_cpu_utilization=MAX_CPU_UTILIZATION)
    
    con_list= [1, 2]
    sd_list = ["sequential", "priority", "machine_learning"]
    da_list = [False, True]
    
    flag_turn_on_dy_alloc = False

    for da_op in da_list:
        if not flag_turn_on_dy_alloc and da_op:
            t_da = threading.Thread(target=da.run, args=(),)
            t_da.start()
        for con in con_list:
            os.system("sh ./script/prepare/" + str(da) + "container.sh")

            # create container list
            if con == 1:
                containers = ["container1"]
            else:
                containers = ["container1", "container2"]

            for sd in sd_list:
                if sd == "sequential":
                    S = Scheduler(ALL_TASKS_NUM, containers, da_op)
                elif sd == "priority":
                    S = PriorityScheduler(ALL_TASKS_NUM, containers, da_op)
                elif sd == "machine_learning":
                    S = ML_Scheduler(ALL_TASKS_NUM, containers, da_op)
                SIMU = Simulater(ALL_TASKS_NUM, S)
                SIMU.run()

            os.system("sh ./script/prepare/rm_container.sh")