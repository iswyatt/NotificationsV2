
import loop_Timer_Module as ltm
from tkinter import *
# from tkinter import ttk
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

import TopLevel_Win as tl

import MainWindowMenu as mwm

from Scroll_Win import Scroll_Window

from TIU_Window import TIU_Window

import Canvas_Scrollable_Frame as csf
##############################################
root = Tk()
##############################################

# 12-19 1644
# 12-30 0646 All files are recomitted, missing graphics error seems to have been resolved
#            with new clone as of 12-29
# 12-30 updates:
# 01/11/2020 reference row 5--38
class gv_global:
    def __init__(self):
        # Three values determin the size of the main window
        # the switch height and the size of the CAS window image
        # masured of select arbitray pixcel values, all othes are referenced to these
        self.CAS_Image_Width        = 533 # measured size of 1/6th window graphic in pixcels
        self.CAS_Image_Height       = 640
        self.CAS_frame_tpt          = (33,30)
        self.CAS_frame_bpt          = (472,299)       
        ###################################################################################                      
        self.height_of_swithes      = 90
        self.statusbar_height       = 12 # pixcels, indicate as a -height to be in pix
        # the number of cas messages in the cas frame
        self.possable_num_of_CASMsg = 10
        # the time in seconds to automaticely ack an ALERT CAS message
        self.ALERT_msg_auto_ack = 10 #seconds
        self.MessageController_1Sec_Loop_Timer_Running = False
        self.Notification_Animation_Timer_Running = False
        ##################################################################################
        ########### screen Tuples filled in the scroll method ##########################
        self.HTuple =   (0,0,0,0,0,0,0,0)     #tuple # off screen high CAS count
        self.STuple =   (0,0,0,0,0,0,0,0)     #tuple # on screen CAS count
        self.BTuple =   (0,0,0,0,0,0,0,0)     #tuple # off screen below CAS count
        # self.CASTuple = (0,0,0,0,0,0,0,0)     #tuple # of ALL CAS message, 
        self.AllowScrolling = False         # red CAS can't be scrolled, controlls CCue
        self.event_adder = 0 # global scroll direction indicator, mouse wheel event driven
        ##################################################################################
        self.ImageSize    = (self.CAS_Image_Width, self.CAS_Image_Height)
        
        self.root_geometry = ( '{}x{}'.format( self.ImageSize[0], 
                                self.ImageSize[1]+self.height_of_swithes+self.statusbar_height*2 )) 
              
        self.MasterSwSize = (self.ImageSize[0], self.height_of_swithes)
        
        self.MasterSwRect = ( 0,
                              0,
                              self.MasterSwSize[0],
                              self.height_of_swithes )
       
        self.ImageRect    = ( 0, 
                              self.height_of_swithes,
                              self.ImageSize[0],
                              self.ImageSize[1] + self.height_of_swithes) 
        
        # a constructed rectangle for the 10 cas messages
        self.CAS_frame_rect = (self.CAS_frame_tpt[0], 
                               self.CAS_frame_tpt[1], 
                                abs(self.CAS_frame_tpt[0]-self.CAS_frame_bpt[0]),
                                abs(self.CAS_frame_tpt[1]-self.CAS_frame_bpt[1]) )
        
        # the Rect for each of the individual cas messages, given the space the the possable number
        self.msgHeight = (float(self.CAS_frame_rect[3])/float(self.possable_num_of_CASMsg)) # pixcels
        
        # the Rect for each individual cas message 
        # relitive to the CAS_frame_rect
        # the individual messages will be clipped if drawn outside 
        # of the CAS_frame_rect      
        self.msg_rect = ( 0, 
                          0, 
                          self.CAS_frame_rect[2],  
                          self.msgHeight)
        ############### The number of displable CAS messages and the list ###############
        self.canvas_list = []
        self.num_in_screen_list = self.possable_num_of_CASMsg # 0..9
        ###############
        # points where the messages will be displayed
        # the points are in a Dictionary where the top point is
        # {0:Point(...), .... }
        self.canvas_pt_dict = {} 
        #################################################################################
        # Notification Retangle
        self.Notification_i_rect = (0,0,0,0)
        #################################################################################        
        ########### set up the fonts and the locations on the canvas ####################
        self.cas_font         = font.Font(family = 'ClearviewADA', size = 20, weight = 'normal')
        self.noti_font        = font.Font(family = 'ClearviewADA', size = 18, weight = 'normal',
                                           slant = 'italic')
        self.but_font         = font.Font(family = 'ClearviewADA', size = 13, weight = 'bold'  )
        self.frame_label_font = font.Font(family = 'ClearviewADA', size = 11, weight = 'bold') 
        self.sym_font         = font.Font(family = 'ClearviewADA', size = 16, weight = 'normal')   
        self.sym_Noti_flag    = font.Font(family = 'Arial Narrow', size = 16, weight = 'normal')        
        ### CAS text ####################################################################
        font_ascent_scaler = 0.6
        self.cas_text_y = self.cas_font.metrics()['ascent'] * font_ascent_scaler
        self.cas_text_x = 1
        self.cas_center_text = self.msg_rect[2]/2
        ### notation text ##############################################################
        self.noti_text_y = self.noti_font.metrics()['ascent'] * font_ascent_scaler
        self.noti_text_x = 3 
        self.cas_canvas_created_and_on_screen = False
        #############################################
