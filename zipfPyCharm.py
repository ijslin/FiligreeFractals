# This version uses PIL

from PIL import Image, ImageFilter
from zipf import *
from math import *


def count_shades(image):
    histogram = {}
    shades = []
    width, height = image.size  # Gets the width and height of the image

    # Gets the shade value for each pixel and adds it to a list
    for y in range(height):
        for x in range(width):
            shade = image.getpixel((x, y))
            shades.append(shade)

    # For each shade in the list, it will add a key in the histogram and keep a count of how many times it occurs
    for shade in shades:
        histogram[shade] = histogram.get(shade, 0) + 1

    return histogram  # Returns a histogram object


def get_image(link):
    # Creates an image object using a raw string to find image in a directory
    image = Image.open(link)
    image = image.convert("L")  # Grayscales the image
    image = image.filter(ImageFilter.FIND_EDGES)  # Edge detects the image

    return image  # Returns the image object


def get_quadrants(image):
    width, height = image.size  # Gets the with and height of the image

    # To make the cropping statements neater and easier to edit during testing, tuple variables containing the left,
    # top, right, and bottom values are created
    tuple1 = (0, 0, (width / 2), (height / 2))
    tuple2 = ((width / 2), 0, (width - 1), (height / 2))
    tuple3 = (0, (height / 2), (width / 2), (height - 1))
    tuple4 = ((width / 2), (height / 2), (width - 1), (height - 1))

    # Crops the image four different times based on the above tuple to create the quadrants
    quad1 = image.crop(tuple1)
    quad2 = image.crop(tuple2)
    quad3 = image.crop(tuple3)
    quad4 = image.crop(tuple4)

    return quad1, quad2, quad3, quad4  # Returns the four quadrants as image objects


# This function is to get the slope and r2 for images that are in color, no longer necessary due to get_image
# grayscaling the image already
def get_zipf_color(image):
    image = image.convert("L")
    image = image.filter(ImageFilter.FIND_EDGES)

    histogram = count_shades(image)
    counts = list(histogram.values())

    slope, r2, yint = byRank(counts)

    return slope, r2


def get_zipf_gray_edge(image):
    histogram = count_shades(image)  # Creates a histogram using the image object
    counts = list(histogram.values())  # creates a list using the histogram values

    slope, r2, yint = byRank(counts)  # Organizes list by rank and returns the slope, r2, and yint of the image

    return slope, r2  # Returns only the slope and r2 as those are the only ones necessary for the Euclidean distance


def euclidean(a, b):
    result = 0  # Holds the Euclidean distance for return

    # This if is to check if the parameters are for only the whole image and no quadrants
    if len(a) == 2:
        dx = b[0] - a[0]
        dy = b[1] - a[1]

        sum = (dx * dx) + (dy * dy)

        result = sqrt(sum)
    else:  # This clause should run if quadrants are included
        sum = 0

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
