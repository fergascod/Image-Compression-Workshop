import cv2
import matplotlib.pyplot as plt
from skimage.color import rgb2gray

import numpy as np


def play_video(file):
    '''
    Plays the video file
    '''

    # Create a VideoCapture object and read from input file 
    cap = cv2.VideoCapture(file) 
    
    # Check if camera opened successfully 
    if (cap.isOpened()== False): 
        print("Error opening video file") 
    
    # Read until video is completed 
    while(cap.isOpened()): 
        ret, frame = cap.read() 
        if ret == True: 
        # Display the resulting frame 
            cv2.imshow('Frame', frame) 
            if cv2.waitKey(25) & 0xFF == ord('q'): 
                break
    
        else: 
            break
    
    cap.release() 
    cv2.destroyAllWindows() 

def read_video(file):
    '''
    Reads the video file onto a list of numpy arrays (one for every frame)
    '''

    list_frames=[]
    vidcap = cv2.VideoCapture(file)
    success,image = vidcap.read()

    while success:
        image = image[:,:,0] # We will compress the first channel
        list_frames.append(image)   
        success,image = vidcap.read()


    return  list_frames

def main(file):
    play_video(file)
    list_frames = read_video(file)

    # Showing the first frame
    plt.imshow(list_frames[0], cmap='gray')
    plt.show()

    '''
    TASK: 
    Use the functions we defined in the compress-image.py file to compress the video
    '''

if __name__=="__main__":
    file = "sevilla2.mp4"
    file_diff = file.split(".")[0]+"_diff.avi"
    main(file)


