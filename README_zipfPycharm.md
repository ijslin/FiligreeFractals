# zipfPycharm.py

## Must install and import PIL (specifically Image and Image Filter), math, os, and csv
## Use zipf.py for zipf

## count_shades returns a dictionary of the colors in the image object used as a parameter/argument.

## get_image returns an edge-detected image object based on the string in the argument.

## get_image_gray returns an grayscaled image object based on the string in the argument.

## get_image_color returns an colored image object based on the string in the argument.

## get_quadrants returns 4 image objects that are the top left, top right, bottom left, and bottom right parts of the image object passed in the argument.

## get_zipf_color coverts the image object in the argument to an edge-detected image and then returns the slope and r2 values.

## get_zipf_gray_edge returns the slope and r2 values of the image object in the argument.

## euclidean gets and returns the euclidean distance between two points or two vectors.

## get_zipf(histogram) gets the slope and r2 values using a histogram for the parameter/argument.

## recursive gets the slope and r2 values for the whole image and any quadrants if the depth is greater than 1; requires a list/array to be made before running so that values can be added.

## recursive_test tests the recursive function using an image with 4 quadrants of different test images.

## get_links gets the links as strings to the filigrees by the specified author and adds the number specified to a list/array; list/array must be made before

## get_all_links gets the links as strings to all of the filigrees and adds them to a list/array; depending on how they are saved in the project folder links may need to be changed

## same_author tests the accuracy of the algorithm by comparing one image against 14 others by the same author.

## different_author tests the accuracy of the algorithm by comparing one image against 7 others by the same author and 7 others by a different author.

## experiment_1 tests the same thing as different_author but has 15 by the same, 3 by a different and compares all of the images to the ones after it; whether the images are edge_detected, grayscaled, or colored should be specified by the parameter/argument.

## all_images is the first attempt at running the algorithm using all of the filigrees and writes it to a txt file; shouldn't be used because it is too slow.

## merge_dicts merges two dictionaries by adding the values of the second parameter/argument into the one specified in the first parameter/argument.

## get_vectors gets the vectors of every image recursively and writes them to a csv file; file name depends on if images are edge-detected, grayscaled, or colored.

## all_images_quick is a quicker version of all images that runs using a similar format to get_vectors in order to make it faster; writes the euclidean distances to a txt file whose name depends on the image type.

## main is to run functions for testing purposes.