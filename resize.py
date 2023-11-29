import os
from PIL import Image


def standardize(image, size=(400, 500)):
    img = image.resize(size)
    return img


def resize_images(in_folder, out_folder):
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    files = os.listdir(in_folder)
    for file in files:
        if file.lower().endswith('.jpg'):
            input_path = os.path.join(in_folder, file)
            output_path = os.path.join(out_folder, file)
            with Image.open(input_path) as img:
                standardized_img = standardize(img)
                standardized_img.save(output_path)


input_folder = r"C:\Users\Smidge\Desktop\Filigree Images\For Research\Corale 1-Monaco Torelli CROPPED"
output_folder = r"C:\Users\Smidge\Desktop\Filigree Images\For Research\C1-2"
resize_images(input_folder, output_folder)
