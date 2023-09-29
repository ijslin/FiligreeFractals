import PIL as pillow
from PIL import Image, ImageFilter
image = Image.open(r"downloads/tree.jpeg")
image.convert("L")
image.filter(ImageFilter.FIND_EDGES)
image.save(r"downloads/treeEdge.jpeg")
exit()
