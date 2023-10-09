import PIL as pillow
from PIL import Image
import zipf.factories
from zipf.factories import ZipfFromList

image = Image.open(r"treeEdge.jpeg")

colors = []

width, height = image.size

for y in range(height):
    for x in range(width):
        pixel = image.getpixel((x, y))
        colors.append(pixel)

my_factory = ZipfFromList()

my_zipf = my_factory.run(colors)

print(my_zipf)
