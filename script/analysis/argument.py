args_chameleon = [i for i in range(100, 1010, 40)]
args_feature_extractor = [10, 20, 50, 100]
args_float_peration = [i for i in range(200000, 2000000, 100000)]
args_image_processing = [i for i in range(1, 10)]
args_linpack = [i for i in range(500, 2100, 100)]
args_matmul = [i for i in range(500, 2100, 100)]
args_ml_lr_prediction_datasets = [10, 20, 50, 100]
# resize for two input arguments
# args_ml_lr_prediction = [(i, j) for i in args_ml_lr_prediction_datasets for j in args_ml_lr_prediction_datasets]
args_video_face_detection = [1]
args_model_training = [10, 20, 50, 100]
args_pyaes_length_of_message = [i for i in range(512, 2049, 512)]
args_pyaes_num_of_iterations = [i for i in range(32, 65, 16)]
# resize for two input arguments
args_pyaes = [(i, j) for i in args_pyaes_length_of_message for j in args_pyaes_num_of_iterations]
args_video_processing = [1]

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

functions = ["chameleon", "feature_extractor", "float_operation", "image_processing", "linpack", "matmul",
            "ml_lr_prediction", "ml_video_face_detection", "model_training", "pyaes", "video_processing"]