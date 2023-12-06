# This version uses PIL

from PIL import Image, ImageFilter
from zipf import *
from math import *
import os
import csv


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


def get_image_gray(link):
    image = Image.open(link)
    image = image.convert("L")

    return image


def get_image_color(link):
    image = Image.open(link)

    return image


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

    return histogram, (slope, r2)  # Returns only the slope and r2 as those are the only ones necessary for the Euclidean distance


def euclidean(a, b):
    # Checks if first item in each list is a string and removes it if it is

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
            if isinstance(a[i], str) | isinstance(b[i], str):
                continue
            else:
                dx = b[i][0] - a[i][0]
                dy = b[i][1] - a[i][1]
                sum = sum + ((dx * dx) + (dy * dy))

        result = sqrt(sum)

    return result


def get_zipf(histogram):
    counts = list(histogram.values())  # creates a list using the histogram values

    slope, r2, yint = byRank(counts)

    return slope, r2


def recursive(image, list, depth):
    if depth == 0:
        histogram, point = get_zipf_gray_edge(image)
        list.append(point)
        return histogram
    else:
        quad1, quad2, quad3, quad4 = get_quadrants(image)
        histogram1 = recursive(quad1, list, depth - 1)
        histogram2 = recursive(quad2, list, depth - 1)
        histogram3 = recursive(quad3, list, depth - 1)
        histogram4 = recursive(quad4, list, depth - 1)

        merge_dicts(histogram1, histogram2)
        merge_dicts(histogram1, histogram3)
        merge_dicts(histogram1, histogram4)

        list.append(get_zipf(histogram1))


def recursive_test():
    print("Test of Recursive Algorithm with 4 Images:")
    print()

    image = get_image(r"images/test_images/recursive_test.jpeg")
    result = []
    recursive(image, result, 1)
    print("Recursive Output: ", result)

    image1 = get_image(r"images/test_images/billmanaris.jpeg")
    r1 = []
    recursive(image1, r1, 0)
    print("Arbitrary Image Zipf: ", r1[0])
    print("Top Left Quadrant Zipf: ", result[0])

    image2 = get_image(r"images/test_images/white-noise-1400x825.jpeg")
    r2 = []
    recursive(image2, r2, 0)
    print("White Noise Zipf: ", r2[0])
    print("Top Right Quadrant Zipf: ", result[1])

    image3 = get_image(r"images/test_images/plain-black-background-02fh7564l8qq4m6d.jpeg")
    r3 = []
    recursive(image3, r3, 0)
    print("Background with Blemish Zipf: ", r3[0])
    print("Bottom Left Quadrant Zipf: ", result[2])

    image4 = get_image(r"images/test_images/tree.jpeg")
    r4 = []
    recursive(image4, r4, 0)
    print("Tree Zipf: ", r4[0])
    print("Bottom Right Quadrant Zipf: ", result[3])
    print()


def get_links(author, number_of_images, list):
    monaco = os.listdir("images/filigrees/Monaco/")
    roselli = os.listdir("images/filigrees/Roselli")
    gherarducci = os.listdir("images/filigrees/Gherarducci")
    camaldolese = os.listdir("images/filigrees/Camaldolese")

    monaco.remove(".DS_Store")
    roselli.remove(".DS_Store")
    gherarducci.remove(".DS_Store")
    camaldolese.remove(".DS_Store")

    if (author == "Monaco") | (author == "monaco"):
        images = number_of_images
        if images > len(monaco):
            images = len(monaco)

        slug = "images/filigrees/Monaco/"

        for i in range(images):
            link = slug + monaco[i]
            list.append(link)

    elif (author == "Roselli") | (author == "roselli"):
        images = number_of_images
        if images > len(roselli):
            images = len(roselli)

        slug = "images/filigrees/Roselli/"

        for i in range(images):
            link = slug + roselli[i]
            list.append(link)

    elif (author == "Gherarducci") | (author == "gherarducci"):
        images = number_of_images
        if images > len(gherarducci):
            images = len(gherarducci)

        slug = "images/filigrees/Gherarducci/"

        for i in range(images):
            link = slug + gherarducci[i]
            list.append(link)

    elif (author == "Camaldolese") | (author == "camaldolese"):
        images = number_of_images
        if images > len(camaldolese):
            images = len(camaldolese)

        slug = "images/filigrees/Camaldolese/"

        for i in range(images):
            link = slug + camaldolese[i]
            list.append(link)


