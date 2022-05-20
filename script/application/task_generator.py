import random

functions = ["chameleon", "feature_extractor", "float_operation", "image_processing", "linpack", "matmul",
            "ml_lr_prediction", "ml_video_face_detection", "model_training", "pyaes", "video_processing"]


func_range = {}
# continuous variable
func_range["chameleon"] = [20, 2000]
func_range["float_operation"] = [200000, 2000000]
func_range["image_processing"] = [1, 9]
func_range["linpack"] = [100, 3000]
func_range["matmul"] = [100, 3000]
# discrete variable
func_range["feature_extractor"] = [10, 20, 50, 100]
func_range["ml_lr_prediction"] = [10, 20, 50, 100]
func_range["model_training"] = [10, 20, 50, 100]
func_range["video_processing"] = [1]
# double variable
func_range["pyaes_length_of_message"] = [256, 4096]
func_range["pyaes_num_of_iterations"] = [16, 128]


def generate_task(num, specify=False, specify_func=-1):
    task_num = num
    task_list = []
    while len(task_list) < task_num:
        if not specify:
            func_num = random.randint(0, 10)
            # abandon function "ml_video_face_detection"
            while func_num == 7:
                func_num = random.randint(0, 10)
        else:
            func_num = specify_func

        func_name = functions[func_num]
        if func_name == "pyaes":
            arg1 = random.randint(func_range["pyaes_length_of_message"][0], func_range["pyaes_length_of_message"][1])
            arg2 = random.randint(func_range["pyaes_num_of_iterations"][0], func_range["pyaes_num_of_iterations"][1])
            task_list.append([func_num, arg1, arg2])
            # print(func_name + " " + str(arg1) + " " + str(arg2))
        elif func_name in ["feature_extractor", "ml_lr_prediction", "model_training", "video_processing"]:
            arg1 = func_range[func_name][random.randint(0, len(func_range[func_name])-1)]
            task_list.append([func_num, arg1])
            # print(func_name + " " + str(arg1))
        else:
            arg1 = random.randint(func_range[func_name][0], func_range[func_name][1])
            task_list.append([func_num, arg1])
            # print(func_name + " " + str(arg1))

    return task_list

if __name__ == "__main__":
    generate_task(4)