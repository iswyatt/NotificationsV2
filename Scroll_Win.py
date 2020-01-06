
import loop_Timer_Module as ltm
from tkinter import *
from tkinter import ttk
import tkinter.font as font
# uses pillow the PIL import
# from PIL import Image, ImageTk
import time 
import datetime
import os 
os.system('cls')
import Canvas_Scrollable_Frame as csf
import Input_Bindings_Class as ibc
import TopLevel_Win
from TopLevel_Win import gTL, TopLevelWindow
# import active_CAS7 as ac
# from MyEnumerations import e
# import math
# from threading import Timer
# from Configuration_Control import cc
# from Notifications_Message import temp
# import InfiniteTimer as ft

               
        

class Scroll_Window(TopLevelWindow):
    
    
    
    
    def __init__(self, window_title = 'default window title', test=0 ):
        super().__init__(window_title)
        
     #########################################################################       
        self.init_scroll_window()
        
        
    def init_scroll_window(self):
        
        self.scrollframe_width = 0 # placehoder value, updated with vsb and msg widths         
        
        delta =30

        self.s_frame = csf.Scrollable_Canvas(self, 0, gTL.tab_height, gTL.msg_width, 500)
#self.s_frame1 = csf.Scrollable_Canvas(self, gTL.msg_width+delta, gTL.tab_height, gTL.msg_width, 500)   
        # self.s_frame2 = csf.Scrollable_Canvas(self, 0, gTL.tab_height, gTL.msg_width, 500)
        # self.s_frame3 = csf.Scrollable_Canvas(self, 0, gTL.tab_height, gTL.msg_width, 500)



# TO BE DELETED                
        #self.width = self.s_frame.width_of_scrolling_msg       
#self.width = self.s_frame.cls_width_of_scrolling_msg
        
        
        ####################################################################
        # binding any configuration change, to capture window width and 
        # height infromation. 
        self.bind('<Configure>', lambda e: self.window_configure_change(event = e) )
        ####################################################################
        
        self.set_TL_width()
        self.get_width(1)   
        
    def get_width(self, fstring):
        
        self.wait_visibility()
        print('====================================================================================================')
        print(fstring)
        print(self.s_frame.frame_main_1_size)
        print('====================================================================================================')

       
        
    def call_from_child(self):
        print('call from child')  
        
        
              
    def set_TL_width(self, num_of_sf = 1): 
        # default number of scrollable frames is 1   
        if self.scrollframe_width > 0 :          
            self.geometry(  f'{self.scrollframe_width * num_of_sf}x{self.winfo_height()}'  )
           
    def window_configure_change(self, event):
        """
        The recieved event data is as follows:
        <Configure event x=1375 y=222 width=374 height=498>
        The event.height value goes krezzy with scrolling,
        use the winfo_xxxx values, updated here with the <Configure> binding
        """
        print(f' config change: height: {self.winfo_height()}, width: {self.winfo_width()}')
        
        # self.s_frame.cls_height_of_scrolling_frame = self.winfo_height() - gTL.tab_height - gTL.win_border
        csf.Scrollable_Canvas.cls_height_of_scrolling_frame = self.winfo_height() - gTL.tab_height - gTL.win_border
               
        self.s_frame.update_canvas()
        # self.s_frame1.update_canvas()
        
        