gv = gv_global()
#########################################################################################
# This function respons to pressing one of the Master Buttons to acknowlege messages by 
# calling the activeCAS Acknowlege function. 
# Status is true from 
def MasterButtonCallback(bt_id, status):
    if status == True:
        ac.Ackknowlege_CAS(bt_id)
    appWin.ScrollCAS(0)
    appWin.MessageController()
    
    if bt_id == e.id_NOTIFICATION:
        # nt.Animation()
        For_Test()
         
################################################################################
class MasterButton(Button):
    # These are the button in the upper section of the main window
    def __init__(self, bn_frame, id, bn_text, active_color, inactive_color): #, Icallback):
        Button.__init__(self, bn_frame )
        self.bn_frame = bn_frame
        self.id = id
        self.bn_text  = bn_text
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.displayed_colors = self.inactive_color
        self.active_status = False

     
        self.bn_geometry = (12, 2 , 5, 15) #button geomerty(width, height, borderwidth, padx)                  
        self.configure( font        = gv.but_font )
        self.configure( width       = self.bn_geometry[0])
        self.configure( height      = self.bn_geometry[1])
        self.configure( borderwidth = self.bn_geometry[2])
        self.configure( padx        = self.bn_geometry[3])
        self.configure( text        = self.bn_text)
        self.configure( command     = self.bn_callback) # this calls the passed-in callback
        
    def SetStatusActive(self, active_status ):
        self.active_status = active_status
        if self.active_status == True:
            self.displayed_colors = self.active_color
        else: 
            self.displayed_colors = self.inactive_color
        # configure the button colors according to the buton status
        self.configure(background          = self.displayed_colors[0])
        self.configure(activebackground    = self.displayed_colors[1])        
        self.configure(foreground          = self.displayed_colors[2]) # text color
        # send the sataus with the button id to the external 
        # global Function def MasterButtonCallback(bt_id, status):
        # self.Icallback( self.id, self.active_status )              
        return self.active_status
    
    def bn_callback(self):
        # Each MasterButton class instance takes the mouse action itself (the button click) 
        # and passes the action on to the MasterButtonCallback
        MasterButtonCallback(self.id, self.active_status)
##############################################################################
class ScrollCanvas():
    def __init__(self, contex,  rect ):
        # rect is pt.x, pt.y, width, height
        self.contex = contex
        self.rect = rect                
        self.sv = Canvas(contex)       
        ######################################################
        self.sv.configure(width  = self.rect[2])
        self.sv.configure(height = self.rect[3])
        self.sv.configure(highlightthickness = 0)
        self.sv.configure(background = 'black')
        self.sv.place(  x = self.rect[0], 
                        y = self.rect[1]  )
        #### Up and Down Arrow Shapes ##################
        a = 13 # length of arrow lines
        b = math.sqrt(0.75)*a
        delx = 29
        dely = 4
        self.up_arrow   = (0+delx, b+dely,    a+delx, b+dely,        (a/2)+delx, 0+dely)
        self.down_arrow = (0+delx, 0+dely,    (a/2)+delx, b+dely,    (a)+delx, 0+dely)
        n_b = 3
        self.Notificaton_cyan_rect = ( 0 + n_b,
                                            0 + n_b,
                                            gv.Notification_i_rect[2] - 1*n_b,
                                            gv.Notification_i_rect[3] - 1*n_b                  )
        
        ##### load all of the CCue images and class variable, created at initilization
        self.Current_image_index = 0 # move up or down referenced to the CAS massage scrolling direction
        self.CCueImage = []
        self.CCueImage.append( Image.open('CCue_360_20.png') )
        self.CCueImage.append( Image.open('CCue_060_20.png') )
        self.CCueImage.append( Image.open('CCue_120_20.png') )
        self.CCueImage.append( Image.open('CCue_180_20.png') )
        self.CCueImage.append( Image.open('CCue_240_20.png') )
        self.CCueImage.append( Image.open('CCue_300_20.png') )
        ### NOTIFICATION GRAPHIC #############
        self.Notification_flag = Image.open('stipple_only_50_100x100.png')
        self.sv.Notification_image = ImageTk.PhotoImage( self.Notification_flag )

    def draw_NOTIFICATION_FLAG(self, sIndication ):
        self.sv.configure( background = 'black' ) 
        self.sv.delete('all') 
        if (int(sIndication) >=2):
            # the number of notification messages must be greater that one 
            # to show the notification flag. 
            #notification stippled image is displayed, and then over it is a cyan 
            # retangle wher the number of hidden messages is indicated. 
            self.sv.create_image(  0, 0, 
                                   image =  self.sv.Notification_image,
                                   anchor='nw'  )            
            #Cyan rectangle overlaying the stippled image
            self.cyan_NRectangle = self.sv.create_rectangle(  self.Notificaton_cyan_rect, 
                                                              outline = 'cyan',  
                                                              fill    = 'cyan' )
            # test format to show the number of messages on-deck with 1 or number
            Noti_1_of_num = '1/{}'.format(sIndication) # can only be one charactor long                                                              
            y_spaceing = 6
            x_spaceing = 8 
            self.sv.create_text(
                x_spaceing,                      # x position of the msg text
                y_spaceing,                      # y position of the msg text
                fill   = 'black',                # text color
                text   = Noti_1_of_num,          # text string
                font   = gv.sym_Noti_flag,       # the font defined in gv and above if-else
                anchor = 'nw'  )                 # anchor west LEFT justify  
            down_triangle = self.sv.create_polygon(  self.down_arrow, outline = 'black', fill = 'black' )
            self.sv.move(down_triangle, -12, 30)
        else:
            return 


    def Update(self, color = ('yellow', 'black'), sIndication = '   ', draw = ''):  
        # "draw = " pass additional information: draw up or dow arrow, notification graphic etc.
        if (draw == 'NOTIFICATION_FLAG'):
            #self.draw_NOTIFICATION_FLAG( sIndication )
            return
                         
        elif draw == 'CCue':
            if gv.AllowScrolling == True:
                # if it is the curlley-cue place place the image into the Canvas.
                # loop through class images 
                #####################
                self.Current_image_index = self.Current_image_index + gv.event_adder
                if self.Current_image_index > 5:
                    self.Current_image_index = 0
                if self.Current_image_index < 0:
                    self.Current_image_index = 5
                # Put the image into a canvas compatible class, and stick in an
                # arbitrary variable to the garbage collector doesn't destroy it
                self.sv.image = ImageTk.PhotoImage( self.CCueImage[self.Current_image_index] )
                # Add the image to the canvas, and set the anchor to the top left / north west corner
                self.sv.create_image(8, 0, image=self.sv.image, anchor='nw')
            else:
                # the old CCue must be erased so that the atea will be blank 
                self.sv.configure( background = 'black' ) 
                self.sv.delete('all') 
            #####################
        else: # draw the amber, white numbers with the approprate arrow
            # determin if it is an up or down arrow
            self.sv.configure( background = color[0] ) 
            self.sv.delete('all') 
            # determin if it is an up or down arrow
            if draw == 'UP_ARROW':
                self.up_triangle = self.sv.create_polygon(  self.up_arrow, outline = color[0], fill = color[1] ) 
            elif draw == 'DOWN_ARROW':
                self.down_triangle = self.sv.create_polygon(  self.down_arrow, outline = color[0], fill = color[1] )          
            self.sv.create_text(
                4,                      # x position of the msg text
                -3,                     # y position of the msg text
                fill   = color[1],      # text color
                text   = sIndication,   # text string
                font   = gv.sym_font,   # the font defined in gv and above if-else
                anchor = 'nw'  )        # anchor west LEFT justify   
