from PIL import Image
import threading

image_size = range(2000, 23000, 1000)

def make_image(size, id):
    origin = Image.open("./dataset/image/dog.jpg")
    origin.resize((int(size * 1.5), size), Image.ANTIALIAS).save("./dataset/image/dog_%d.jpg" % id)


if __name__ == "__main__":
    length = len(image_size)
    for i in range(length):
        make_image(image_size[i], i + 1)