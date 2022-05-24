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
        arguments = "-num_of_rows=" + str(args[0]) + " -num_of_cols=" + str(args[0])
    # float_operation & linpack & matmul
    elif func_name == "float_operation" or func_name == "linpack" or func_name == "matmul":
        arguments = "-n=" + str(args[0])
    # feature_extractor 
    elif func_name == "feature_extractor":
        arguments = "-object_key=" + "reviews" + str(args[0]) + "mb.csv"
    # image_processing
    elif func_name == "image_processing":
        arguments = "-object_key=" + "dog_" + str(args[0]) + ".jpg"
    # ml_video_face_detection & video_processing
    elif func_name == "ml_video_face_detection" or func_name == "video_processing":
        arguments = "-object_key=" + "testVideo00" + str(args[0]) + ".mp4"
    # ml_lr_predictio
    elif func_name == "ml_lr_prediction":
        # arguments = "-dataset_train_object_key=" + str(args[0]) + " -dataset_test_object_key=" + str(args[1])
        arguments = "-dataset_test_object_key=" + "reviews" + str(args[0]) + "mb.csv"
    # model_training
    elif func_name == "model_training":
        arguments = "-dataset_object_key=" + "reviews" + str(args[0]) + "mb.csv"
    # pyaes
    elif func_name == "pyaes":
        arguments = "-length_of_message=" + str(args[0]) + " -num_of_iterations=" + str(args[1])
    # none    
    else:
        arguments = ""
    
    return arguments


def parse_cmd(f1, f1_args):
    cmd1 = "python3 ./aws/cpu-memory/" + f1 + "/lambda_function.py " + handle_args(f1, f1_args)

    return cmd1