############################################################################
############################################################################            
class Scroll_Indicator():
    def __init__(self, contex):
        # creates the indicators canvases and the notification flag canvas
        # and the CCue canvas.
        self.m_contex = contex 
        pad = 10
        m_NoOfCanvas=   6        
        m_Added_height_for_notifications = 34.8
        m_Height    =   (gv.CAS_frame_bpt[1] - gv.CAS_frame_tpt[1])/2

        m_Width     =   gv.CAS_Image_Width - ( gv.CAS_frame_bpt[0] + int(pad *1.7))   #50               
        self.m_pt   =   (gv.CAS_frame_bpt[0] + pad, gv.CAS_frame_bpt[1] - m_Height - m_Added_height_for_notifications+3)
   
        self.Scroll_cv_list = []
        ############################################################
        self.m_Scroll_rect  =   (   self.m_pt[0], 
                                    self.m_pt[1], 
                                    m_Width, 
                                    m_Height + m_Added_height_for_notifications  )
     
        self.m_Scroll_frame =   Frame(  self.m_contex,
                                        width   = self.m_Scroll_rect[2],
                                        height  = self.m_Scroll_rect[3],                                   
                                        bg      = 'black'  )
        
        self.m_Scroll_frame.place(      x       = self.m_Scroll_rect[0],
                                        y       = self.m_Scroll_rect[1]    )
        #############################################################        
        self.m_Scroll_Canvas_size=   (m_Width, m_Height/m_NoOfCanvas)               
        for i in range( m_NoOfCanvas ):                                                      
            i_offset = i * self.m_Scroll_Canvas_size[1] 
            ############ 
            i_rect = (  0, 
                        i_offset,
                        self.m_Scroll_Canvas_size[0],
                        self.m_Scroll_Canvas_size[1]    )   
            ############
            # Make the last canvas bigger for the notification flag
            if i == (m_NoOfCanvas - 1):
                gv.Notification_i_rect = (  0, 
                            i_offset,
                            self.m_Scroll_Canvas_size[0],
                            self.m_Scroll_Canvas_size[1] + m_Added_height_for_notifications )  
            
                self.Scroll_cv_list.append( ScrollCanvas(   self.m_Scroll_frame, 
                                                            gv.Notification_i_rect  )  ) 
            ############
            else:
                self.Scroll_cv_list.append( ScrollCanvas(   self.m_Scroll_frame, 
                                                            i_rect  )  )     
                
    #######################################################################################
    #######################################################################################
    def UpdateScrollIndicator(self): 
        # called from MasterController and when the CAS messages are scrolled
        # according to the values in the H+B Tuple the individual scroll
        # canvas are updated by the update function
        sColor =  ('black', 'black')   #(  bachground, text color )   
        # up \u00AD or \u0044, dn \u00AF or \u00D1 
        self.Scroll_cv_list[e.sCURLY_CUE].Update( color         = ('cyan', 'cyan'), 
                                                  sIndication   = '    ',
                                                  draw          = 'CCue'          )
        ################
        # ALERT White above          
        num_of_msg = gv.HTuple[e.ALERT_no] + gv.HTuple[e.ALERT_yes]
        if  num_of_msg > 0: 
               
            if  gv.HTuple[e.ALERT_no] > 0:
                sColor = ('white', 'black') #(  bachground, text color )             
            else:
                sColor = ('black', 'white')               
                 
            self.Scroll_cv_list[e.sWHITE_ABOVE].Update( color = sColor, 
                                                        sIndication = str(num_of_msg).zfill(2),
                                                        draw = 'UP_ARROW' )                                                       
        else:
            self.Scroll_cv_list[e.sWHITE_ABOVE].Update( color = sColor, 
                                                        sIndication = '   ',
                                                        draw = 'UP_ARROW'       )            
        ################ 
        # AMBER CAUTION above  
        num_of_msg = gv.HTuple[e.CAUTION_no] + gv.HTuple[e.CAUTION_yes]
        if  num_of_msg > 0:         
            if  gv.HTuple[e.CAUTION_no] > 0:
                sColor = ('yellow', 'black')  #(  bachground, text color )            
            else:
                sColor = ('black', 'yellow')                                              
            self.Scroll_cv_list[e.sAMBER_ABOVE].Update( color = sColor, 
                                                        sIndication = str( num_of_msg ).zfill(2), 
                                                        draw = 'UP_ARROW'  )            
        else:
            self.Scroll_cv_list[e.sAMBER_ABOVE].Update( color = ('black', 'black'), 
                                                        sIndication = '   '      )                 
        ################
        # WHITE Alert BELOW          
        num_of_msg = gv.BTuple[e.ALERT_no] + gv.BTuple[e.ALERT_yes]
        if  num_of_msg > 0:  
            
            if  gv.BTuple[e.ALERT_no] > 0:
                sColor = ('white', 'black')            
            else:
                sColor = ('black', 'white')   
                            
            self.Scroll_cv_list[e.sWHITE_BELOW].Update( color = sColor, 
                                                        sIndication = str( num_of_msg ).zfill(2), 
                                                        draw = 'DOWN_ARROW' )
        else:
            self.Scroll_cv_list[e.sWHITE_BELOW].Update( color = ('black', 'blue'), 
                                                        sIndication = '   '      )            
        ################
        # YELLOW CAUTION BELOW   
        num_of_msg = gv.BTuple[e.CAUTION_no] + gv.BTuple[e.CAUTION_yes]
        if  num_of_msg > 0:         
            if  gv.BTuple[e.CAUTION_no] > 0:
                sColor = ('yellow', 'black')            
            else:
                sColor = ('black', 'yellow')                                              
            self.Scroll_cv_list[e.sAMBER_BELOW].Update( color = sColor, 
                                                        sIndication = str( num_of_msg ).zfill(2),
                                                        draw = 'DOWN_ARROW'  )            
        else:
            self.Scroll_cv_list[e.sAMBER_BELOW].Update( color = ('black', 'black'), 
                                                        sIndication = '   '      )  
        ################
        # NOTIFICATION
        # total number of Notification messages
        num_of_msg = abs( gv.BTuple[e.TOTAL_NO_MSG] - gv.BTuple[e.END_of_CAS_MSG] )
        if num_of_msg > 0:
            sColor = ( 'cyan', 'black')
        else:
            sColor = ('cyan', 'cyan')   
        self.Scroll_cv_list[e.sNOTIFICATION].Update( color = sColor, 
                                                     sIndication = str( num_of_msg ).zfill(1) , 
                                                     draw = 'NOTIFICATION_FLAG')   
