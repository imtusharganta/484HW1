import tkinter as tk
from tkinter import *
import math
import os
from PIL import Image, ImageTk
from PixInfo import PixInfo


# main functionalities
root = tk.Tk()
root.title("Image Viewer")

pictureInfo = PixInfo(root)
root.mainloop()
