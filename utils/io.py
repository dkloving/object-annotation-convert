import numpy as np

try:
    from PIL import Image
except ImportError as error:
    import sys
    raise type(error)(str(error) + '. Pillow must be installed to use this format.').with_traceback(sys.exc_info()[2])


def read_image_file(image_file):
    return np.asarray(Image.open(image_file))
