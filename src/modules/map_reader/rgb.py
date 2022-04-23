from PIL import Image

def get_rgb(fp, at:tuple):
    return Image.open(fp).convert("RGB").getpixel(at)