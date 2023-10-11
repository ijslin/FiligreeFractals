from image import *
from zipf import *


def count_shades(image):
   histogram = {}
   
   shades = []
   width = image.getWidth()
   height = image.getHeight()
   
   for y in range(height):
      for x in range(width):
         shade = image.getPixel(x, y)
         shades.append(shade)
         
   for i in range(len(shades)):
      r = shades[i][0]
      g = shades[i][1]
      b = shades[i][2]
      
      if (r == g & g == b & b == r):
         shades[i] = r
      else:
         break
   
   for shade in shades:
      histogram[shade] = histogram.get(shade, 0) + 1   
            
   return histogram


def get_zipf(file_name):
   # open image and get the width and height
   image = Image(file_name)
   width = image.getWidth()
   height = image.getHeight()
   
   # create a list to hold the shade values
   shades = []
   
   # create histogram
   histogram = count_shades(image)
   counts = histogram.values()
      
   # order the shades by rank and return R2 slope, return the values returned
   slope, r2, yint = byRank(counts)
   return slope, r2


def main():
   a = get_zipf("treeEdge.jpeg")
   print(a)
   
   
main()