def get_all_links(list):
    corale1 = os.listdir("images/filigrees/Corale 1/")
    corale3 = os.listdir("images/filigrees/Corale 3/")
    corale5 = os.listdir("images/filigrees/Corale 5/")
    corale6 = os.listdir("images/filigrees/Corale 6/")
    corale7 = os.listdir("images/filigrees/Corale 7/")
    corale8 = os.listdir("images/filigrees/Corale 8/")
    corale9 = os.listdir("images/filigrees/Corale 9/")
    corale11 = os.listdir("images/filigrees/Corale 11/")
    corale12 = os.listdir("images/filigrees/Corale 12/")
    corale13 = os.listdir("images/filigrees/Corale 13/")
    corale14 = os.listdir("images/filigrees/Corale 14/")
    corale15 = os.listdir("images/filigrees/Corale 15/")
    corale16 = os.listdir("images/filigrees/Corale 16/")
    corale17 = os.listdir("images/filigrees/Corale 17/")
    corale18 = os.listdir("images/filigrees/Corale 18/")
    corale19 = os.listdir("images/filigrees/Corale 19/")

    corale1.remove(".DS_Store")
    corale3.remove(".DS_Store")
    corale5.remove(".DS_Store")
    corale6.remove(".DS_Store")
    corale7.remove(".DS_Store")
    corale8.remove(".DS_Store")
    corale9.remove(".DS_Store")
    corale11.remove(".DS_Store")
    corale12.remove(".DS_Store")
    corale13.remove(".DS_Store")
    corale14.remove(".DS_Store")
    corale15.remove(".DS_Store")
    corale16.remove(".DS_Store")
    corale17.remove(".DS_Store")
    corale18.remove(".DS_Store")
    corale19.remove(".DS_Store")

    for image in corale1:
        slug = "images/filigrees/Corale 1/"
        url = slug + image
        list.append(url)
    for image in corale3:
        slug = "images/filigrees/Corale 3/"
        url = slug + image
        list.append(url)
    for image in corale5:
        slug = "images/filigrees/Corale 5/"
        url = slug + image
        list.append(url)
    for image in corale6:
        slug = "images/filigrees/Corale 6/"
        url = slug + image
        list.append(url)
    for image in corale7:
        slug = "images/filigrees/Corale 7/"
        url = slug + image
        list.append(url)
    for image in corale8:
        slug = "images/filigrees/Corale 8/"
        url = slug + image
        list.append(url)
    for image in corale9:
        slug = "images/filigrees/Corale 9/"
        url = slug + image
        list.append(url)
    for image in corale11:
        slug = "images/filigrees/Corale 11/"
        url = slug + image
        list.append(url)
    for image in corale12:
        slug = "images/filigrees/Corale 12/"
        url = slug + image
        list.append(url)
    for image in corale13:
        slug = "images/filigrees/Corale 13/"
        url = slug + image
        list.append(url)
    for image in corale14:
        slug = "images/filigrees/Corale 14/"
        url = slug + image
        list.append(url)
    for image in corale15:
        slug = "images/filigrees/Corale 15/"
        url = slug + image
        list.append(url)
    for image in corale16:
        slug = "images/filigrees/Corale 16/"
        url = slug + image
        list.append(url)
    for image in corale17:
        slug = "images/filigrees/Corale 17/"
        url = slug + image
        list.append(url)
    for image in corale18:
        slug = "images/filigrees/Corale 18/"
        url = slug + image
        list.append(url)
    for image in corale19:
        slug = "images/filigrees/Corale 19/"
        url = slug + image
        list.append(url)


def same_author():
    print("Test with Multiple Filigrees with the Same Known Author:")
    print()

    links = []
    get_links("Monaco", 15, links)
    filigree1 = get_image(links[0])
    test_link = links[0]
    links.pop(0)

    print("Author: Monaco")
    test_number = 1

    for link in links:
        print("Test", test_number, ":")

        filigree2 = get_image(link)

        result1 = [test_link]
        result2 = [link]

        recursive(filigree1, result1, 1)
        recursive(filigree2, result2, 1)

        print("Filigree 1: ", result1)
        print("Filigree 2: ", result2)

        print("Euclidean Distance: ", euclidean(result1, result2))
        test_number += 1
        print()
    print()


def different_authors():
    print("Test with Multiple Filigrees with Different Known Authors:")
    print()

    links = []
    get_links("Monaco", 8, links)
    get_links("Camaldolese", 7, links)
    filigree1 = get_image(links[0])
    test_link = links[0]
    links.pop(0)

    print("Author 1: Monaco")
    print("Author 2: Camaldolese")
    test_number = 1

    for link in links:
        print("Test", test_number, ":")

        filigree2 = get_image(link)

        result1 = [test_link]
        result2 = [link]

        recursive(filigree1, result1, 1)
        recursive(filigree2, result2, 1)

        print("Filigree 1: ", result1)
        print("Filigree 2: ", result2)

        print("Euclidean Distance: ", euclidean(result1, result2))
        test_number += 1
        print()