# #########################################################################################
# The CAS() class is the individual meaasages with the text background and text color.  
class CASMessage():
    def __init__(self, contex = None,  msg_point = (0,0)):
        self.contex = contex                
        self.cv = Canvas(contex)
        #######################################################
        # bind the mouse button 1 event to the CASMessage Clase
        # the Callback i.e. CancasCallback is a class method
        self.cv.bind("<Button-1>", self.CanvasCallback)
        ######################################################
        self.cv.configure(width  = gv.msg_rect[2])
        self.cv.configure(height = gv.msg_rect[3])
        self.cv.configure(highlightthickness = 0)
        self.cv.configure(background = '#330033')
        # self.cv.place(x = 0, y = 0)
        self.cv.place(x = msg_point[0], y = msg_point[1]) 
        #################################################
        # CAS Message colors by status and type
        # Background fill id [0]. text color is [1]
        self.CAS_no_ack  = {'WARNING': ('red', 'white'), 
                            'CAUTION': ('yellow', 'black'), 
                            'ALERT':   ('white', 'black'),   
                            'AA_NOTI': ('cyan', 'black') 
                           }

        self.CAS_yes_ack = {'WARNING': ('black', 'red'), 
                            'CAUTION': ('black', 'yellow'), 
                            'ALERT':   ('black', 'white'),   
                            'AA_NOTI': ('gray', 'darkgray') 
                           }
        ################################################
        # this method handles the Button 1 mouse event in the
        # CAS canvas area
    def CanvasCallback(self, event):
        if event.x < gv.msg_rect[2]/2:
            print('from canvas LEFT')
        else:
            print('from canvas RIGHT')           
        print("clicked at", event.x, event.y)
        ################################################
    def CASColors(self, active):
        if ac.active_CAS[active][2] == 'no_ACKNOWLEDGED':
            if ac.active_CAS[active][1] == 'WARNING':
                colors = self.CAS_no_ack[  'WARNING']   
                return colors
            if ac.active_CAS[active][1] == 'CAUTION':
                colors = self.CAS_no_ack[  'CAUTION']   
                return colors
            if ac.active_CAS[active][1] == 'ALERT':
                colors = self.CAS_no_ack[  'ALERT']   
                return colors
            if ac.active_CAS[active][1] == 'AA_NOTI':
                colors = self.CAS_no_ack[  'AA_NOTI']   
                return colors
            else:
                print('no_ACKNOWLEDGED ERROR'*10)
                colors = self.CAS_yes_ack[ 'AA_NOTI'] 
                return colors  
        ######################################################       
        elif ac.active_CAS[active][2]   == 'yes_ACKNOWLEDGED':
            if ac.active_CAS[active][1] == 'WARNING':
                colors = self.CAS_yes_ack[ 'WARNING']   
                return colors
            if ac.active_CAS[active][1] == 'CAUTION':
                colors = self.CAS_yes_ack[ 'CAUTION']   
                return colors
            if ac.active_CAS[active][1] == 'ALERT':
                colors = self.CAS_yes_ack[ 'ALERT']   
                return colors
            if ac.active_CAS[active][1] == 'AA_NOTI':
                colors = self.CAS_yes_ack[ 'AA_NOTI']   
                return colors
            else:
                print('yes_ACKNOWLEDGED ERROR'*10)
                colors = self.CAS_yes_ack[ 'AA_NOTI'] 
                return colors                        
        else:
            print('>>>>active_CAS ERROR<<<<'*10)     
        ###################################################### 
    def ClearMessage(self):
        self.cv.configure(background = 'black')
        self.cv.delete('all')
        
    def ENDMessage(self):
        self.ClearMessage()
        self.cv.create_text(
                            gv.cas_center_text,                 # x position of the msg text
                            gv.cas_text_y,                      # y position of the msg text
                            fill   = 'white',                   # text color
                            text   = 'END',                     # text string
                            font   = gv.noti_font,              # the font defined in gv and above if-else
                            anchor = 'c'  )                     # anchor west LEFT justify    
        
    # load and show the text in the CAS messages from the active_CAS message array           
    def ShowMessage(self, active = 0 ):
        # active the active_CAS list index number
        # the location is referenced to the massage canvas coordinates.
        # if at the end of the list 'END' is displayed
        # print('Active message is: {}'.format(active))
        # Delect will clear the canvas previous content
        # set background color to black before clearing           
        self.cv.configure(background = self.CASColors(active)[0])
        self.cv.delete('all')
        self.cv.create_text(gv.cas_text_x,                      # x position of the msg text
                            gv.cas_text_y,                      # y position of the msg text                           
                            fill   = self.CASColors(active)[1], # text color
                            text   = ac.active_CAS[active][0],  # text string
                            font   = gv.cas_font,               # the font defined in gv and above if-else
                            anchor = 'w'  )                     # anchor west LEFT justify

