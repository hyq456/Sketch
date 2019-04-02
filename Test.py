
from PIL import Image
import os
import glob

def rgba2rgb(path):
    cate = [path + '/' + x for x in os.listdir(path) if os.path.isdir(path + '/' + x)]
    for folder in cate:
        # _, imgfolder = os.path.split(folder)
        for im in glob.glob(folder + '/*.png'):
            try:
                png = Image.open(im)
                png.load()  # required for png.split()

                background = Image.new("RGB", png.size, (255, 255, 255))
                background.paste(png, mask=png.split()[3]) # 3 is the alpha channel

                background.save(im, 'PNG', quality=100)
            except:
                print()
            # print('convert ' + im)
            # out_name = im.replace('.svg','.png',)
            # cairosvg.svg2png(url=im,write_to=out_name)
            # os.remove(im)
            print(im)
    print(" Finish")

path = './svg_processed'
rgba2rgb(path)