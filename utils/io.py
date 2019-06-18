import numpy as np

try:
    from PIL import Image
except ImportError as error:
    import sys
    raise type(error)(str(error) + '. Pillow must be installed to use this format.').with_traceback(sys.exc_info()[2])


def read_image_file(image_file):
    return np.asarray(Image.open(image_file))


def write_image_file(image_array, filename):
    if not type(image_array) == np.ndarray:
        raise TypeError("image_array must be type numpy.ndarray")
    if not image_array.dtype == np.uint8:
        raise ValueError("image_array must be dtype uint8")
    if not ((image_array.shape[-1] == 3) or (image_array.shape[-1] == 1)):
        raise ValueError("image_array must be [m * n * 3] or (m * n * 1)")
    mode = 'L' if image_array.shape[-1] == 1 else 'RGB'
    pil_image = Image.fromarray(image_array, mode)
    pil_image.save(filename)