class MainWindow(Frame):   
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.MasterSwFrame = LabelFrame()
        self.WARNIND_bn         = object #MasterButton()
        self.CAUTION_bn         = object #MasterButton()
        self.NOTIFICATION_bn    = object #MasterButton()  
        self.WARNING_bn_status  = False
        self.CAUTION_bn_status  = False
        self.NOTIFICATION_bn_status  = False 
        self.scroll_up_down = 0 # the scroll position in the CAS window, from top of list
        
        ########### CAS message indexes for on screen and high/low off screen. ##########
        self.CAS_on_screen = (0,0) # the top and botton active_CAS messages on the screen
        self.CAS_off_screen_high = (0,0) 
        self.CAS_off_screen_low = (0,0)
        #################################################################################
        self.init_window()
        self.init_MsButtons( self.MasterSwFrame )
        self.startup_status_master_buttons()
        #################################################################################
        self.si =Scroll_Indicator( self.ImageFrame )
        self.ArrowLabel = Label(root)
        # #################################################################################
        # self.tm = mwm.Main_Window_Menu(root, self) # self being the parent_window in the menu script
        # # adding application menu
        # moved from here 12/31/2019
        #################################################################################
        
    def exit_application(self):
        # shoutdown times and distroy widgits, primarly from the menu or x commands
        MessageController_1Sec_Loop_Timer(start = False)
        Notification_Animation_Timer(start = False)
        print('wm_delete_window')
        root.destroy()
        #################################################################################
    def init_window(self):
        self.master.title("Primary Window(Frame)")
        self.configure(background = 'black')
        # setup themaster waring caution switch frame            
        self.MasterSwFrame = LabelFrame(root, width = gv.MasterSwRect[2], 
                    height = gv.MasterSwRect[3], 
                    bg     = 'gray', fg = 'black',
                    font   = gv.frame_label_font,
                    text   = "External Panel Mounted Switches", 
                    padx   = 2, 
                    pady   = 2  ) 

        self.MasterSwFrame.place( x      =   gv.MasterSwRect[0],
                                  y      =   gv.MasterSwRect[1],
                                  width  =   gv.MasterSwRect[2],
                                  height =   gv.MasterSwRect[3] )
        
        ######################################################### 
        # the Image Frame  is the placement of the 1/6 witdow graphic     
        self.ImageFrame = Frame(root,  width  =   gv.CAS_Image_Width, 
                                  height =   gv.CAS_Image_Height, 
                                  bg     =   '#5555ff')   
        self.ImageFrame.place( x       =  gv.ImageRect[0],
                               y       =  gv.ImageRect[1],    
                               width   =  gv.ImageRect[2],
                               height  =  gv.ImageRect[3] ) 
        #########################################################
        loaded_img = Image.open('CAS-black640x533.png')
        render     = ImageTk.PhotoImage( loaded_img )                                   
         # use a label control to place the image
         # into the ImageFrame, all coordinates are then local
         # to that frame.
        CAS_img = Label(self.ImageFrame, image = render)
        CAS_img.image = render
        CAS_img.place(x=0, y=0)  
        ################################################
       
        # The CASFrame is the area where the CAS messages are displayed
        # The coordinates of the internal CASFrame are 0,0 in upper left
        self.CASFrame =  Frame(  self.ImageFrame,
                            width   = gv.CAS_frame_rect[2],
                            height  = gv.CAS_frame_rect[3],
                            bg      = 'black'  ) 
         
        self.CASFrame.place( x       = gv.CAS_frame_rect[0],
                             y       = gv.CAS_frame_rect[1],
                             width   = gv.CAS_frame_rect[2],                       
                             height  = gv.CAS_frame_rect[3]  ) 
        self.CreateCASMsgCanvas()
    #####################################################
        self.StatusBar = Label(root, 
                    text= '', 
                    bd=1, 
                    anchor=W, 
                    height = -gv.statusbar_height,
                    bg = 'gray')
        self.StatusBar.pack(side=BOTTOM, fill=X)
    
    # initilize the Master buttons         
    def init_MsButtons(self, master_sw_frame):            
        active_bn_colors   = ('red','#ffcccc', 'white')
        inactive_bn_colors = ('gray', 'gray' ,'black') 
        bn_text = 'MASTER\nWARNING'
        self.WARNING_bn = MasterButton( master_sw_frame, 
                                        e.id_WARNING, 
                                        bn_text, 
                                        active_bn_colors, 
                                        inactive_bn_colors ) 
              
        self.WARNING_bn.pack(side=LEFT, expand=True, fill='both')       
        #######################################################################################       
        active_bn_colors   = ('yellow','#FFFFcc', 'black') # CAUTION active colors
        inactive_bn_colors = ('gray', 'gray' ,'black') 
        bn_text = 'MASTER\nCAUTION'
        self.CAUTION_bn = MasterButton(     master_sw_frame, 
                                            e.id_CAUTION, 
                                            bn_text, 
                                            active_bn_colors, 
                                            inactive_bn_colors)
                                            #MasterButtonCallback   ) 
              
        self.CAUTION_bn.pack(side=LEFT, expand=True, fill='both')        
        #######################################################################################
        active_bn_colors   = ('cyan','#ccFFFF','black' ) # NOTIFICATION active colors
        inactive_bn_colors = ('gray', 'gray' ,'black')
        bn_text = 'Notifications\nFMS, iNAV' 
        self.NOTIFICATION_bn = MasterButton(    master_sw_frame, 
                                                e.id_NOTIFICATION, 
                                                bn_text, 
                                                active_bn_colors, 
                                                inactive_bn_colors  ) 
               
        self.NOTIFICATION_bn.pack(side=LEFT, expand=True, fill='both')  

    ################################################################################
    # script function excuted only once to create the CAS messages canvases
    ### use the gv parameters to create the individual canvases for the CAS messages
    def CreateCASMsgCanvas(self):
        # create the canvases if first time through
        for i in range(int(gv.num_in_screen_list)):
            msg_offset = i * gv.msgHeight # the y distance down from the cas top point
            # set the individual x, y points for the CAS msg in the dictionary, 
            # key the position in the CAS window
            gv.canvas_pt_dict = {i:(gv.msg_rect[0], gv.msg_rect[1] + msg_offset )}
            # the canvas_list (array of CASMessage class) create each canvas
            gv.canvas_list.append( CASMessage(self.CASFrame, gv.canvas_pt_dict[i] ) )
            # indicate the canvases are now created
    ################################################################################
    def startup_status_master_buttons(self):
        self.WARNING_bn.SetStatusActive(False)
        self.CAUTION_bn.SetStatusActive(False)
        self.NOTIFICATION_bn.SetStatusActive(False)    
    ################################################################################        
    def MessageController(self):
        gv.CASTuple = ac.mMsg_count.Count_active_CAS()
        ############################################
        status = BooleanVar # true if an un Ack message exists.
        ### WARNING_No messages
        if gv.CASTuple[e.WARNING_no] > 0:
            status = True
        else:
            status = False
        # activate the WARNING master switch
        self.WARNING_bn_status = self.WARNING_bn.SetStatusActive(status)
        ### CAUTION_No messages               
        if gv.CASTuple[e.CAUTION_no] > 0:
            status = True
        else:
            status = False
            # activate the CAUTION master switch
        self.CAUTION_bn_status = self.CAUTION_bn.SetStatusActive(status)
        ###########################################################################
        ### ALERT WHITE CAS are auto acknowloged.
        ### ALERT_No messages 
        ### Auto acknowledge requires the MessageController loop timer to be running.
        ### If it is not by-pass the auto ack code below.
        if gv.MessageController_1Sec_Loop_Timer_Running == False:
            return # by-pass the code             
        if gv.CASTuple[e.ALERT_no] > 0:
            ack_time = time.time() - gv.ALERT_msg_auto_ack # time interval to auto ack. 
            ALERT_ACKNOWLEDGED_redraw_CAS = False # when time as expited, set to true 
            for row in ac.active_CAS:
                if (    ( row[1]=='ALERT') and 
                        ( row[2]=='no_ACKNOWLEDGED') and
                        ( row[3] <= ack_time)       ):
                    row[2] = 'yes_ACKNOWLEDGED'         # change status and en-able cas redraw
                    ALERT_ACKNOWLEDGED_redraw_CAS = True
            if ALERT_ACKNOWLEDGED_redraw_CAS == True:
                #### NOTE, don't re-sort, to keed mes order ac.CAS_Messages_Sort()
                self.UpDateTuples()
                self.redraw_CAS()
                self.si.UpdateScrollIndicator()

    #############################################################################
    def ScrollCAS(self, scroll_event = 0):
        # scroll_event mouse event from wheel
        gv.event_adder = 0
        # if scroll_event is positive, msg are scrolling DOWN
        if scroll_event > 0:
            gv.event_adder = -1
        elif scroll_event < 0:
            gv.event_adder = +1
        else:
            gv.event_adder = 0
        ###########################################################            
        ####### add to the total scrolled msg and check 
        ####### that can't scroll down from top
        self.scroll_up_down = self.scroll_up_down + gv.event_adder
        ###########################################################        
        if self.scroll_up_down  < 0:
            self.scroll_up_down = 0       
        if self.scroll_up_down  >= ac.mMsg_count.END_of_CAS_MSG  :  # just off the top of screen
            self.scroll_up_down =  ac.mMsg_count.END_of_CAS_MSG     # and no CAS is displayed, only EN
        
        # Get the number of red CAS in the active DB. if there are any red, there is no scrolling,
        # the CCue icon should not be show.  ALLOW_NEVER = 0;  ALLOW_WHEN_ACK = 1; ALLOW_ALL = 2       
        rtn_tuple = cc.Scrolling_with_RedCAS_Control(  self.scroll_up_down, 
                                                       ac.mMsg_count.AllCasTuple )       
        self.scroll_up_down  = rtn_tuple[0]
        gv.AllowScrolling    = rtn_tuple[1]
            
        #########################################################################################################
        temp = min( self.scroll_up_down + gv.possable_num_of_CASMsg, ac.mMsg_count.END_of_CAS_MSG )
        self.CAS_on_screen          = (self.scroll_up_down, temp)   
                     
        self.CAS_off_screen_high    = (0, self.CAS_on_screen[0] )  
        
        self.CAS_off_screen_low     = (self.CAS_on_screen[1] ,  ac.mMsg_count.END_of_CAS_MSG)    
        
        gv.num_in_screen_list       = self.CAS_on_screen[1] - self.CAS_on_screen[0]   

        self.UpDateTuples()
        self.redraw_CAS()
        self.ShowTuples()
        ##########################################################################
        
    def UpDateTuples(self):
        gv.HTuple = ac.mMsg_count.Count_active_CAS(self.CAS_off_screen_high[0],self.CAS_off_screen_high[1])
        gv.BTuple = ac.mMsg_count.Count_active_CAS(self.CAS_off_screen_low[0],self.CAS_off_screen_low[1])
        gv.STuple = ac.mMsg_count.Count_active_CAS(self.CAS_on_screen[0],self.CAS_on_screen[1])                      
    def redraw_CAS(self):
        self.si.UpdateScrollIndicator()       
        # ##################################################################### 
        # show the CAS messages on each canvas from top to bottom
        # cv.index is the particular canvas and location
        # i is the meaasge indes from the string list       
        self.cv_index = 0
        for i in range(self.CAS_on_screen[0], self.CAS_on_screen[1], 1):          
             
            gv.canvas_list[self.cv_index].ShowMessage(i)
            self.cv_index +=1
        # if at end of CAS Massage lest write the END message    
        if  self.cv_index < gv.possable_num_of_CASMsg :
            gv.canvas_list[  self.cv_index ].ENDMessage()
            self.cv_index +=1
        # clear and remaining canvas locations      
        while self.cv_index < gv.possable_num_of_CASMsg :
            gv.canvas_list[  self.cv_index ].ClearMessage()
            self.cv_index +=1  

        #######################################################################
        #Shows the number of messages off screen in the statusbay
    def ShowTuples(self):   
        tx0 = 'Above: Red({}, {}); Amber({}, {}); White({}, {})'.format(    gv.HTuple[e.WARNING_no],
                                                                            gv.HTuple[e.WARNING_yes],
                                                                            gv.HTuple[e.CAUTION_no],
                                                                            gv.HTuple[e.CAUTION_yes],
                                                                            gv.HTuple[e.ALERT_no],
                                                                            gv.HTuple[e.ALERT_yes]
                                                                            )

        tx1 = 'Below: Red({}, {}); Amber({}, {}); White({}, {})'.format(    gv.BTuple[e.WARNING_no],
                                                                            gv.BTuple[e.WARNING_yes],
                                                                            gv.BTuple[e.CAUTION_no],
                                                                            gv.BTuple[e.CAUTION_yes],
                                                                            gv.BTuple[e.ALERT_no],
                                                                            gv.BTuple[e.ALERT_yes]
                                                                            )
        tx2 = '--'
        if( gv.MessageController_1Sec_Loop_Timer_Running == True ) :
            tx2 = 'Running'
        else:
            tx2 = 'Stopped'
            
        self.StatusBar.configure(text = tx0+ ' ' + tx1 + '; ' + tx2)
        #######################################################################       

