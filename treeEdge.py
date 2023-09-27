import PIL as pillow
from PIL import Image, ImageFilter
image = Image.open(r"downloads/tree.jpeg"_
image.convert("L")
image.filter(ImageFilter.FIND_EDGES)
image.save(r"downloads/treeEdge.jpeg")
exit()
