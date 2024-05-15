# Image-Compression-Workshop
This repository contains the code for the workshop on image compression of the Data Days 2024 event. You can find the slides of the presentation of the workshop (in Catalan) in the file [Data_Days_2024.pdf](https://github.com/fergascod/Image-Compression-Workshop/blob/main/Data_Days_2024.pdf). 

# Prerequisites

To execute the scripts provided in this repo you should install the required Python libraries which are included in the `requirements.txt` file. To do so, start a Python virtual environment, activate it and then install the dependencies using:

```
python3 -m venv myenv
source myenv/bin/activate
python3 -m pip install -r requirements.txt
```

# Usage

In order to execute the examples simply use the python command from terminal where the environment has been activated:

```
python3 compress_image.py
```
The code will show you an image and compute its histogram and entropy. Then, it will use predictive coding to decorrelate the image to try to lower its entropy, in this case we are simply using the previous pixel in raster-scan order. Finally, an image with the residuals will be shown and its entropy and histogram will be shown. To see how much the residuals can be compressed a Python library implementing Huffman coding ([dahuffman](https://pypi.org/project/dahuffman/)) compresses the image into a string of bits whose size is compared to the original file size. In the code, you can select one of three images to compress: a portrait of a dog, an image with uniform noise and a gradient image; check out the differences/similarities of the entropy of the images/residuals and try to understand them!

You can also try to compress video files by using the same techniques in `compress_video.py`! A list of possible tasks to do with the code is provided in the last slide of the presentation in [Data_Days_2024.pdf](https://github.com/fergascod/Image-Compression-Workshop/blob/main/Data_Days_2024.pdf).

# Author

Fernando Gastón Codony (fgaston@crm.cat/fergascod@gmail.com)
