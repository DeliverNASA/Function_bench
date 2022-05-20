from task_generator import generate_task, functions
from scheduler import scheduler
from cmd_parser2 import parse_cmd
from multiprocessing import Process
from time import sleep, time

import random
import os


task_num = 6
case_num = 20
masks = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]

def exec_container(container, command):
    # print(container + " start...")
    cmd = "docker exec " + container + " " + command
    os.system(cmd)
    # print(container + " finish.")


def record_time(commands, order):
    total_time = 0
    for group_id in range(int(task_num / 2)):
        # create multiple processes
        # print()
        # print(commands[order[2*group_id]])
        # print(commands[order[2*group_id+1]])
        p1 = Process(target=exec_container, args=("container1", commands[order[2*group_id]]),)
        p2 = Process(target=exec_container, args=("container2", commands[order[2*group_id+1]]),)
        # start running
        start_time = time()
        p1.start()
        p2.start()
        # wait
        p1.join()
        p2.join()
        latency = time() - start_time
        total_time += latency
    return total_time


if __name__ == "__main__":
    # single function
    for func_id in range(len(functions)):
        if masks[func_id]:
            continue
        for i in range(case_num):
            task_list = generate_task(task_num, specify=True, specify_func=func_id)
            print("case " + str(i) + ": " + str(task_list))
            commands = []
            for task in task_list:
                commands.append(parse_cmd(functions[task[0]], task[1:]))

            # sequential combination & random combination & scheduler's combination
            sequential_combination = [i for i in range(task_num)]
            random_combination = sequential_combination.copy()
            random.shuffle(random_combination)
            scheduler_combination = scheduler(task_list)

            # os.system("echo sequential,random,scheduler >> ./record/result/all.csv")
            times = []
            print("scheduler_combination: " + str(scheduler_combination))
            times.append(record_time(commands, scheduler_combination))
            print("sequential_combination: " + str(sequential_combination))
            times.append(record_time(commands, sequential_combination))
            print("random_combination: " + str(random_combination))
            times.append(record_time(commands, random_combination))
            info = str(times[0]) + "," + str(times[1]) + "," + str(times[2])
            print(info)
            # os.system("echo " + info + " >> ./record/result/all.csv")
            os.system("echo " + info + " >> ./record/result/" + functions[func_id] + ".csv")