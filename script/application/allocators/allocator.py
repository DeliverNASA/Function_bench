import threading 
import time
import os


cpu_log_file = "./script/application/log/cpu.txt"
docker_basic_path = "/sys/fs/cgroup/cpu/docker/"
MAX_QUOTA = 1000000
MIN_QUOTA = 100000

CPU_PERIOD = 1000000


def transform_perc(percentage):
    percentage = percentage[:-2]
    return float(percentage) / 100

class Dynamic_allocator():
    def __init__(self, period, step, min_cpu_utilization, max_cpu_utilization) -> None:
        self.period = period
        self.step = step
        self.min_cpu_utilization = min_cpu_utilization
        self.max_cpu_utilization = max_cpu_utilization
    def run(self):
        os.system("taskset -pc 1-7 " + str(os.getpid()))
        while True:
            # collect data once in a period
            time.sleep(self.period)
            print("Info: pid " + str(os.getpid()) + " dynamic allocator start analysing...")
            # analysis
            with open(cpu_log_file, "r") as file:
                line = file.readline()
                while line:
                    container_info = line.split(",")
                    name = container_info[0]
                    id = container_info[1]
                    cpu_perc = transform_perc(container_info[2])
                    container_path = docker_basic_path + id + "/cpu.cfs_quota_us"

                    file2 = open(container_path, "r")
                    cur_quota = int(file2.readline())
                    print("Info: " + name + "\'s cpu usage: " + str(cpu_perc))
                    # need more cpu resource
                    if cpu_perc > (self.max_cpu_utilization * (float(cur_quota) / CPU_PERIOD)):
                        if cur_quota + self.step < MAX_QUOTA:
                            cmd = "echo " + str(cur_quota + self.step) + " > " + container_path
                            print(cmd)
                            os.system(cmd)
                            print("Info: dynamic allocator increase " + name + "'s quota to " + str(cur_quota + self.step))
                    # don't need some cpu resource
                    elif cpu_perc < (self.min_cpu_utilization * (float(cur_quota) / CPU_PERIOD)):
                        if cur_quota - self.step > MIN_QUOTA:
                            cmd = "echo " + str(cur_quota - self.step) + " > " + container_path
                            print(cmd)
                            os.system(cmd)
                            print("Info: dynamic allocator decrease " + name + "'s quota to " + str(cur_quota - self.step))
                    line = file.readline()
            print("Info: dynamic allocator finish the work.")
            


if __name__ == "__main__":
    thread1 = Dynamic_allocator(period=5, step=100000, min_cpu_utilization=0.1, max_cpu_utilization=0.9)
    thread1.run()