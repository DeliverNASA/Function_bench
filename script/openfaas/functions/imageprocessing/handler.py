import uuid
from time import time
from PIL import Image, ImageFilter

TMP = "./dataset/image_transform/"
def flip(image, file_name):
    path_list = []
    path = TMP + "flip-left-right-" + file_name
    img = image.transpose(Image.FLIP_LEFT_RIGHT)
    # img.save(path)
    # path_list.append(path)

    path = TMP + "flip-top-bottom-" + file_name
    img = image.transpose(Image.FLIP_TOP_BOTTOM)
    # img.save(path)
    # path_list.append(path)

    return path_list


def rotate(image, file_name):
    path_list = []
    path = TMP + "rotate-90-" + file_name
    img = image.transpose(Image.ROTATE_90)
    # img.save(path)
    # path_list.append(path)

    path = TMP + "rotate-180-" + file_name
    img = image.transpose(Image.ROTATE_180)
    # img.save(path)
    # path_list.append(path)

    path = TMP + "rotate-270-" + file_name
    img = image.transpose(Image.ROTATE_270)
    # img.save(path)
    # path_list.append(path)

    return path_list


def filter(image, file_name):
    path_list = []
    path = TMP + "blur-" + file_name
    img = image.filter(ImageFilter.BLUR)
    # img.save(path)
    # path_list.append(path)

    path = TMP + "contour-" + file_name
    img = image.filter(ImageFilter.CONTOUR)
    # img.save(path)
    # path_list.append(path)

    path = TMP + "sharpen-" + file_name
    img = image.filter(ImageFilter.SHARPEN)
    # img.save(path)
    # path_list.append(path)

    return path_list


def gray_scale(image, file_name):
    path = TMP + "gray-scale-" + file_name
    img = image.convert('L')
    # img.save(path)
    return [path]


def resize(image, file_name):
    path = TMP + "resized-" + file_name
    image.thumbnail((128, 128))
    # image.save(path)
    return [path]

def image_processing(file_name, image_path):
    path_list = []
    start = time()
    with Image.open(image_path) as image:
        tmp = image
        path_list += flip(image, file_name)
        path_list += rotate(image, file_name)
        path_list += filter(image, file_name)
        path_list += gray_scale(image, file_name)
        path_list += resize(image, file_name)

    latency = time() - start
    return latency, path_list

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    #event = json.loads(req)
    #input_path = event["input_path"]
    #object_key = event['object_key']

    # object key是转换后的图像名称
    # download_path是要转换的图像名称
    object_key = '{}.jpg'.format(uuid.uuid4())
    #download_path = '/tmp/{}{}'.format(uuid.uuid4(), object_key)
    download_path = "/home/app/function/test.jpg"

    #wget.download(input_path,  download_path)
    print(object_key)
    print(download_path)

    latency, path_list = image_processing(object_key, download_path)
    path_list.clear()
    #os.remove(download_path)
    # for file_path in path_list:
    #     os.remove(file_path)
    
    return latency


if(__name__ == "__main__"):
    # st = get_stdin()
    # ret = handler.handle(st)
    # if ret != None:
    #     print(ret)
    ret = handle(None)
    print(ret)