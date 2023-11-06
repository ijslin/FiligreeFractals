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
    tuple2 = ((width / 2), 0, width, (height / 2))
    tuple3 = (0, (height / 2), (width / 2), height)
    tuple4 = ((width / 2), (height / 2), width, height)

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
            dx = b[i][0] - a[i][0]
            dy = b[i][1] - a[i][1]
            sum = sum + ((dx * dx) + (dy * dy))

        result = sqrt(sum)

    return result


def recursive(image, list, depth):
    if depth == 0:
        list.append(get_zipf_gray_edge(image))
    else:
        quad1, quad2, quad3, quad4 = get_quadrants(image)
        recursive(quad1, list, depth - 1)
        recursive(quad2, list, depth - 1)
        recursive(quad3, list, depth - 1)
        recursive(quad4, list, depth - 1)

        list.append(get_zipf_gray_edge(image))


def recursive_test():
    image = get_image(r"images/test_images/recursive_test.jpeg")
    result = []
    recursive(image, result, 1)
    print("Recursive Output: ", result)

    image1 = get_image(r"images/test_images/billmanaris.jpeg")
    r1 = []
    recursive(image1, r1, 1)
    print("Arbitrary Image Zipf: ", r1[4])
    print("Top Left Quadrant Zipf: ", result[0])

    image2 = get_image(r"images/test_images/white-noise-1400x825.jpeg")
    r2 = []
    recursive(image2, r2, 1)
    print("White Noise Zipf: ", r2[4])
    print("Top Right Quadrant Zipf: ", result[1])

    image3 = get_image(r"images/test_images/plain-black-background-02fh7564l8qq4m6d.jpeg")
    r3 = []
    recursive(image3, r3, 1)
    print("Background with Blemish Zipf: ", r3[4])
    print("Bottom Left Quadrant Zipf: ", result[2])

    image4 = get_image(r"images/test_images/tree.jpeg")
    r4 = []
    recursive(image4, r4, 1)
    print("Tree Zipf: ", r4[4])
    print("Bottom Right Quadrant Zipf: ", result[3])


def same_author():
    links = [r"images/filigrees/Monaco/C1-2r-Opening V-cropped.jpg", r"images/filigrees/Monaco/C1-2v _ 4r-cropped.jpg",
             r"images/filigrees/Monaco/C1-16r-S w mandorla-croppedA.jpg",
             r"images/filigrees/Monaco/C1-16r-S w mandorla-croppedA.jpg",
             r"images/filigrees/Monaco/C1-19v-20r-Magdalene-cropped.jpg",
             r"images/filigrees/Monaco/C1-20v-21r-Magdanele hymn 2-cropped.jpg"]
    filigree1 = get_image(r"images/filigrees/Monaco/C1-2r-Opening V-cropped.jpg")
    links.remove(r"images/filigrees/Monaco/C1-2r-Opening V-cropped.jpg")

    print("Author: Monaco")
    test_number = 1

    for link in links:
        print("Test", test_number, ":")

        filigree2 = get_image(link)

        result1 = []
        result2 = []

        recursive(filigree1, result1, 1)
        recursive(filigree2, result2, 1)

        print("Filigree 1: ", result1)
        print("Filigree 2: ", result2)

        print("Euclidean Distance: ", euclidean(result1, result2))
        test_number += 1
        print()


def different_authors():
    filigree1 = get_image(r"images/filigrees/Monaco/C1-2r-Opening V-cropped.jpg")
    filigree2 = get_image(r"images/filigrees/Roselli/C3-1v-Resurrection-6-E-cropped.jpeg")

    print("Author of Filigree 1: Monaco")
    print("Author of Filigree 2: Roselli")

    result1 = []
    result2 = []

    recursive(filigree1, result1, 1)
    recursive(filigree2, result2, 1)

    print("Filigree 1: ", result1)
    print("Filigree 2: ", result2)

    print("Euclidean Distance: ", euclidean(result1, result2))


def main():
    print("Test of Recursive Algorithm with 4 Images:")
    print()
    recursive_test()
    print()

    print("Test with Multiple Filigrees with the Same Known Author:")
    print()
    same_author()
    print()

    print("Test with 2 Filigrees with Different Known Authors:")
    print()
    different_authors()


main()
