# This version uses PIL

from PIL import Image, ImageFilter
from zipf import *
from math import *
import os
import csv
import tkinter as tk
from tkinter import filedialog


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
            if isinstance(a[i], str) or isinstance(b[i], str):
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

    if (author == "Monaco") or (author == "monaco"):
        images = number_of_images
        if images > len(monaco):
            images = len(monaco)

        slug = "images/filigrees/Monaco/"

        for i in range(images):
            link = slug + monaco[i]
            list.append(link)

    elif (author == "Roselli") or (author == "roselli"):
        images = number_of_images
        if images > len(roselli):
            images = len(roselli)

        slug = "images/filigrees/Roselli/"

        for i in range(images):
            link = slug + roselli[i]
            list.append(link)

    elif (author == "Gherarducci") or (author == "gherarducci"):
        images = number_of_images
        if images > len(gherarducci):
            images = len(gherarducci)

        slug = "images/filigrees/Gherarducci/"

        for i in range(images):
            link = slug + gherarducci[i]
            list.append(link)

    elif (author == "Camaldolese") or (author == "camaldolese"):
        images = number_of_images
        if images > len(camaldolese):
            images = len(camaldolese)

        slug = "images/filigrees/Camaldolese/"

        for i in range(images):
            link = slug + camaldolese[i]
            list.append(link)


def get_filigree_by_book(book_number, list):
    corale = ""
    slug = ""
    if book_number == 1:
        slug = "images/filigrees/Corale 1/"
        corale = os.listdir(slug)
    elif book_number == 3:
        slug = "images/filigrees/Corale 3/"
        corale = os.listdir(slug)
    elif book_number == 5:
        slug = "images/filigrees/Corale 5/"
        corale = os.listdir(slug)
    elif book_number == 6:
        slug = "images/filigrees/Corale 6/"
        corale = os.listdir(slug)
    elif book_number == 7:
        slug = "images/filigrees/Corale 7/"
        corale = os.listdir(slug)
    elif book_number == 8:
        slug = "images/filigrees/Corale 8/"
        corale = os.listdir(slug)
    elif book_number == 9:
        slug = "images/filigrees/Corale 9/"
        corale = os.listdir(slug)
    elif book_number == 11:
        slug = "images/filigrees/Corale 11/"
        corale = os.listdir(slug)
    elif book_number == 12:
        slug = "images/filigrees/Corale 12/"
        corale = os.listdir(slug)
    elif book_number == 13:
        slug = "images/filigrees/Corale 13/"
        corale = os.listdir(slug)
    elif book_number == 14:
        slug = "images/filigrees/Corale 14/"
        corale = os.listdir(slug)
    elif book_number == 15:
        slug = "images/filigrees/Corale 15/"
        corale = os.listdir(slug)
    elif book_number == 16:
        slug = "images/filigrees/Corale 16/"
        corale = os.listdir(slug)
    elif book_number == 17:
        slug = "images/filigrees/Corale 17/"
        corale = os.listdir(slug)
    elif book_number == 18:
        slug = "images/filigrees/Corale 18/"
        corale = os.listdir(slug)
    elif book_number == 19:
        slug = "images/filigrees/Corale 19/"
        corale = os.listdir(slug)

    corale.remove(".DS_Store")

    for image in corale:
        url = slug + image
        list.append(url)


def get_all_links(list):
    get_filigree_by_book(1, list)
    get_filigree_by_book(3, list)
    get_filigree_by_book(5, list)
    get_filigree_by_book(6, list)
    get_filigree_by_book(7, list)
    get_filigree_by_book(8, list)
    get_filigree_by_book(9, list)
    get_filigree_by_book(11, list)
    get_filigree_by_book(12, list)
    get_filigree_by_book(13, list)
    get_filigree_by_book(14, list)
    get_filigree_by_book(15, list)
    get_filigree_by_book(16, list)
    get_filigree_by_book(17, list)
    get_filigree_by_book(18, list)
    get_filigree_by_book(19, list)


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
        results = [link]

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
        # for result in results:
            # row = [result[0], result[1]]
            # rows.append(row)
        row = []

        for result in results:
            if isinstance(result, str):
                row.append(result)
            else:
                row.append(result[0])
                row.append(result[1])

        rows.append(row)

    file_name = ""  # Initializes the file name as an empty string

    # What file will be created depends on the image type
    if image_type == "edge":
        file_name = "zipf_edge_detection_v2.csv"
    elif image_type == "gray":
        file_name = "zipf_grayscale_v2.csv"
    elif image_type == "color":
        file_name = "zipf_color_v2.csv"

    # Writes the rows to the csv file
    with open(file_name, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Image", "Slope Q1", "R2 Q1", "Slope Q2", "R2 Q2", "Slope Q3", "R2 Q3", "Slope Q4", "R2 Q4",
                         "Slope Whole", "R2 Whole"])
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

    file_name = ""  # Initializes the file name as an empty string

    # What file will be created depends on the image type
    if image_type == "edge":
        file_name = "edge_detection.txt"
    elif image_type == "gray":
        file_name = "grayscale.txt"
    elif image_type == "color":
        file_name = "color.txt"

    file = open(file_name, "w")
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


