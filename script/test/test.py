# from dataclasses import field
# import os
# from multiprocessing import Process
# from re import L
# from time import sleep
# import re

# def perf_monitor():
#     os.system("perf stat -e instructions,cycles  -C 0 -o ./record/tmp.txt sleep 5")
#     # perf stat -I 1000 -e cycles -a sleep 5

# def exec_container(container, command):
#     print(container + ": Start executing commands...")
#     cmd = "docker exec " + container + " " + command
#     print(cmd)
#     os.system(cmd)
#     print(container + ": Finish.")


# if __name__ == "__main__":
#     # create processes
#     p1 = Process(target=exec_container, args=("container1", "python3 ./aws/cpu-memory/linpack/lambda_function.py -n=2000"),)
#     p2 = Process(target=exec_container, args=("container2", "python3 ./aws/cpu-memory/ml_lr_prediction/lambda_function.py -dataset_train_object_key=reviews10mb.csv -dataset_test_object_key=reviews20mb.csv"),)
#     p3 = Process(target=perf_monitor,)
#     # start running
#     p1.start()
#     p2.start()
#     p3.start()
#     # wait
#     p1.join()
#     p2.join()
#     p3.join()
#     print("Process finish.")

#     # read the specific line
#     ips_line = 6
#     file = open("./record/tmp.txt", "r")
#     count = 0
#     while count < ips_line:
#         line = file.readline()
#         count += 1
#     print(line)

#     # find the number
#     regex = re.compile(r'\d+')
#     nums = regex.findall(line)
#     instructions = 0
#     for num in nums[:-2]:
#         print(num)
#         instructions = instructions * 1000 + int(num)
#     print(instructions)

#     line = file.readline()
#     nums = regex.findall(line)
#     cycles = 0
#     for num in nums:
#         cycles = cycles * 1000 + int(num)
#     print(cycles)


#     ans = instructions / cycles
#     # write as a record
#     info = "n,train,test,ipc"
#     os.system("echo " + info + " >> ./record/5_7.csv")
#     info = "2000,10,20," + str(round(ans, 4))
#     os.system("echo " + info + " >> ./record/5_7.csv")
    
#     # print("Record finish.")

# import multiprocessing
# import os
# import signal
# import time

# def func(i):
#     while True:
#         a = i
#         print("the {} dog".format(os.getpid()))
#         # array[0] = a
#         # a = i
        
    


# process_list = []

# for i in range(10):
#     process = multiprocessing.Process(target=func, args=(i,), daemon=False)
#     process_list.append(process)
#     process.start()
#     # time.sleep(0.2) #等待进程运行
    
#     # print(num)
#     # print(num_array[0])
    
# time.sleep(5)
# for process in process_list:
#     process.te


a = [[1,2], [3,4]]
b = []
b.append(a)
b.append(a)
a = []
print(b)