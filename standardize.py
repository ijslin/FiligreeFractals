from PIL import Image


def standardize(image, size=(256, 256), mode="RGB"):
    with Image.open(image) as img:
        img = img.resize(size)
        img = img.convert(mode)
        return img


# Test usage:
input_image_path = "C1-16r-S w mandorla.jpg"
test = standardize(input_image_path)
test.save(r"standardized_image2.jpg")
