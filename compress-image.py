import skimage 
import constriction
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from math import log2

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
                new_frame[i][j] = frame[i][j]
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

def main():
    file_path = "doggo.jpeg"
    img = skimage.io.imread(file_path)
    
    # Plot image
    plt.imshow(img)
    plt.show()

    # Number of bits to store entire image
    print(img.shape)
    size = img.shape[0]*img.shape[1]*8

    # Plot Red component
    red = img[:,:,0]
    plt.imshow(red, cmap='gray')
    plt.show()

    H=compute_entropy(red)
    print(f"The entropy of the values of the image is {H}(bits/pixel)")

    # Display histogram
    plt.hist(red.ravel(), bins=256, histtype='step', color='black')
    plt.show()

    #difs = red-x_diferences(red)
    difs = intraframe(red)
    plt.imshow(difs, cmap='gray')
    plt.show()

    H=compute_entropy(difs)
    print(f"The entropy of the values of the image is {H}(bits/pixel)")

    # Display histogram
    plt.hist(difs.ravel(), bins=256, histtype='step', color='black')
    plt.show()

if __name__=="__main__":
    main()