import tkinter as tk
from tkinter import *
import tkinter.font as font
import math
import os
from PIL import Image, ImageTk
from PixInfo import PixInfo

class GUI(Frame):
    #----------------------------------------------------------------------------------------
    #                                              CONSTRUCTOR                            
    def __init__(self, master, pix_info):
        Frame.__init__(self, master)
        self.master = master
        self.pix_info = pix_info
        self.current_image_index = 0 
        
        #main frame of the GUI
        guiFrame = Frame(master)
        guiFrame.pack()
        
    #----------------------------------------------------------------------------------------
        #                                          LEFT FRAME
        #
        # Create the left frame that will take up 2/3 of the GUI
        # The purpose of this is to house all of the images
        self.leftFrame = Frame(guiFrame, bg='#F4F7E8', width=550, height=300)
        self.leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand = True)
        
        # Create a canvas inside the left frame
        self.canvas = Canvas(self.leftFrame, bg='#F4F7E8')
        #self.canvas.grid(row=0, column=0, sticky='nsew')
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.leftFrame.pack_propagate(0)

        # Create a scrollbar and associate it with the canvas
        self.scrollbar = Scrollbar(self.leftFrame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Bind the mouse wheel event to the canvas
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)


        # Create a frame inside the canvas to hold other widgets
        self.innerFrame = Frame(self.canvas, bg='#F4F7E8')
        self.canvas.create_window((0, 0), window=self.innerFrame, anchor='nw')

        # Update the scroll region to fit the inner frame
        self.innerFrame.bind('<Configure>', lambda e: self.canvas.config(scrollregion=self.canvas.bbox('all')))
        self.populate_images()
 
    #----------------------------------------------------------------------------------------
        #                                           RIGHT FRAME
        #
        # Create the right frame that will take up 1/3 of the GUI
        # The purpose of this is to house the selected image
        self.rightFrame = Frame(guiFrame, bg='#EAE5DC', width=250, height=300)
        self.rightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand = True)
        self.rightFrame.pack_propagate(0)
        
        self.selected_image_label = Label(self.rightFrame)
        self.selected_image_label.pack(side=TOP, fill=BOTH, expand=False)
        
        # Set a default image from PixInfo's photoList
        
        default_image = pix_info.get_imageList()[0]  # Using the first image as the default
        default_image_resized = default_image.resize((200, 100), Image.LANCZOS)  # Resize the image
        default_image_tk = ImageTk.PhotoImage(default_image_resized)
        self.selected_image_label.config(image=default_image_tk)
        self.selected_image_label.image = default_image_tk 
       
    #---------------------------------------------------------------------------------------    
        #Buttons
        # This will be used for creating buttons such as INTENSITY, OPEN IMAGE, COLOR CODE#
        intensity_button = Button(self.rightFrame, text="Intensity Method", fg="black", padx=5, width=5, height=2)
        intensity_button.pack(side=TOP, fill=X)
        intensity_button.bind("<Enter>", self.make_bold)
        intensity_button.bind("<Leave>", self.make_normal)       
        # intensity_button = Button(self.rightFrame, text = "Intensity Method", fg = "black", padx = 5, width = 5, height = 2)
        # #intensity_button.grid(row = 0)
        # intensity_button.pack(side = TOP, fill = X)

        #button works, still need to figure out how to open selected image
        openImage_button = Button(self.rightFrame, text="Open Image", fg="black", padx=5, width=5, height=2, command=lambda: self.open_image(self.pix_info.get_imageList()[self.current_image_index].filename))
        #openImage_button.grid(row = 1)
        openImage_button.pack(side = TOP, fill = X)
        openImage_button.bind("<Enter>", self.make_bold)
        openImage_button.bind("<Leave>", self.make_normal)

        colorCode_button = Button(self.rightFrame, text = "Color-Code Method", fg = "black", padx = 5, width = 5,height = 2)
        #colorCode_button.grid(row = 2)
        colorCode_button.pack(side = TOP, fill = X)
        colorCode_button.bind("<Enter>", self.make_bold)
        colorCode_button.bind("<Leave>", self.make_normal)       

    #---------------------------------------------------------------------------------------
        #                                           BOTTOM FRAME
        # Create a frame at the bottom for results
        # The purpose of this is to house the results of the image comparison
        #Create a horizontal scrollbar
    
        # Create a frame at the bottom for results
        # The purpose of this is to house the results of the image comparison
        self.bottomFrame = Frame(self, bg='#E8F5EF', width=800, height=100)
        self.bottomFrame.pack(side=tk.BOTTOM, fill=tk.X)  # Changed to fill=tk.X

        # Create a canvas inside the bottom frame
        self.bottomCanvas = Canvas(self.bottomFrame, bg='#E8F5EF', height=100)  # Set height
        self.bottomCanvas.pack(side=LEFT, fill=X, expand=True)  # Changed to fill=X

        # Create a horizontal scrollbar and associate it with the canvas
        self.bottomScrollbar = Scrollbar(self.bottomFrame, orient=HORIZONTAL, command=self.bottomCanvas.xview)
        self.bottomScrollbar.pack(side=BOTTOM, fill=X)  # Changed to fill=X
        self.bottomCanvas.config(xscrollcommand=self.bottomScrollbar.set)

        # Create a frame inside the canvas to hold other widgets
        self.bottomInnerFrame = Frame(self.bottomCanvas, bg='#E8F5EF')
        self.bottomCanvas.create_window((0, 0), window=self.bottomInnerFrame, anchor='nw')

        # Update the scroll region to fit the inner frame
        self.bottomInnerFrame.bind('<Configure>', lambda e: self.bottomCanvas.config(scrollregion=self.bottomCanvas.bbox('all')))  

    #---------------------------------------------------------------------------------------
        self.pack()
        
    def populate_images(self):
         row, col = 0, 0
         for i, photo in enumerate(self.pix_info.get_photoList()):
        # Resize the image to a fixed size (e.g., 100x100 pixels)
            img = Image.open(self.pix_info.get_imageList()[i].filename)
            img = img.resize((100, 100), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            # Create a label for the image and place it in the grid
            img_label = Label(self.innerFrame, image=img)
            img_label.image = img  # Keep a reference to avoid garbage collection
            img_label.image_index = i  # Save the index to the label
            img_label.grid(row=row * 2, column=col)  # Multiply row by 2 to leave space for filenames
            img_label.filename = self.pix_info.get_imageList()[i].filename  # Save the filename to the label
            img_label.bind('<Button-1>', self.on_image_click)  # Bind click event

            # Create a label for the filename and place it under the image
            filename_label = Label(self.innerFrame, text=os.path.basename(img_label.filename), wraplength=100)
            filename_label.grid(row=row * 2 + 1, column=col)

            col += 1
            if col > 4:
                col = 0
                row += 1
   #---------------------------------------------------------------------------------------
   #this is the method when we click the image, it displays on the right side
    def on_image_click(self, event):
        clicked_label = event.widget
        self.current_image_index = event.widget.image_index 
        image_filename = clicked_label.filename

        # Retrieve the actual PIL Image object using the filename
        selected_image = Image.open(image_filename)

        # Get original dimensions
        original_width, original_height = selected_image.size

        # Define scale factor
        scale_factor = 0.5

        # Calculate new dimensions
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        # Resize the image
        selected_image_resized = selected_image.resize((new_width, new_height), Image.LANCZOS)
        selected_image_tk = ImageTk.PhotoImage(selected_image_resized)

        # Update the label
        self.selected_image_label.config(image=selected_image_tk)
        self.selected_image_label.image = selected_image_tk 
    #---------------------------------------------------------------------------------------  
    # Mouse wheel scroll        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")               
    #---------------------------------------------------------------------------------------
    def open_image(self, filename):
        os.startfile(filename)
    #---------------------------------------------------------------------------------------
    def make_bold(self, event):
        event.widget.config(font=("Helvetica", "10", "bold"))

    def make_normal(self, event):
        event.widget.config(font=("Helvetica", "10"))
    #---------------------------------------------------------------------------------------

# main function    
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Image Viewer")
    
    root.resizable(False, False)
    pictureInfo = PixInfo(root)
            
    gui = GUI(root, pictureInfo)
    root.mainloop()
