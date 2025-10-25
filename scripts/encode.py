import numpy as np
from PIL import Image
import struct


def encode(path, output_file):
    img = Image.open(path).convert("RGB")
    arr = np.array(img).astype(np.float32)
    flat = arr.flatten()

    # normalized flattened pixel values, store as "quantum amplitudes of a state"
    norm = np.linalg.norm(flat)
    amplitudes = flat / norm

    # write in binary mode
    with open(output_file, "wb") as f:
        # write width, height, norm
        f.write(struct.pack("HHf", img.width, img.height, norm))
        amplitudes.tofile(f)
