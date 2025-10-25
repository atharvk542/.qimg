import numpy as np
from PIL import Image
import struct


def decode(file_path, output_path):
    # read in binary mode
    with open(file_path, "rb") as f:
        # unpack width, height, and norm from header
        width, height, norm = struct.unpack("HHf", f.read(8))
        amps = np.fromfile(f, dtype=np.float32)

    # revert pixels back into respective values and clip to appropriate rgb values / format
    pixels = amps * norm
    pixels = np.clip(pixels, 0, 255).astype(np.uint8)

    img = Image.fromarray(pixels.reshape((height, width, 3)))
    img.save(output_path)
