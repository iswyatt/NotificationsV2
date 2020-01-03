import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
import random
from PIL import Image, ImageTk
import os 
os.system('cls')


class Scrollable_Canvas():
    def __init__(self, context, x_place, y_place, width_of_scrolling_window, height_of_scrolling_window ):
        print("Scrollable_Canvas ")
        self.context = context
        self.x_place = x_place
        self.y_place = y_place
        self.width_of_scrolling_window  = width_of_scrolling_window
        self.height_of_scrolling_window = height_of_scrolling_window
        ### def sb_process_070(context, x_place, y_place):
        # the width and height of frame as no effect,
        # use the dimentions of the canvas values.  
        self.frame_main_1 = tk.Frame( context)
        self.frame_main_1.place( x = x_place, 
                                 y = y_place )
        self.frame_main_1.grid_propagate(False)
        ### def sb_process_072(frame_main_1):
        # Add a canvas in that frame
        self.canvas = tk.Canvas(self.frame_main_1, bg="dark slate grey")
        ### def sb_process_172(frame_main_1, canvas):
        # Link a scrollbar to the canvas
        self.vsb = tk.Scrollbar( master  = self.frame_main_1, 
                                 orient  = "vertical", 
                                 command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.vsb.set)
        ### def sb_process_176(canvas):
        # Make a scrollable frame linked to the canvas
        # and a window in the canvas holding the scrollable frame
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind( "<Configure>", 
                                    lambda e: self.canvas.configure( scrollregion=self.canvas.bbox("all") ))
        self.canvas.create_window((0, 0), window = self.scrollable_frame, anchor="nw")
        ### def sb_process_295(vsb, canvas):
        self.context.update_idletasks()
        # height_of_scrolling_window = 500
        self.width_of_scrolling_window = self.width_of_scrolling_window - self.vsb.winfo_width()
        self.canvas.configure( width =  self.width_of_scrolling_window, 
                               height = self.height_of_scrolling_window)
        ### def sb_process_210(vsb, canvas):
        # frame_main_1.pack()
        self.canvas.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")
        ### end of 210
        self.sb_content()
    #########################################################################    
    def sb_content(self):
                # CONTENT OF THE SCROLL FRAME GOES HERE 
        """
        Below, a image is displayed in a Label, i.e. the img_label.
        The width MAY BE limited by setting the width.
        """
        if True: # show or hide picture
            load = Image.open("Penguins.jpg")
            render = ImageTk.PhotoImage(load)
            img_label = tk.Label( self.scrollable_frame, 
                                  image = render)
            img_label.configure(width = 300)
            img_label.configure(height = 300)    
            img_label.image = render
            img_label.grid(row = 0, column = 0)  
            
        for i in range(50):
            l = tk.Label( self.scrollable_frame, 
                        text=f"{i}...in the scrollable_frame " , 
                        anchor = 'w',
                        width = 40)
            l.grid(row = i+1, column = 0, sticky = 'w')
#########################################################################
        
        
    
    
    
