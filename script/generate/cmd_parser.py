# import argparse

# parser = argparse.ArgumentParser()

# # function name
# parser.add_argument('-f', type=str, default="chamelon")
# # chameleon
# parser.add_argument('-num_of_rows', type=str, default="400")
# parser.add_argument('-num_of_cols', type=str, default="400")
# # float_operation & linpack & matmul
# parser.add_argument('-n', type=str, default="1000000")
# # feature_extractor & image_processing & ml_video_face_detection & video_processing
# parser.add_argument('-object_key', type=str, default="")
# # ml_lr_prediction
# parser.add_argument('-dataset_train_object_key', type=str, default="reviews10mb.csv")
# parser.add_argument('-dataset_test_object_key', type=str, default="reviews20mb.csv")
# # model_training
# parser.add_argument('-dataset_object_key', type=str, default="reviews10mb.csv")
# # pyaes
# parser.add_argument('-length_of_message', type=str, default="1024")
# parser.add_argument('-num_of_iterations', type=str, default="32")

# parser.add_argument('-f1', type=str, default="")
# parser.add_argument('-f1_arg1', type=str, default="")
# parser.add_argument('-f1_arg2', type=str, default="")
# parser.add_argument('-f2', type=str, default="")
# parser.add_argument('-f2_arg1', type=str, default="")
# parser.add_argument('-f2_arg2', type=str, default="")

# args = parser.parse_args()


# store arguments of functions
func_args = dict()

func_args["chameleon"] = ["num_of_row_col"]

func_args["float_operation"] = ["n"]
func_args["linpack"] = ["n"]
func_args["matmul"] = ["n"]

func_args["feature_extractor"] = ["object_key"]
func_args["image_processing"] = ["object_key"]
func_args["ml_video_face_detection"] = ["object_key"]
func_args["video_processing"] = ["object_key"]

func_args["ml_lr_prediction"] = ["dataset_test_object_key"]

func_args["model_training"] = ["dataset_object_key"]

func_args["pyaes"] = ["length_of_message", "num_of_iterations"]




def handle_args(func_name, args):
    # print(func_name)
    # print(arg1)
    # print(arg2)
    # chameleon
    if func_name == "chameleon":
        arguments = "-num_of_rows=" + str(args) + " -num_of_cols=" + str(args)
    # float_operation & linpack & matmul
    elif func_name == "float_operation" or func_name == "linpack" or func_name == "matmul":
        arguments = "-n=" + str(args)
    # feature_extractor & image_processing & ml_video_face_detection & video_processing
    elif func_name == "feature_extractor" or func_name == "image_processing" or func_name == "ml_video_face_detection" or func_name == "video_processing":
        arguments = "-object_key=" + str(args)
    # ml_lr_predictio
    elif func_name == "ml_lr_prediction":
        # arguments = "-dataset_train_object_key=" + str(args[0]) + " -dataset_test_object_key=" + str(args[1])
        arguments = "-dataset_test_object_key=" + str(args)
    # model_training
    elif func_name == "model_training":
        arguments = "-dataset_object_key=" + str(args)
    # pyaes
    elif func_name == "pyaes":
        arguments = "-length_of_message=" + str(args[0]) + " -num_of_iterations=" + str(args[1])
    # none    
    else:
        arguments = ""
    
    return arguments


def parse_cmd(f1, f1_args, f2, f2_args):
    cmd1 = "python3 ./aws/cpu-memory/" + f1 + "/lambda_function.py " + handle_args(f1, f1_args)
    cmd2 = "python3 ./aws/cpu-memory/" + f2 + "/lambda_function.py " + handle_args(f2, f2_args)

    return [cmd1, cmd2]