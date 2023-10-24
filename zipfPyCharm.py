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


def euclidean(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    return sqrt((dx * dx) + (dy * dy))


def main():
    image1 = get_image(r"images/filigrees/C1-2r-Opening V-cropped.jpeg")
    image2 = get_image(r"images/filigrees/C1-2v & 4r-cropped.jpeg")
    a = get_zipf_gray_edge(image1)
    b = get_zipf_gray_edge(image2)

    print(a)
    print()
    print(b)
    print()
    print(euclidean(a[0], a[1], b[0], b[1]))


main()
