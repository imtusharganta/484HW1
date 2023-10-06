import tkinter as tk
from tkinter import *
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
        
        #main frame of the GUI
        guiFrame = Frame(master)
        guiFrame.pack()
        
    #----------------------------------------------------------------------------------------
        #                                          LEFT FRAME
        #
        # Create the left frame that will take up 2/3 of the GUI
        # The purpose of this is to house all of the images
        self.leftFrame = Frame(guiFrame, bg='#F4F7E8', width=525, height=300)
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
        self.rightFrame = Frame(guiFrame, bg='#EAE5DC', width=275, height=300)
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

        intensity_button = Button(self.rightFrame, text = "Intensity", fg = "black", padx = 5, width = 5, height = 2)
        #intensity_button.grid(row = 0)
        intensity_button.pack(side = TOP, fill = X)

        #button works, still need to figure out how to open selected image
        openImage_button = Button(self.rightFrame, text = "Open Image", fg = "black", padx = 5, width = 5, height = 2, command=lambda : self.open_image(pix_info.get_imageList()[0].filename))
        #openImage_button.grid(row = 1)
        openImage_button.pack(side = TOP, fill = X)

        colorCode_button = Button(self.rightFrame, text = "Color-Code", fg = "black", padx = 5, width = 5,height = 2)
        #colorCode_button.grid(row = 2)
        colorCode_button.pack(side = TOP, fill = X)

    #---------------------------------------------------------------------------------------
        #                                           BOTTOM FRAME
        # Create a frame at the bottom for results
        # The purpose of this is to house the results of the image comparison
        self.bottomFrame = Frame(self, bg='#E8F5EF', width=800, height=100)
        self.bottomFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand = True)  
        
        
        

        #Create a horizontal scrollbar
        bottom_scroll = Scrollbar(self.bottomFrame, orient=HORIZONTAL)
        bottom_scroll.pack(side=BOTTOM, fill = X)
        #bottom_Scroll.config(command=text.xview) -- "text" being the area with the results
        

    #---------------------------------------------------------------------------------------
        self.pack()
        
    def populate_images(self):
        row, col = 0, 0
        for i, photo in enumerate(self.pix_info.get_photoList()):
            img_label = Label(self.innerFrame, image=photo)
            img_label.grid(row=row, column=col)
            img_label.filename = self.pix_info.get_imageList()[i].filename  # Save the filename to the label
            img_label.bind('<Button-1>', self.on_image_click)  # Bind click event

            col += 1
            if col > 4:  
                col = 0
                row += 1  
   #---------------------------------------------------------------------------------------
   #this is the method when we click the image, it displays on the right side
    def on_image_click(self, event):
        clicked_label = event.widget
        image_filename = clicked_label.filename  # Assuming you've stored the filename in the label

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
 
# main function    
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Image Viewer")
    
    root.resizable(False, False)
    pictureInfo = PixInfo(root)
            
    gui = GUI(root, pictureInfo)
    root.mainloop()
