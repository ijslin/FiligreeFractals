import PIL as pillow
from PIL import Image, ImageFilter
image = Image.open(r"downloads/tree.jpeg")
image = image.convert("L")
image = image.filter(ImageFilter.FIND_EDGES)
image.save(r"downloads/treeEdge.jpeg")
exit()