appWin = MainWindow(root)

################################################################################
######################    NOTIFICATION MESSAGE     #############################
class Notifications:
    def __init__(self):
        # four png files: 
        # 1. the active notification
        # 2. the acknowogared notification (cyan text on black ground with the stippling)
        # 3. the inactive nodifications, used then there are pending CAUTION or WARNING messages
        # 4. the thin stippled strip when the screen is full of un-acked WARNING and CAUTION
        self.stippleNoteL = ImageTk.PhotoImage(file = 'noteBarPoleL2_437x451.png')
        self.stippleNoteR = ImageTk.PhotoImage(file = 'noteBarPoleR2_437x451.png')
        self.wn = Canvas(    appWin.CASFrame, 
                        width  = gv.CAS_frame_rect[2], 
                        height = gv.CAS_frame_rect[3]/2, # the notification is 1/2 the CAS frame (5 CAS msg)
                        highlightthickness=0,
                        background = 'cyan')
        self.wn.create_image(0,0, image = self.stippleNoteL, anchor = 'nw')
        self.wn_y = gv.CAS_frame_rect[e.height]*2##/2
        self.Notification_zero = gv.CAS_frame_rect[e.height]
        self.wn.place(x=0, y=self.Notification_zero-3 )
        self.counter = 0

    def Animation(self): 
        Notification_Animation_Timer(True)  
        print('nt.Animation') 
        self.counter = self.counter +1
        print(self.counter)
        txt = '{}\t'.format(self.counter)
    #     The notification messags will anamate up from the bottom of the case window
    #     in steps, 3 to 4 for the height of the notification (1/2 seconds in transit). 
    #     The MAXIMU total will be 5, 
    #     or 1/2 the CAS window height. The clock rate is 8 hz
