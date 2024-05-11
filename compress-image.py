import skimage
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import numpy as np
from math import log2

from dahuffman import HuffmanCodec

def compute_entropy(img):
    '''
    Returns the entropy of the distribution of the pixels of the image
    '''
    values = img.flatten()
    n = len(values)

    if n <= 1:
        return 0

    value, counts = np.unique(values, return_counts=True)
    probs = counts / n
    n_difs = np.count_nonzero(probs)

    if n_difs <= 1:
        return 0

    H = 0
    for i in probs:
        H -= i * log2(i)
    return H
 
def x_diferences(frame):
    '''
    Returns a numpy array where the value at every pixel p(i, j) is set 
    to p(i, j-1) the value of the prediction.
    '''
    new_frame=np.empty(frame.shape, dtype=np.int32)
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            if i==0 and j==0:
                new_frame[i][j] = 0
            elif j==0:
                new_frame[i][j] = frame[i-1][j]
            else:
                new_frame[i][j] = frame[i][j-1]
    return new_frame


def main(img):
    # Number of bits to store entire image
    print(np.max(img))
    print(f"The image has {img.shape[0]}x{img.shape[1]} pixels")
    n_pixels=img.shape[0]*img.shape[1]
    size = n_pixels*8
    print(f"It would use {size} bits if left uncompressed")


    plt.imshow(img, cmap='gray')
    plt.show()

    H=compute_entropy(img)
    print(f"The entropy of the values of the image is {H}(bits/pixel)")

    # Display histogram
    plt.hist(img.ravel(), bins=256, histtype='step', color='black')
    plt.show()

    difs = img-x_diferences(img)
    # difs = intraframe(img)
    plt.imshow(difs, cmap='gray')
    plt.show()

    H=compute_entropy(difs)
    print(f"The entropy of the values of the image is {H}(bits/pixel)")

    # Display histogram
    plt.hist(difs.ravel(), bins=256, histtype='step', color='black')
    plt.show()

    # Do huffman encoding of the errors using library HuffmanCodec
    codec = HuffmanCodec.from_data(difs.ravel())
    encoded = codec.encode(difs.ravel())
    print(f"The encoded errors use {len(encoded)*8} bits which is an average of {len(encoded)*8/n_pixels} (bits/pixel)")

if __name__=="__main__":

    # Dog image
    file_path = "doggo.jpeg"
    img1 = skimage.io.imread(file_path)
    img1 = rgb2gray(img1)*255
    img1 = img1.astype(np.int16)

    # Random uniform noise
    img2 = np.random.rand(255, 255)*255
    img2 = img2.astype(np.int16)

    # Gradient image
    img3 = np.zeros((255, 255))
    for i in range(255):
        img3[i,:] = i

    main(img1)