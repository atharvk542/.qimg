from PIL import Image
import struct
import numpy as np


def load_probs(path):
    with open(path, "rb") as f:
        width, height, norm = struct.unpack("HHf", f.read(8))
        amplitudes = np.fromfile(f, dtype=np.float32)

    # raw probability amplitudes in the giant state
    probs = amplitudes**2

    # squash to 255
    probs = probs / np.max(probs) * 255
    probs = probs.astype(np.uint8)

    # load the probabilities
    image = Image.fromarray(probs.reshape((height, width, 3)))
    return image
