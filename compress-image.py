import skimage
from skimage.color import rgb2gray
import constriction
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from math import log2

from dahuffman import HuffmanCodec

def compute_entropy(img):
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

def intraframe(frame):
    new_frame=np.empty(frame.shape, dtype=np.int32)
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            x = frame[i][j].astype(np.int16)
            if i==0 and j==0:
                new_frame[i][j] = x
            elif i==0:
                new_frame[i][j] = x - frame[i][j-1]
            elif j==0:
                new_frame[i][j] = x - frame[i-1][j]
            else:
                a = frame[i][j-1].astype(np.int16)
                b = frame[i-1][j]
                c = frame[i-1][j-1]
                if (c >= max(a, b)):
                    new_frame[i][j] = x - min(a, b)
                elif (c <= min(a, b)):
                    new_frame[i][j] = x - max(a, b)
                else:
                    new_frame[i][j] = x - a + b - c
    
    return new_frame

def encode_huffman(difs):
    codec = HuffmanCodec.from_data(difs)
    return codec.encode(difs)


def main(img):
    # Number of bits to store entire image
    print(img.shape)
    n_pixels=img.shape[0]*img.shape[1]
    size = n_pixels*8

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

    # Do huffman encoding of the errors
    encoded = encode_huffman(difs.ravel())
    print(f"The encoded errors use {len(encoded)*8} bits which is an average of {len(encoded)*8/n_pixels} (bits/pixel)")

if __name__=="__main__":

    # Dog image
    file_path = "doggo.jpeg"
    img = skimage.io.imread(file_path)
    img = rgb2gray(img)

    # Random noise
    img = np.random.rand(255, 255)*255
    img = img.astype(np.int16)

    # Gradient image
    img = np.zeros((255, 255))
    for i in range(255):
        img[i,:] = i

    main(img)