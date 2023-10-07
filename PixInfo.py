# PixInfo.py
# Program to start evaluating an image in python
from PIL import Image, ImageTk
import glob
import os
import math


# Pixel Info class.
class PixInfo:
#---------------------------------------------------------------------------------------
    # Constructor.
    def __init__(self, master):
        self.master = master
        self.imageList = []
        self.photoList = []
        self.xmax = 0
        self.ymax = 0
        self.colorCode = []
        self.intenCode = []
         # Initialize an empty list to store intensity values
        self.intensity_values = []
        self.pixList = []

        # Add each image (for evaluation) into a list,
        # and a Photo from the image (for the GUI) in a list.
        for infile in glob.glob('images/*.jpg'):

            file, ext = os.path.splitext(infile)
            im = Image.open(infile)

            # Resize the image for thumbnails.
            imSize = im.size
            x = int(imSize[0]/4)
            y = int(imSize[1]/4)
            imResize = im.resize((x, y), Image.LANCZOS)
            photo = ImageTk.PhotoImage(imResize)

            # Find the max height and width of the set of pics.
            if x > self.xmax:
                self.xmax = x
            if y > self.ymax:
                self.ymax = y

            # Add the images to the lists.
            self.imageList.append(im)
            self.photoList.append(photo)

        # Create a list of pixel data for each image and add it
        # to a list.
        for im in self.imageList[:]:

            pixList = list(im.getdata())
            CcBins, InBins = self.encode(pixList)
            self.colorCode.append(CcBins)
            self.intenCode.append(InBins)
#---------------------------------------------------------------------------------------
# Method to calculate intensity for each pixel in an image
    def intensity_calculator(self, pixList):
        # Convert the image to a list of pixel data
        
        # Loop through each pixel
        for pixel in pixList:
            # Extract R, G, B values from the pixel
            R, G, B = pixel[:3]
            
            # Calculate intensity
            intensity = 0.299 * R + 0.587 * G + 0.114 * B
            
            # Append the intensity value to the list
            self.intensity_values.append(intensity)
        
        return self.intensity_values 
    # Bin function returns an array of bins for each
    # image, both Intensity and Color-Code methods.
#---------------------------------------------------------------------------------------
    def encode(self, pixList):

        # # 2D array initilazation for bins, initialized
        # # to zero.
        # CcBins = [0]*64
        # InBins = [0]*25

        # # your code

        # # Return the list of binary digits, one digit for each
        # # pixel.
        # return CcBins, InBins
             # 2D array initialization for bins, initialized to zero.
        CcBins = [0]*64
        InBins = [0]*25

        # Calculate intensity values for the image
        intensity_values = self.intensity_calculator(self.pixList)

        # Populate InBins based on intensity values
        InBins[0] = len(intensity_values)  # h0 includes the total number of pixels
        for intensity in intensity_values:
            bin_index = int(intensity // 10) + 1  # Calculate which bin the intensity falls into
            if bin_index < 25:  # Ensure the index is within the range of InBins
                InBins[bin_index] += 1  # Increment the count for that bin

        return CcBins, InBins

    # Accessor functions:

    def get_imageList(self):
        return self.imageList

    def get_photoList(self):
        return self.photoList

    def get_xmax(self):
        return self.xmax

    def get_ymax(self):
        return self.ymax

    def get_colorCode(self):
        return self.colorCode

    def get_intenCode(self):
        return self.intenCode
