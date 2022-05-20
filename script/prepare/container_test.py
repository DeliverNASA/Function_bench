from itertools import count
import os
from multiprocessing import Process
import re

def create_container(name, cpu_period, cpu_quota):
    cmd = "docker run -itd -v \"$(pwd):/usr/local/\" -v \"/usr/local/lib/python3.8/dist-packages:/usr/local/lib/python3.8/dist-packages\" --cpuset-cpus 0 --cpu-period " + str(cpu_period) + " --cpu-quota " + str(cpu_quota) + " --name " + name + " blueddocker/ubuntu"
    os.system(cmd)

def remove_container():
    cmd = "docker rm -f $(docker ps -aq)"
    os.system(cmd)


def perf_monitor():
    print("perf start...")
    os.system("perf stat -e instructions,cycles  -C 0 -o ./record/container/tmp.txt sleep 5")
    print("perf finish.")


def exec_container(container, command):
    print(container + " start...")
    cmd = "docker exec " + container + " " + command
    os.system(cmd)
    print(container + " finish.")


if __name__ == "__main__":
    counter = 0
    for i in range(100000, 1100000, 100000):
        for j in range(i, 1100000, 100000):
            counter += 1
            print("task %d begin:" % counter)
            print("container1: " + str(i/1000000) + " container2: " + str(j/1000000))
            # create container
            create_container("container1", 1000000, i)
            create_container("container2", 1000000, j)
            # create multiple processes
            p1 = Process(target=exec_container, args=("container1", "python3 ./script/test/test_all.py",))
            p2 = Process(target=exec_container, args=("container2", "python3 ./script/test/test_all.py",))
            p3 = Process(target=perf_monitor,)
            # start running
            p1.start()
            p2.start()
            p3.start()
            # wait
            p1.join()
            p2.join()
            p3.join()
            # remove container
            remove_container()


            # read the specific line
            ips_line = 6
            file = open("./record/container/tmp.txt", "r")
            count = 0
            while count < ips_line:
                line = file.readline()
                count += 1
            # print(line)

            # event: instructions
            regex = re.compile(r'\d+')
            nums = regex.findall(line)
            instructions = 0
            for num in nums[:-2]:
                instructions = instructions * 1000 + int(num)
            # print(instructions)

            # event: cycles
            line = file.readline()
            nums = regex.findall(line)
            cycles = 0
            for num in nums:
                cycles = cycles * 1000 + int(num)
            # print(cycles)

            file.close()

            # save instructions per cycle (IPC)
            ans = instructions / cycles
            info = str(i/1000000) + "，" + str(i/1000000) + "，" + str(round(ans, 4))
            print(info)
            os.system("echo " + info + " >> ./record/container/ans.csv")

            print("task %d finish." % counter)
            print()