def experiment_1(image_type):
    links = []
    get_links("Monaco", 15, links)
    get_links("Camaldolese", 3, links)

    if image_type == "edge":
        print("Edge-Detected Images")
        print()

        for i in range(len(links)):
            print("Image", i + 1)
            print()
            filigree1 = get_image(links[i])

            for j in range(len(links)):
                if j <= i:
                    continue
                else:
                    result1 = [links[i]]
                    recursive(filigree1, result1, 1)

                    filigree2 = get_image(links[j])
                    result2 = [links[j]]
                    recursive(filigree2, result2, 1)

                    print("Filigree 1: ", result1)
                    print("Filigree 2: ", result2)
                    print("Euclidean Distance: ", euclidean(result1, result2))
                    print()

    elif image_type == "gray":
        print("Gray-Scaled Images")
        print()

        for i in range(len(links)):
            print("Image", i + 1)
            print()
            filigree1 = get_image_gray(links[i])

            for j in range(len(links)):
                if j <= i:
                    continue
                else:
                    result1 = [links[i]]
                    recursive(filigree1, result1, 1)

                    filigree2 = get_image_gray(links[j])
                    result2 = [links[j]]
                    recursive(filigree2, result2, 1)

                    print("Filigree 1: ", result1)
                    print("Filigree 2: ", result2)
                    print("Euclidean Distance: ", euclidean(result1, result2))
                    print()

    elif image_type == "color":
        print("Colored Images")
        print()

        for i in range(len(links)):
            print("Image", i + 1)
            print()
            filigree1 = get_image_color(links[i])

            for j in range(len(links)):
                if j <= i:
                    continue
                else:
                    result1 = [links[i]]
                    recursive(filigree1, result1, 1)

                    filigree2 = get_image_color(links[j])
                    result2 = [links[j]]
                    recursive(filigree2, result2, 1)

                    print("Filigree 1: ", result1)
                    print("Filigree 2: ", result2)
                    print("Euclidean Distance: ", euclidean(result1, result2))
                    print()


def all_images():
    links = []
    get_all_links(links)

    file = open("all_images_test.txt", "w")

    # Outer loop gets one of the filigree images
    for i in range(len(links)):
        print("Image", i + 1, file=file)
        print("\n", file=file)

        filigree1 = get_image(links[i])

        # Inner loop grabs the rest of the images to compare
        for j in range(len(links)):
            if j <= i:  # Skips an image if it is the same one or the two were compared in a previous test
                continue
            else:
                result1 = [links[i]]
                recursive(filigree1, result1, 1)

                filigree2 = get_image(links[j])
                result2 = [links[j]]
                recursive(filigree2, result2, 1)

                print("Filigree 1: ", result1, file=file)
                print("Filigree 2: ", result2, file=file)
                print("Euclidean Distance: ", euclidean(result1, result2), file=file)
                print("\n", file=file)
    file.close()


def merge_dicts(dict1, dict2):
    for entry in dict2:
        # Adds the counts of same keys and creates new keys if they don't exist
        dict1[entry] = dict1.get(entry, 0) + dict2.get(entry, 0)


def dict_merge_test():
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'a': 3, 'b': 4}
    merge_dicts(dict1, dict2)
    print(dict1)


def get_vectors(image_type):
    links = []
    get_all_links(links)
    rows = []

    # Runs through all of the filigree images to get the zipf distribution recursively
    for link in links:
        results = []

        # This if-else clause checks the parameter to determine what type of image to use whether edge detected,
        # grayscaled, or colored; the last clause prints an error message if the parameter doesn't match the three
        # options
        if image_type == "edge":
            image = get_image(link)
            recursive(image, results, 1)
        elif image_type == "gray":
            image = get_image_gray(link)
            recursive(image, results, 1)
        elif image_type == "color":
            image = get_image_color(link)
            recursive(image, results, 1)
        else:
            print("Image type not supported! Please use 'edge' for edge-detection, 'gray' for grayscale, and 'color' "
                  "for color")
            break

        # Adds all of the slope and r2 values gotten to a list of rows to be written to a csv file
        for result in results:
            row = [result[0], result[1]]
            rows.append(row)

    # Writes the rows to the csv file
    with open("zipf_edge_detection.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def all_images_quick(image_type):
    links = []
    get_all_links(links)
    zipfs = []

    # Runs through all of the filigree images to get the zipf distribution recursively
    for link in links:
        results = [link]

        # This if-else clause checks the parameter to determine what type of image to use whether edge detected,
        # grayscaled, or colored; the last clause prints an error message if the parameter doesn't match the three
        # options
        if image_type == "edge":
            image = get_image(link)
            recursive(image, results, 1)
            zipfs.append(results)
        elif image_type == "gray":
            image = get_image_gray(link)
            recursive(image, results, 1)
            zipfs.append(results)
        elif image_type == "color":
            image = get_image_color(link)
            recursive(image, results, 1)
            zipfs.append(results)
        else:
            print("Image type not supported! Please use 'edge' for edge-detection, 'gray' for grayscale, and 'color' "
                  "for color")
            break

    file = None  # Initializes the file as None

    # What file will be created depends on the image type
    if image_type == "edge":
        file = open("edge_detection.txt", "w")
    elif image_type == "gray":
        file = open("grayscale.txt", "w")
    elif image_type == "color":
        file = open("color.txt", "w")

    # Runs through the zipfs created to compare and writes the Euclidean distance to the file created before
    for i in range(len(zipfs)):
        a = zipfs[i]

        if i < (len(zipfs) - 1):
            print("Image", i + 1, file=file)
            print(a, file=file)

        for j in range(len(zipfs)):
            if j <= i:
                continue
            else:
                b = zipfs[j]
                print(b, file=file)
                print("Euclidean Distance: ", euclidean(a, b), file=file)
                print("\n", file=file)

    file.close()


def main():
    all_images_quick("color")


main()
