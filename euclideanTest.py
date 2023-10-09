from PIL import Image, ImageFilter
from zipf.factories import ZipfFromList
from dictances import *


def get_zipf(image_link):
    colors = []
    image = Image.open(image_link)
    image = image.convert("L")
    image = image.filter(ImageFilter.FIND_EDGES)

    width, height = image.size

    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            colors.append(pixel)

    my_factory = ZipfFromList()
    my_zipf = my_factory.run(colors)

    return my_zipf


a = get_zipf(r"tree.jpeg")
b = get_zipf(r"Landscape-Color.jpeg")

distance = euclidean(a, b)
print("Euclidean Distance: ", distance)
