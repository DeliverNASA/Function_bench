from itertools import count
import os
from multiprocessing import Process
from cmd_parser import parse_cmd

print('Process (%s) start...' % os.getpid())

def perf_monitor():
    os.system("perf stat")

def exec_container(container, command):
    print(container + ": Start executing commands...")
    cmd = "docker exec " + container + command
    os.system(cmd)
    print(container + ": Finish.")


functions = ["chameleon", "feature_extractor", "float_operation", "image_processing", "linpack", "matmul",
            "ml_lr_prediction", "ml_video_face_detection", "model_training", "pyaes", "video_processing"]
masks = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

args_chameleon = [i for i in range(100, 1010, 20)]
args_feature_extractor = ["reviews10mb.csv", "reviews20mb.csv", "reviews50mb.csv", "reviews100mb.csv"]
args_float_peration = [i for i in range(200000, 2000000, 100000)]
args_image_processing = ["dog_%d" % i for i in range(1, 21)]
args_linpack = [i for i in range(500, 2100, 100)]
args_matmul = [i for i in range(500, 2100, 100)]
args_ml_lr_prediction_datasets = ["reviews10mb.csv", "reviews20mb.csv", "reviews50mb.csv", "reviews100mb.csv"]
# resize for two input arguments
args_ml_lr_prediction = [(i, j) for i in args_ml_lr_prediction_datasets for j in args_ml_lr_prediction_datasets]
args_video_face_detection = ["testVideo001.mp4"]
args_model_training = ["reviews10mb.csv", "reviews20mb.csv", "reviews50mb.csv", "reviews100mb.csv"]
args_pyaes_length_of_message = [i for i in range(256, 4197, 256)]
args_pyaes_num_of_iterations = [i for i in range(16, 65, 16)]
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
args.append(args_ml_lr_prediction)
args.append(args_video_face_detection)
args.append(args_model_training)
args.append(args_pyaes)
args.append(args_video_processing)

if __name__ == "__main__":
    # p1 = Process(target=exec_container,)
    # p2 = Process(target=exec_container,)
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
    # print("main")
    length = len(functions)
    counter = 1
    for f1_id in range(length):
        # skip the abandoned function
        if masks[f1_id]:
            continue

        for f2_id in range(f1_id, length):
            # skip the abandoned function
            if masks[f2_id]:
                continue
            f1 = functions[f1_id]
            f2 = functions[f2_id]
            len_f1_args = len(args[f1_id])
            len_f2_args = len(args[f2_id])

            for i in range(len_f1_args):
                if f1_id != f2_id:  start = 0
                else: start = i

                for j in range(start, len_f2_args):
                    commands = parse_cmd(f1, args[f1_id][i], f2, args[f2_id][j])
                    # show command info
            print(counter)
            counter += 1
            print(commands[0])
            print(commands[1])
            print()
                    # # create multiple processes
                    # p1 = Process(target=exec_container, args=("container1", commands[0]),)
                    # p2 = Process(target=exec_container, args=("container2", commands[1]),)
                    # p3 = Process(target=perf_monitor,)
                    # # start running
                    # p1.start()
                    # p2.start()
                    # p3.start()
                    # # wait
                    # p1.join()
                    # p2.join()
                    # p3.join()


    # print(args)
    os.system("perf stat --")
    os.system("python3 ./test_scripts/aws/cpu-memory/linpack/lambda_function.py -n=2000")
    os.system("python3 ./test_scripts/aws/cpu-memory/ml_lr_prediction/lambda_function.py -dataset_train_object_key=reviews100mb.csv -dataset_test_object_key=reviews100mb.csv")