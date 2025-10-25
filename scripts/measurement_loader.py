import numpy as np
from PIL import Image
import struct


# this viewer is random, and repeated measurements will lead to a larger likelihood
# of seeing a specific pixel
# more times a pixel is observed, more bright it will be
def simulate_measurement(file_path, samples=10000, count_steps=1):
    with open(file_path, "rb") as f:
        width, height, norm = struct.unpack("HHf", f.read(8))
        amplitudes = np.fromfile(f, dtype=np.float32)

    probs = amplitudes**2
    probs /= np.sum(probs)

    counts = np.zeros_like(probs)  # will store selected pixels and num selections

    # simulate repeated measurements by choosing random pixels
    indices = np.random.choice(len(probs), size=samples, p=probs)
    for i in indices:
        counts[i] += count_steps

    # normalize for viewing
    img_array = np.clip(counts, 0, 255).astype(np.uint8)
    img = Image.fromarray(img_array.reshape((height, width, 3)))

    return img