def case_tests(test_code, image_type):
    links = []
    rows = []
    file_name = "case_" + test_code + "_" + image_type + ".csv"

    if test_code == 'a':
        get_filigree_by_book(16, links)
    elif test_code == 'b':
        get_filigree_by_book(11, links)
    elif test_code == 'c':
        get_filigree_by_book(19, links)
    elif test_code == 'd':
        get_filigree_by_book(8, links)
    elif test_code == 'e':
        get_filigree_by_book(5, links)
    elif test_code == 'f':
        get_filigree_by_book(1, links)
    elif test_code == 'g':
        get_filigree_by_book(15, links)

    for link in links:
        results = [link]

        if image_type == "edge":
            image = get_image(link)
            recursive(image, results, 1)
        elif image_type == "color":
            image = get_image_color(link)
            recursive(image, results, 1)
        else:
            print("Image type not supported! Please use 'edge' for edge-detection and 'color' for color")
            break

        row = []

        for result in results:
            if isinstance(result, str):
                row.append(result)
            else:
                row.append(result[0])
                row.append(result[1])

        rows.append(row)

    with open(file_name, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Image", "Slope Q1", "R2 Q1", "Slope Q2", "R2 Q2", "Slope Q3", "R2 Q3", "Slope Q4", "R2 Q4",
                         "Slope Whole", "R2 Whole"])
        writer.writerows(rows)


def get_book_number(list):
    link = list[0].split("/")
    book = link[-2]

    if book == "Corale 3":
        list.append(3)
    elif book == "Corale 5":
        list.append(5)
    elif book == "Corale 6":
        list.append(6)
    elif book == "Corale 7":
        list.append(7)
    elif book == "Corale 8":
        list.append(8)
    elif book == "Corale 9":
        list.append(9)
    elif book == "Corale 11":
        list.append(11)
    elif book == "Corale 12":
        list.append(12)
    elif book == "Corale 13":
        list.append(13)
    elif book == "Corale 14":
        list.append(14)
    elif book == "Corale 15":
        list.append(15)
    elif book == "Corale 16":
        list.append(16)
    elif book == "Corale 17":
        list.append(17)
    elif book == "Corale 18":
        list.append(18)
    elif book == "Corale 19":
        list.append(19)
    elif book == "Corale 1":
        list.append(1)
    else:
        list.append(0)


def get_book_by_file(list):
    link = list[0].split("/")
    image = link[-1]

    if "C3" in image:
        list.append(3)
    elif "C5" in image:
        list.append(5)
    elif "C6" in image:
        list.append(6)
    elif "C7" in image:
        list.append(7)
    elif "C8" in image or "Corale 8" in image:
        list.append(8)
    elif "C9" in image:
        list.append(9)
    elif "C11" in image:
        list.append(11)
    elif "C12" in image:
        list.append(12)
    elif "C13" in image:
        list.append(13)
    elif "C14" in image or "C-" in image:
        list.append(14)
    elif "C15" in image:
        list.append(15)
    elif "C16" in image:
        list.append(16)
    elif "C17" in image:
        list.append(17)
    elif "C18" in image:
        list.append(18)
    elif "C19" in image or "Chp 19" in image:
        list.append(19)
    elif "C1" in image:
        list.append(1)
    else:
        list.append(0)


def all_cases(image_type):
    links = []
    rows = []
    file_name = "all_cases_" + image_type + ".csv"

    get_filigree_by_book(16, links)
    get_filigree_by_book(11, links)
    get_filigree_by_book(19, links)
    get_filigree_by_book(8, links)
    get_filigree_by_book(5, links)
    get_filigree_by_book(1, links)
    get_filigree_by_book(15, links)

    for link in links:
        results = [link]

        get_book_number(results)

        if image_type == "edge":
            image = get_image(link)
            recursive(image, results, 1)
        elif image_type == "color":
            image = get_image_color(link)
            recursive(image, results, 1)
        else:
            print("Image type not supported! Please use 'edge' for edge-detection and 'color' for color")
            break

        row = []

        for result in results:
            if isinstance(result, str) or isinstance(result, int):
                row.append(result)
            else:
                row.append(result[0])
                row.append(result[1])

        rows.append(row)

    with open(file_name, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Image", "Book Number", "Slope Q1", "R2 Q1", "Slope Q2", "R2 Q2", "Slope Q3", "R2 Q3",
                         "Slope Q4", "R2 Q4", "Slope Whole", "R2 Whole"])
        writer.writerows(rows)