#        self.wn.configure( background = 'cyan' ) 
        self.wn.delete('all') 
        self.wn.create_image(0,0, image = self.stippleNoteL, anchor = 'nw')
        y_line_space = 20 
        self.wn.create_text(20,                             # x position of the msg text
                    6,                                      # y position of the msg text
                    fill   = 'black',                       # text color
                    text   = txt,    # text string
                    font   = gv.noti_font,                  # the font defined in gv and above if-else
                    anchor = 'nw'  )                        # anchor west LEFT justify
        self.wn.create_text(20,                             # x position of the msg text
                    6 + y_line_space,                       # y position of the msg text
                    fill   = 'black',                       # text color
                    text   = 'FMS1/2: NEW LINE ',           # text string
                    font   = gv.noti_font,                  # the font defined in gv and above if-else
                    anchor = 'nw'  )                        # anchor west LEFT justify
        delta = (self.Notification_zero * 0.8)/4                
        self.wn_y =  delta*self.counter       
        self.wn.place(x=0, y=self.wn_y)
        if self.counter > 4:
            Notification_Animation_Timer(False)  
######################
nt = Notifications() 
#########################################################################################
root.geometry( gv.root_geometry )
root.resizable(0,0)

#################################################
def OnMouseWheel(event):
    # print("Mousewheel event: ", event.delta)
    # draw_CAS(event.delta)
    appWin.ScrollCAS(event.delta)   
    return "break" 
