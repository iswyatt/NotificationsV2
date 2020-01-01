
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
# import active_CAS7 as ac
# from MyEnumerations import e
# import math
# from threading import Timer
# from Configuration_Control import cc
# from Notifications_Message import temp
# import InfiniteTimer as ft


# 
# 
class Top_Level_Win_Geometry:
    def __init__(self):
        self.height = 800
        self.width  = int((4/9) * self.height)
        self.win1_geo_string = '{}x{}+1000+100'.format(self.width, self.height) 
        self.msg_width = self.width
        self.msg_height = 30
        self.message_rect = (0,0, self.msg_width, self.msg_height) 

gTL = Top_Level_Win_Geometry()






class Messages:
    def __init__(self, contex = None,  msg_point = (0,0)): 
        self.contex = contex                
        self.mv = Canvas(contex) 
        self.mv.configure(width  = gTL.message_rect[2]-10)
        self.mv.configure(height = gTL.message_rect[3])
        self.mv.configure(highlightthickness = 0)
        self.mv.configure(background = 'pink')
        self.mv.configure(relief = GROOVE)
        self.cas_font= font.Font(family = 'ClearviewADA', size = 14, weight = 'normal')        
        txt = "this is text need descender gqtypj"  
        self.mv.create_text(20,                             # x position of the msg text
                    3,                                      # y position of the msg text
                    fill   = 'blue',                       # text color
                    font   =  self.cas_font,
                    text   = txt,    # text string
                    anchor = 'nw'  )                        # anchor west LEFT justify        
        
        # self.cv.place(x = 0, y = 0)
        self.mv.place( x = msg_point[0], 
                       y = msg_point[1]  )         
        # self.mv.pack()   
               
        
        
               
class TopLevelWindow(Toplevel):
    """
    The Toplevel window CANNOT be created prior to the main root window,
    or strange thing will happen.
    """
    def __init__(self, window_title = 'default window title' ):
        super().__init__()
        # self.parent_window = parent_window
        self.configure (bg = '#333333')
        self.title(window_title)
        self.geometry(gTL.win1_geo_string)
        self.resizable(0,0)
        self.msg_frames = []
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack( side = RIGHT,
                             fill = Y)
        self.msg_canvas = Messages(self, (0,100))
        # attach  to scrollbar
        self.msg_canvas.mv.config( yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(     command        = self.msg_canvas.mv.yview)
        ####################################################################
        """
        The Boolvar trace method causes the show_hide_toggle to be called 
        ANYTIME it is set(). This caused some rece problems with the wm_state() status
        of the toplevel windows and the value of the Boolvar. This was fixed show_hide_toggle 
        method by checking that Boolvar and wm_state matached PRIOR to toggling the toplevel
        windows state.
        """
        self.bv_window_status = BooleanVar()
        self.bv_window_status.trace( mode = 'w', 
                                     callback = self.show_hide_toggle ) 
        #####################################################################
        # wm_protocols to intercept various windows control messages.        
        # Use the 'X' pressed in window to minimize the window, not destroy it. 
        # self.wm_protocol('WM_DELETE_WINDOW', self.iconify())
        """
        The wm_protocol('WM_DELETE_WINDOW', ...) works when in the init method,
        it does not seem to work from the main root path.
        """
        self.wm_protocol('WM_DELETE_WINDOW', self.hide )
        
    def hide(self):
        # the change in the bv_window_status (trace) causes the show_hide_toggle be 
        # called, since the wm_state and Boolvar match, the toggle does not occore. 
        self.wm_iconify()
        self.bv_window_status.set(False)
       
    def show_hide_toggle(self, *argv):
        # do nothing is the Boolvar and wm_state match, otherwis toggle the window
        if (self.wm_state() == 'normal') and (self.bv_window_status.get()==True):
            return 
        if (self.wm_state() == 'iconic') and (self.bv_window_status.get()==False):
            return 
        #print(f'bv_window_status: {self.bv_window_status.get()}, self.wm_state(): {self.wm_state()} ')        
        # TOGGLE,  Change the window state and set the Boolvar to match
        if self.wm_state() == 'normal':
            self.wm_iconify()
            self.bv_window_status.set(False)
        else:
            self.wm_state('normal')
            self.bv_window_status.set(True)
        #print(f'bv_window_status: {self.bv_window_status.get()}, self.wm_state(): {self.wm_state()} ')        
        
        
    def Test_Print(self):
        print( f"self.winfo_geometry():= {self.winfo_geometry()} ")
        
"""
NOTE, from documentation
wm_state()     window ?newstate?
If newstate is specified, the window will be set to the new state, 
otherwise it returns the current state of window: 
either normal, iconic, withdrawn, icon, or (Windows and Mac OS X only) zoomed. 
The difference between iconic and icon is that iconic refers
to a window that has been iconified (e.g., with the wm iconify command)
while icon refers to a window whose only purpose is to serve as the icon 
for some other window (via the wm iconwindow command). The icon state cannot be set.
"""