import loop_Timer_Module as ltm
from tkinter import *
from tkinter import ttk
import tkinter.font as font
# uses pillow the PIL import
from PIL import Image, ImageTk
import time 
import datetime
import os 
os.system('cls')
import active_CAS7 as ac
from MyEnumerations import e
import math
from threading import Timer
from Configuration_Control import cc
from Notifications_Message import temp
import InfiniteTimer as ft


win1 = object
win2 = object

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
        
        
# class Messages:
#     def __init__(self, contex = None,  msg_point = (0,0)): 
#         contex = contex                
#         mv = Canvas(contex) 
#         mv.configure(width  = gTL.message_rect[2]-10)
#         mv.configure(height = gTL.message_rect[3])
#         mv.configure(highlightthickness = 0)
#         mv.configure(background = 'white')
#         mv.configure(relief = GROOVE)
#         cas_font= font.Font(family = 'ClearviewADA', size = 20, weight = 'normal')        
#         txt = "this is text need descender gqtypj"  
#         mv.create_text(20,                             # x position of the msg text
#                     3,                                      # y position of the msg text
#                     fill   = 'blue',                       # text color
#                     font   =  cas_font,
#                     text   = txt,    # text string
#                     anchor = 'nw'  )                
        
        
               
class TopLevelWindow(Toplevel):
    def __init__(self, window_title = 'default window title'):
        super().__init__()
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
        
        
        
        
        
    def Init_Messages(self):
        mes = Messages(self, (0,0) )
        
    def Test_Print(self):
        print('does test print work???????????????????')








def create_win2( ):
    global win2
    win2 = TopLevelWindow( window_title = 'TopLever Win2')  
    print(id(win2))
    return win2   

def create_win1( ):
    global win1
    win1 = TopLevelWindow(window_title = 'TopLever Win1')   
    print(id(win1))
    return win1   

  
# ############################################## 
# def Create_Win1():
#     Win1 = Toplevel(    bg = 'black',
#                         height   =   800,
#                         width    =   300  )
#     Win1.title('New window Win1')
#     Win1.geometry('533x1080+1000+100')
#     Win1.resizable(0,0)
    
##############################################
# win1=TopLevelWindow()
