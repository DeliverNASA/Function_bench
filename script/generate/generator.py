from itertools import count
import os
from multiprocessing import Process
from cmd_parser import parse_cmd, func_args
import re

print('Process (%s) start...' % os.getpid())

def perf_monitor():
    print("perf start...")
    os.system("perf stat -e instructions,cycles  -C 0 -o ./record/tmp.txt sleep 5")
    print("perf finish.")


def exec_container(container, command):
    print(container + " start...")
    cmd = "docker exec " + container + " " + command
    os.system(cmd)
    print(container + " finish.")


def show_args(datas):
    info = ""
    if type(datas) == tuple:
        for data in datas:
            print(data)
            info = info + str(data) + ","
    else:
        info = info + str(datas) + ","
    return info


# unused: ml_video_face_detection
functions = ["chameleon", "feature_extractor", "float_operation", "image_processing", "linpack", "matmul",
            "ml_lr_prediction", "ml_video_face_detection", "model_training", "pyaes", "video_processing"]
masks = [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0]
# masks1 = [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
# masks2 = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]



args_chameleon = [i for i in range(100, 1010, 40)]
args_feature_extractor = ["reviews10mb.csv", "reviews20mb.csv", "reviews50mb.csv", "reviews100mb.csv"]
args_float_peration = [i for i in range(200000, 2000000, 100000)]
args_image_processing = ["dog_%d.jpg" % i for i in range(1, 10)]
args_linpack = [i for i in range(500, 2100, 100)]
args_matmul = [i for i in range(500, 2100, 100)]
args_ml_lr_prediction_datasets = ["reviews10mb.csv", "reviews20mb.csv", "reviews50mb.csv", "reviews100mb.csv"]
# resize for two input arguments
# args_ml_lr_prediction = [(i, j) for i in args_ml_lr_prediction_datasets for j in args_ml_lr_prediction_datasets]
args_video_face_detection = ["testVideo001.mp4"]
args_model_training = ["reviews10mb.csv", "reviews20mb.csv", "reviews50mb.csv", "reviews100mb.csv"]
args_pyaes_length_of_message = [i for i in range(512, 2049, 512)]
args_pyaes_num_of_iterations = [i for i in range(32, 65, 16)]
# resize for two input arguments
args_pyaes = [(i, j) for i in args_pyaes_length_of_message for j in args_pyaes_num_of_iterations]
args_video_processing = ["testVideo001.mp4"]

args = list()
args.append(args_chameleon)
args.append(args_feature_extractor)
args.append(args_float_peration)
args.append(args_image_processing)
args.append(args_linpack)
args.append(args_matmul)
args.append(args_ml_lr_prediction_datasets)
args.append(args_video_face_detection)
args.append(args_model_training)
args.append(args_pyaes)
args.append(args_video_processing)

if __name__ == "__main__":
    # create containers
    # os.system("sh ./script/create_container.sh")

    length = len(functions)
    counter = 0

    for f1_id in range(length):
        # skip the abandoned function
        if masks[f1_id]:
            continue

        for f2_id in range(f1_id + 1, length):
            # skip the abandoned function
            if masks[f2_id]:
                continue
            f1 = functions[f1_id]
            f2 = functions[f2_id]
            len_f1_args = len(args[f1_id])
            len_f2_args = len(args[f2_id])
            
            # create a record file
            info = ""
            for key in func_args[f1]:  info = info + "f1_" + key + ","
            for key in func_args[f2]:  info = info + "f2_" + key + ","
            info += "ipc"
            os.system("echo " + info + " >> ./record/%d_%d.csv" % (f1_id, f2_id))

            for i in range(len_f1_args):
                # avoid repeating
                if f1_id != f2_id:  start = 0
                else: start = i

                for j in range(start, len_f2_args):
                    commands = parse_cmd(f1, args[f1_id][i], f2, args[f2_id][j])
                    # show command info
                    counter += 1
                    print("task %d: " % counter + str(args[f1_id][i]) + " " + str(args[f2_id][j]))
                    print(commands[0])
                    print(commands[1])
                    # print()

                    # create multiple processes
                    p1 = Process(target=exec_container, args=("container1", commands[0]),)
                    p2 = Process(target=exec_container, args=("container2", commands[1]),)
                    p3 = Process(target=perf_monitor,)
                    # start running
                    p1.start()
                    p2.start()
                    p3.start()
                    # wait
                    p1.join()
                    p2.join()
                    p3.join()

                    # read the specific line
                    ips_line = 6
                    file = open("./record/data/tmp.txt", "r")
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

                    # save instructions per cycle (IPC)
                    ans = instructions / cycles
                    info = show_args(args[f1_id][i]) + show_args(args[f2_id][j])
                    info += str(round(ans, 4))
                    os.system("echo " + info + " >> ./record/data/%d_%d.csv" % (f1_id, f2_id))

                    print("task %d finish." % counter)
                    print()