def mouse_bn_callback(event):
    print("clicked at", event.x, event.y)
root.bind("<Button-1>", mouse_bn_callback)
root.bind("<Button-2>", mouse_bn_callback)
root.bind("<Button-3>", mouse_bn_callback)
root.bind("<MouseWheel>", OnMouseWheel)
###################################################
#### Blinking Line ##############################
# def f_loop():
#     if (loop.loop_counter % 2) == 0:
#         wn.create_image(0,0, image = stippleNoteL, anchor = 'nw')
#     else:
#         wn.create_image(0,0, image = stippleNoteR, anchor = 'nw')
# #################################################
### Below, final initilization and start-up
### Two times are created, the Message Controller 1 second
### loop is started and rus through the duration of the application.
### the 8 cps loop runs to animate the Notification messages.
# ##################################################################
Msg_Cont_loop = ltm.loop_Timer_Hz( hz = 1.0 , 
                                   hFunction_name = appWin.MessageController )

notification_loop = ft.InfiniteTimer( cycles_per_seconds = 12 , 
                                      target = nt.Animation )
####################################################################
def MessageController_1Sec_Loop_Timer( start = True ):
    global Msg_Cont_loop
    if start == True:
        gv.MessageController_1Sec_Loop_Timer_Running = Msg_Cont_loop.start()
    else: 
        gv.MessageController_1Sec_Loop_Timer_Running = Msg_Cont_loop.cancel()
    appWin.ScrollCAS(0)
    appWin.MessageController()
#####################################################
def Notification_Animation_Timer( start = True):
    global notification_loop
    ######  cycles_per_second = 8 
    if ( start == True and gv.Notification_Animation_Timer_Running == False):
        rtn = gv.Notification_Animation_Timer_Running = notification_loop.start()
    elif start == False: 
        rtn = gv.Notification_Animation_Timer_Running = notification_loop.cancel()      
    else:
        return  #print('Continuing with Notification_Animation_Timer running')    
##############################################
if False:
    # Timer off 
    # True or False in this if statement activates (or not) the start and loading
    
    # of the CAS messages.
    # 1. the Msg_Count_loop is a one second continous loop the calls the 
    #    appWin (main window) MessaheController to control process. 
    # 2. The notification loop is a 12 hz time only stated when moving notification messages.
    ##############################################
    #start message loop to update scroll messages 
    # and ack the whate alert CAS messages
    # Msg_Cont_loop = ltm.loop_Timer_Hz( 1.0 , appWin.MessageController )
    MessageController_1Sec_Loop_Timer(True) 
    ##############################################
    # notification_loop 
    nt.Animation()
    ############################################## 

# win1 = tl.TopLevelWindow(window_title = 'TopLevel Win1')

# win2 = tl.TopLevelWindow(window_title = 'TopLevel Win2') 

win1 = Scroll_Window(window_title = 'Data Entry', test = 101)
win2 = TIU_Window(window_title = ' TIU ')

appMenu = mwm.Main_Window_Menu(root, appWin, win1, win2) # self being the parent_window in the menu script

def For_Test():
    root.update_idletasks()
    
    
    
    
    

###############################################################################
def wm_delete_window_appWin(): # intercept the MainWindow "X" pressed message
    appWin.exit_application()  
# win1.wm_protocol(('WM_DELETE_WINDOW', wm_delete_window_Win1))
root.wm_protocol('WM_DELETE_WINDOW', wm_delete_window_appWin)
################################################################################




mainloop()