def get_path_GUI():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(parent=root, title='Choose a file')
    return file_paths


def write_csv(images):
    rows = []
    file_name = "filigrees.csv"
    csv_file_name = os.path.join(os.path.expanduser('~'), 'Documents', file_name)

    for i in range(len(images)):
        results = [images[i]]
        get_book_by_file(results)

        row = []

        filigree = get_image(images[i])
        recursive(filigree, results, 1)

        for result in results:
            if isinstance(result, str) or isinstance(result, int):
                row.append(result)
            else:
                row.append(result[0])
                row.append(result[1])

        rows.append(row)

    with open(csv_file_name, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Image", "Book Number", "Slope Q1", "R2 Q1", "Slope Q2", "R2 Q2", "Slope Q3", "R2 Q3",
                         "Slope Q4", "R2 Q4", "Slope Whole", "R2 Whole"])
        writer.writerows(rows)

    convert_to_arff(csv_file_name)


def convert_to_arff(csv_file_name):
    csv_file = csv_file_name
    arff_file = csv_file_name.replace(".csv", ".arff")
    relation = "Filigree_Images"

    data_type = ["nominal", "nominal", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric",
                 "numeric", "numeric", "numeric", "numeric"]
    # data_type = []
    columns_temp = []
    unique_temp = []
    unique_of_column = []
    data_type_temp = []
    final_data_type = []
    att_types = []
    p = 0

    f = open(csv_file, "r")
    reader = csv.reader(f)
    all_data = list(reader)
    attributes = all_data[0]
    total_columns = len(attributes)
    total_rows = len(all_data)
    f.close()

    for j in range(total_columns):
        for i in range(total_rows):
            if len(all_data[i][j]) == 0:
                all_data[i][j] = "0"

    for j in range(total_columns):
        for i in range(1, (total_rows - 1)):
            all_data[i][j] = all_data[i][j].lower()
            if "\r" in all_data[i][j] or '\r' in all_data[i][j] or "\n" in all_data[i][j] or '\n' in all_data[i][j]:
                all_data[i][j] = all_data[i][j].rstrip(os.linesep)
                all_data[i][j] = all_data[i][j].rstrip("\n")
                all_data[i][j] = all_data[i][j].rstrip("\r")
            try:
                if all_data[i][j] == str(float(all_data[i][j])) or all_data[i][j] == str(int(all_data[i][j])):
                    print()
            except ValueError as e:
                all_data[i][j] = "'" + all_data[i][j] + "'"

    for j in range(total_columns):
        for i in range(1, (total_rows - 1)):
            columns_temp.append(all_data[i][j])
        for item in columns_temp:
            if not (item in unique_temp):
                unique_temp.append(item)
        unique_of_column.append("{" + ','.join(unique_temp) + "}")
        unique_temp = []
        columns_temp = []

    # for j in range(1, total_rows):
    #     for i in range(0, total_columns):
    #         try:
    #             if all_data[j][i] == str(float(all_data[j][i])) or all_data[j][i] == str(int(all_data[j][i])):
    #                 data_type.append("numeric")
    #         except ValueError as e:
    #             data_type.append("nominal")

    for j in range(total_columns):
        p = j
        for i in range((total_rows - 1)):
            data_type_temp.append(data_type[p])
            # p += total_columns
        if "nominal" in data_type_temp:
            final_data_type.append("nominal")
        else:
            final_data_type.append("numeric")
        data_type_temp = []

    for i in range(len(final_data_type)):
        if final_data_type[i] == "nominal":
            att_types.append(unique_of_column[i])
        else:
            att_types.append(final_data_type[i])

    write_file = open(arff_file, "w")

    write_file.write("%\n% Comments go after a '%' sign.\n%\n")
    write_file.write("%\n% Relation: " + relation + "\n%\n%\n")
    write_file.write("% Attributes: " + str(total_columns) + " " * 5 + "Instances: " + str(total_rows - 1)
                     + "\n%\n%\n\n")

    write_file.write("@RElATION " + relation + "\n\n")

    for i in range(total_columns):
        write_file.write("@ATTRIBUTE" + " '" + attributes[i] + "' " + att_types[i] + "\n")

    write_file.write("\n@DATA\n")

    for i in range(1, (total_rows - 1)):
        write_file.write(','.join(all_data[i]) + "\n")


def run_selectable_images():
    files = get_path_GUI()
    write_csv(files)


def main():
    run_selectable_images()
    # convert_to_arff("iris.csv")


main()
