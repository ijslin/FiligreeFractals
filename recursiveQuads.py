import PIL as pillow
from PIL import Image

def crop(input,height,width,k):
    im = Image.open(input)
    imgwidth = im.size[0]
    imgheight = im.size[1]
    for i in range(0,imgheight-height/2,height-2):
        print(i)
        for j in range(0,imgwidth-width/2,width-2):
            print(j)
            box = (j, i, j+width, i+height)
            a = im.crop(box)
            im = a.save("e-Fillegre.jpg")
            k +=1

crop("e-Fillegre.jpg", 50, 50, 4)