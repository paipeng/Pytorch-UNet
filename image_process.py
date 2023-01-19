import PIL
from PIL import Image
import glob
import argparse
from pathlib import Path
import random
import time

def convert_image(s2idir: str, gray: bool, cropsize: int, resize: int, output: str):
    s2icodes = sorted(glob.glob(s2idir + '/*'))
    for file in s2icodes:
        print(f'file: {file}')
        image = Image.open(file)
        if gray:
            if image.mode != 'L':
                image = image.convert('L')
        """
        if image.width == 1280:
            image = image.resize((640, 640), Image.BILINEAR)
        elif image.height == 480:
            image = image.resize((int(640/1.16), int(480/1.16)), Image.BILINEAR)
        """
        width, height = image.size   # Get dimensions


        if cropsize > 0:
            new_width = 300
            new_height = 300
            left = (width - new_width)/2
            top = (height - new_height)/2
            right = (width + new_width)/2
            bottom = (height + new_height)/2
            # Crop the s2icode of the image
            image = image.crop((left, top, right, bottom))

        width, height = image.size   # Get dimensions
        print(f'image size: {width}-{height}')

        if resize > 0:
            image = image.resize((resize, int(resize*height/width)), Image.BILINEAR)
        
        files = file.split('/')
        output_file = '{output}/{file}'.format(output=output, file=files[-1])
        print(f'output_file: {output_file}')
        image.save(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='image preprocessing')
    parser.add_argument('-i', '--input', metavar='I', type=str, required=True, help='image folder path')
    parser.add_argument('-o', '--output', metavar='O', type=str, required=True, help='output folder')
    parser.add_argument('-g', '--gray', metavar='O', type=bool, default=False, required=False, help='output folder')
    parser.add_argument('-c', '--cropsize', metavar='O', type=int, default=320, required=False, help='crop size')
    parser.add_argument('-r', '--resize', metavar='O', type=int, default=512, required=False, help='resize')
    args = parser.parse_args()

    Path(args.output).mkdir(parents=True, exist_ok=True)

    convert_image(args.input, args.gray, args.cropsize, args.resize, args.output)