from PIL import Image, GifImagePlugin
import os

filenames = sorted((fn for fn in os.listdir('bmp/')))
images = (Image.open('bmp/'+fn) for fn in filenames)
im = Image.open('bmp/020.bmp')

fp = open("out.gif", "wb")
GifImagePlugin._save(images, fp, 'out.gif')
fp.close()