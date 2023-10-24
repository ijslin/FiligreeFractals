# This version uses PIL

from PIL import Image, ImageFilter
from zipf import *
from math import *


def count_shades(image):
    histogram = {}
    shades = []
    width, height = image.size

    for y in range(height):
        for x in range(width):
            shade = image.getpixel((x, y))
            shades.append(shade)

    for shade in shades:
        histogram[shade] = histogram.get(shade, 0) + 1

    return histogram


def get_image(link):
    image = Image.open(link)
    image = image.convert("L")
    image = image.filter(ImageFilter.FIND_EDGES)
    return image


def get_quadrants(image):
    width, height = image.size

    tuple1 = (0, 0, (width / 2), (height / 2))
    tuple2 = ((width / 2), 0, (width - 1), (height / 2))
    tuple3 = (0, (height / 2), (width / 2), (height - 1))
    tuple4 = ((width / 2), (height / 2), (width - 1), (height - 1))

    quad1 = image.crop(tuple1)
    quad2 = image.crop(tuple2)
    quad3 = image.crop(tuple3)
    quad4 = image.crop(tuple4)

    return quad1, quad2, quad3, quad4


def get_zipf_color(image):
    image = image.convert("L")
    image = image.filter(ImageFilter.FIND_EDGES)

    histogram = count_shades(image)
    counts = list(histogram.values())

    slope, r2, yint = byRank(counts)

    return slope, r2


def get_zipf_gray_edge(image):
    histogram = count_shades(image)
    counts = list(histogram.values())

    slope, r2, yint = byRank(counts)

    return slope, r2


def euclidean(a, b):
    result = 0

    if len(a) == len(b) & len(a) == 2:
        dx = b[0] - a[0]
        dy = b[1] - a[1]

        sum = (dx * dx) + (dy * dy)

        result = sqrt(sum)
    else:
        sum = ((b[0][0] - a[0][0]) * (b[0][0] - a[0][0])) + (b[0][1] - a[0][1]) * (b[0][1] - a[0][1])

        for i in range(len(b)):
            sum = sum + ((b[i][0] - a[i][0]) * (b[i][0] - a[i][0])) + (b[i][1] - a[i][1]) * (b[i][1] - a[i][1])

        result = sqrt(sum)

    return result


def main():
    image1 = get_image(r"images/filigrees/C1-2r-Opening V-cropped.jpeg")
    image2 = get_image(r"images/filigrees/C1-2v & 4r-cropped.jpeg")
    a = get_zipf_gray_edge(image1)
    b = get_zipf_gray_edge(image2)

    print(a)
    print()
    print(b)
    print()
    print(euclidean(a, b))


main()
