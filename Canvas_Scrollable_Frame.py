# import tkinter as tk
from tkinter import ttk
from tkinter import *
import random
from PIL import Image, ImageTk
import os 
os.system('cls')

class Tabs(): 
    def __init__(self, context, place_x, place_y, width, height):
        self.context = context,
        self.width = width
        self.height = height
        mcolor = '#%06x' % random.randint(0, 0xFFFFFF)

        self.tab_frame = Frame( master = context, 
                                width  = self.width,
                                height = self.height ,
                                highlightbackground="green", 
                                highlightcolor="green", 
                                highlightthickness=1,
                                bg = mcolor
                                )        

class Scrollable_Canvas():
    cls_num_of_tabs = 4
    cls_width_of_scrolling_msg = 0  # message width without the 
    cls_vsb_width = 0               # width of the scrollbar
    cls_width_of_scrolling_frame = 0   # total width, messages and the vsb
    cls_height_of_scrolling_frame = 0  # height of the scrolling messages(i.e. the vsb height)
    cls_tab_height = 20             # height of the selector tabs 
    cls_top_label_height = 15       # height of the label just below the tabs
    cls_top_frame_height =  600     # cls_tab_height + cls_top_label_height   
                                   
    
    def __init__(self, context, x_place, y_place, width_of_scrolling_msg, height_of_scrolling_frame ):
        ######## class variables ################
        Scrollable_Canvas.cls_num_of_tabs += 1
        print(f"Scrollable_Canvas # {Scrollable_Canvas.cls_num_of_tabs}")
        self.context = context
        self.x_place = x_place
        self.y_place = y_place
        
        Scrollable_Canvas.cls_width_of_scrolling_msg  = width_of_scrolling_msg
        
        Scrollable_Canvas.cls_height_of_scrolling_frame = height_of_scrolling_frame
        
#self.scrollframe_width = IntVar() # callback when scroll_frame is updated, call_parent()
        
        # the width and height of frame as no effect,
        # use the dimentions of the canvas values.  
        self.frame_main_1 = Frame( self.context)
        self.frame_main_1.place( x = x_place, 
                                 y = y_place )
        self.frame_main_1.grid_propagate(False)
        ### def sb_process_072(frame_main_1):
        # Add a canvas in that frame
        self.canvas = Canvas(self.frame_main_1, bg="dark slate grey")
        ### def sb_process_172(frame_main_1, canvas):
        # Link a scrollbar to the canvas
        self.vsb = Scrollbar( master  = self.frame_main_1, 
                              orient  = "vertical", 
                              command = self.canvas.yview)
        
        self.canvas.configure(yscrollcommand = self.vsb.set)
        ### def sb_process_176(canvas):
        # Make a scrollable frame linked to the canvas
        # and a window in the canvas holding the scrollable frame
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind( "<Configure>", 
                                    lambda e: self.canvas.configure( scrollregion=self.canvas.bbox("all") ))

        self.canvas.create_window( (0, 0), 
                                   window = self.scrollable_frame, 
                                   anchor="nw")
        ### def sb_process_295(vsb, canvas):
        ### Geometry calculation moved to be accomplished after the content is produced. 
        ### If done earler, the vsb width is not correct. 
        #####################################################################
        ### pack canvas and scrollbars, geometry updated after content
        self.canvas.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")
        ### end of 210
        ##################
        self.sb_content()  ## PLACE THE SCROLLING MESSAGES IN THIS METHOD
        ##################
        self.set_inital_geometry()
        self.update_canvas()
        self.call_parent()
        self.init_tabs()
    ######################################################################### 
    def init_tabs(self):
        self.tb =   Tabs(   context = self.context,
                            place_x =  0,
                            place_y = 0,
                            width = Scrollable_Canvas.cls_width_of_scrolling_frame,
                            height = 30  )
    ######################################################################### 
        self.tb.tab_frame.place( x = self.x_place, y = 0  )

    def call_parent(self):
        print('call parent')
        ## this tells the parent that the scrollframe width is set. UPDATE, NOT NECESSARY
        self.context.call_from_child()  
        
        
    def set_inital_geometry(self):
        self.context.update_idletasks()
        Scrollable_Canvas.cls_vsb_width = self.vsb.winfo_width() 
        ### set the sf with in the parent toplevel window  
        Scrollable_Canvas.cls_width_of_scrolling_frame  = Scrollable_Canvas.cls_width_of_scrolling_msg + Scrollable_Canvas.cls_vsb_width    
        self.context.scrollframe_width = Scrollable_Canvas.cls_width_of_scrolling_frame
        
    def update_canvas(self):
        ### Each instance of the canvas must be updated with the class variables,
        ### for that reasion a cls @classmethod method will not work
        ### this method is called whenever there is a window <Configure> charge from binding       

        # self.canvas.configure( width =  Scrollable_Canvas.cls_width_of_scrolling_msg, 
        #                        height = Scrollable_Canvas.cls_height_of_scrolling_frame)

        self.canvas.configure( width =  Scrollable_Canvas.cls_width_of_scrolling_frame, 
                               height = Scrollable_Canvas.cls_height_of_scrolling_frame)

   
         
    def sb_content(self):
        # CONTENT OF THE SCROLL FRAME GOES HERE 
        """
        Below, a image is displayed in a Label, i.e. the img_label.
        The width MAY BE limited by setting the width.
        """
        if False: # show or hide picture
            load = Image.open("Penguins.jpg")
            render = ImageTk.PhotoImage(load)
            img_label = Label( master = self.scrollable_frame, 
                                  image  = render)
            img_label.configure(width = 300)
            img_label.configure(height = 300)    
            img_label.image = render
            img_label.grid(row = 0, column = 0)  
            
        for i in range(150):
            mcolor = '#%06x' % random.randint(0, 0xFFFFFF)
            label_frame = Frame( master = self.scrollable_frame,
                                    width  = 300, 
                                    height = 30, 
                                    bg     = mcolor)
            label_frame.grid(row = i+1, column = 0, sticky = 'w')
            
            label_frame.pack_propagate(0)           
            
            label = Label(   master = label_frame, 
                                text=f"{i}...in the scrollable_frame " , 
                                anchor = 'w',
                                width = 24)
            label.pack_propagate(0)
            label.pack( fill='none',
                        side = 'left')
                        
#########################################################################
        
if __name__ == "__main__":  
    root = Tk()      
    
    temp = Scrollable_Canvas(root, 0,0,300,600)
    
    mainloop()
    
