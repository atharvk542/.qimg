# .qimg Image Encoder

.qimg is a quantum-inspired image format that uses amplitude encoding. It comes with a Flask-based web interface for encoding, decoding, and viewing .qimg files using probability-based and measurement-based loaders.

To run the web interface, clone the repository and install dependencies with `pip install -r requirements.txt`. Run `python app.py` to start the server. In the web interface, you can encode images into .qimg format (with download), decode .qimg files back to PNG, or view .qimg files through probability or measurement simulations.

## Encoding

Encoding stores image data as quantum amplitudes. The RGB image is flattened into a 1D array of pixel values (each pixel contributes 3 values for R, G, B). These values are normalized by dividing by the Euclidean norm of the array, creating amplitudes that sum to 1 in squared magnitude. This represents the image as a quantum state:

$$

\ket{\psi} = \sum_{i=1}^{N} \alpha_i \ket{i}


$$

where $N$ is the total number of color channels across all pixels (width × height × 3), and $\alpha_i$ are the normalized amplitudes.

The file format starts with a header: width (2 bytes), height (2 bytes), norm (4 bytes), followed by the float32 amplitudes.

## Decoding

Decoding reverses the process. It reads the header to get width, height, and norm. Then reads the amplitudes array, multiplies each by the norm to recover original pixel values, clips to [0, 255], and reshapes into an RGB image array. The result is saved as a standard PNG file.

## Probability Loader

The probability loader visualizes the quantum probabilities. It computes $p_i = |\alpha_i|^2$ for each amplitude, normalizes these probabilities to [0, 255] for display, and reshapes into an RGB image. Brighter pixels indicate higher probabilities in the quantum state.

## Measurement Loader

The measurement loader simulates quantum measurements. It computes probabilities as above, then performs random sampling (default 10,000 shots) based on these probabilities. Each "measurement" selects a pixel index, and counts are accumulated (default increment of 1 per measurement, adjustable via count_steps for brighter images with fewer shots). The counts are clipped to [0, 255] and displayed as an image, showing measurement frequencies. This demonstrates how repeated measurements might reveal the image through quantum collapse.

By default, 10,000 shots usually results in a very dark image, depending on the resolution of your image. This is because every single image must be counted multiple times in order for any color to appear. By zooming into the measurement-loaded images, you can see the individual red, green, and blue pixels forming the larger colors you see. Increasing the count_steps parameter will increase the brightness of the selected pixels. 
