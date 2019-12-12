
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
##############################################
root = Tk()
##############################################

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
        ##################################################################################
        ########### screen Tuples filled in the scroll method ##########################
        self.HTuple = (0,0,0,0,0,0,0,0)     #tuple # off screen high CAS count
        self.STuple = (0,0,0,0,0,0,0,0)     #tuple # on screen CAS count
        self.BTuple = (0,0,0,0,0,0,0,0)     #tuple # off screen below CAS count
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
        ########### set up the fonts and the locations on the canvas ####################
        self.cas_font         = font.Font(family = 'ClearviewADA', size = 20, weight = 'normal')
        self.noti_font        = font.Font(family = 'ClearviewADA', size = 18, weight = 'normal',
                                           slant = 'italic')
        self.but_font         = font.Font(family = 'ClearviewADA', size = 13, weight = 'bold'  )
        self.frame_label_font = font.Font(family = 'ClearviewADA', size = 11, weight = 'bold') 
        self.sym_font         = font.Font(family = 'ClearviewADA', size = 16, weight = 'normal')   
        # self.sym_font         = font.Font(family = 'Symbol', size = 16, weight = 'normal')        
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
def MasterButtonCallback(bt_id, status):
    if status == True:
        ac.Ackknowlege_CAS(bt_id)
    appWin.ScrollCAS(0)
    appWin.MessageController()
         
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
        #self.Icallback = Icallback       
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
        print('Class Method callback from:: id={} status={}'.format( self.id, self.active_status ))
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
        a = 16 # length of arrow lines
        b = math.sqrt(0.75)*a
        delx = 24
        dely = 2
        self.up_arrow   = (0+delx, b+dely,    a+delx, b+dely,        (a/2)+delx, 0+dely)
        self.down_arrow = (0+delx, 0+dely,    (a/2)+delx, b+dely,    (a)+delx, 0+dely)

               
    def Update(self, color = ('yellow', 'black'), sIndication = '   ', draw = ''):  
        # "draw = " pass additional information: draw up or dow arrow, notification graphic etc.
     
        if draw == 'down' :
            self.sv.configure( background = 'black' ) 
            self.sv.delete('all') 
            self.up_triangle = self.sv.create_polygon(  self.down_arrow, outline = color[0], fill = color[1] )
        
            
            self.the_text = str(9).zfill(2)
            
                                                        
            # self.sv.move(self.up_triangle, 1, 2)  
            self.sv.create_text(
                0,                      # x position of the msg text
                -2,                     # y position of the msg text
                fill   = 'yellow',      # text color
                text   = self.the_text,   # text string
                font   = gv.sym_font,   # the font defined in gv and above if-else
                anchor = 'nw'  )        # anchor west LEFT justify  
            
            
                  
        elif sIndication == 'CCue':
            # if it is the curlley-cue place place the image into the Canvas
            #####################
            self.CCueImage = Image.open('CCue_20x20.png')
            # Put the image into a canvas compatible class, and stick in an
            # arbitrary variable to the garbage collector doesn't destroy it
            self.sv.image = ImageTk.PhotoImage( self.CCueImage )
            # Add the image to the canvas, and set the anchor to the top left / north west corner
            self.sv.create_image(8, 0, image=self.sv.image, anchor='nw')
            #####################
        else:
            self.sv.configure( background = color[0] ) 
            self.sv.delete('all')       
            self.sv.create_text(
                4,                      # x position of the msg text
                -3,                     # y position of the msg text
                fill   = color[1],      # text color
                text   = sIndication,   # text string
                font   = gv.sym_font,   # the font defined in gv and above if-else
                anchor = 'nw'  )        # anchor west LEFT justify   
############################################################################
############################################################################            
class ScrollIndicator():
    def __init__(self, contex):
        self.m_contex = contex 
        pad = 10
        m_NoOfCanvas=   6        
        m_Added_height_for_notifications = 25
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
                i_rect = (  0, 
                            i_offset,
                            self.m_Scroll_Canvas_size[0],
                            self.m_Scroll_Canvas_size[1] + m_Added_height_for_notifications )  
            ############
            self.Scroll_cv_list.append( ScrollCanvas(   self.m_Scroll_frame, i_rect  )  ) 
    #######################################################################################
    #######################################################################################
    def UpdateScrollIndicator(self): 
        sColor =  ('black', 'black')   # ( bachground, text color )   
        # up \u00AD or \u0044, dn \u00AF or \u00D1 
        self.Scroll_cv_list[e.sCURLY_CUE].Update( color = ('cyan', 'cyan'), 
                                                        sIndication = 'CCue')
        ################          
        num_of_msg = gv.HTuple[e.ALERT_no] + gv.HTuple[e.ALERT_yes]
        if  num_of_msg > 0:         
            self.Scroll_cv_list[e.sWHITE_ABOVE].Update( color = ('black', 'white'), 
                                                        sIndication = '\u0044 {}'.format( num_of_msg ))
        else:
            self.Scroll_cv_list[e.sWHITE_ABOVE].Update( color = ('black', 'black'), 
                                                        sIndication = '   '      )            
        ################   
        num_of_msg = gv.HTuple[e.CAUTION_no] + gv.HTuple[e.CAUTION_yes]
        if  num_of_msg > 0:         
            if  gv.HTuple[e.CAUTION_no] > 0:
                sColor = ('yellow', 'black')            
            else:
                sColor = ('black', 'yellow')                                              
            self.Scroll_cv_list[e.sAMBER_ABOVE].Update( color = sColor, 
                                                        sIndication = '\u0044 {}'.format( num_of_msg ))            
        else:
            self.Scroll_cv_list[e.sAMBER_ABOVE].Update( color = ('black', 'black'), 
                                                        sIndication = '   '      )                 
        ################
        ################          
        num_of_msg = gv.BTuple[e.ALERT_no] + gv.BTuple[e.ALERT_yes]
        if  num_of_msg > 0:         
            self.Scroll_cv_list[e.sWHITE_BELOW].Update( color = ('black', 'white'), 
                                                        sIndication = '\u00D1 {}'.format( num_of_msg ))
        else:
            self.Scroll_cv_list[e.sWHITE_BELOW].Update( color = ('black', 'black'), 
                                                        sIndication = '   '      )            
        ################   
        num_of_msg = gv.BTuple[e.CAUTION_no] + gv.BTuple[e.CAUTION_yes]
        if  num_of_msg > 0:         
            if  gv.BTuple[e.CAUTION_no] > 0:
                sColor = ('yellow', 'black')            
            else:
                sColor = ('black', 'yellow')                                              
            self.Scroll_cv_list[e.sAMBER_BELOW].Update( color = sColor, 
                                                        sIndication = '\u00D1 {}'.format( num_of_msg ))            
        else:
            self.Scroll_cv_list[e.sAMBER_BELOW].Update( color = ('black', 'black'), 
                                                        sIndication = '   '      )  

        ################
        # Notification Flag
        # total number of Notification messages
        num_of_msg = abs( gv.BTuple[e.TOTAL_NO_MSG] - gv.BTuple[e.END_of_CAS_MSG] )
        if num_of_msg > 0:
            sColor = ( 'cyan', 'black')
        else:
            sColor = ('black', 'black')   
        self.Scroll_cv_list[e.sNOTIFICATION].Update( color = sColor, 
                                            sIndication = ' {}\n{} '.format( num_of_msg, 123 ), draw = 'down')   
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
        self.si = ScrollIndicator( self.ImageFrame )
        self.ArrowLabel = Label(root)
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
    
    # # script function excuted only once to create the CAS messages canvases
    # ### use the gv parameters to create the individual canvases for the CAS messages
    # def CreateScrollCanvas(self):
    #     return
    #     # create the canvases if first time through
    #     for i in range(int(gv.Num_of_Scroll_canvas)):
    #         sv_offset = i * gv.Scroll_frame_rect[3] # the y distance down from the scroll top point
    #         # set the individual x, y points for the scroll sv in the dictionary, 
    #         # key the position in the scroll frame
    #         gv.Scroll_canvas_pt_dict = { i: (gv.Scroll_canvas_rect[0], 
    #                                          gv.Scroll_canvas_rect[1] + sv_offset )
    #                                     }
    #         # the canvas_list (array of CASMessage class) create each canvas
    #         gv.Scroll_canvas_list.append( ScrollCanvas( self.Scroll_frame, 
    #                                                     gv.Scroll_canvas_pt_dict[i] ) )
    #         # indicate the canvases are now created
    ################################################################################    
    
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
        rtn = ac.mMsg_count.Count_active_CAS()
        status = BooleanVar
        if rtn[e.WARNING_no] > 0:
            status = True
        else:
            status = False
            # activate the WARNING master switch
        self.WARNING_bn_status = self.WARNING_bn.SetStatusActive(status)
               
        if rtn[e.CAUTION_no] > 0:
            status = True
        else:
            status = False
            # activate the CAUTION master switch
        self.CAUTION_bn_status = self.CAUTION_bn.SetStatusActive(status)
    #############################################################################
    def ScrollCAS(self, scroll_event = 0):
        # scroll_event mouse event from wheel
        # top_displayed_msg = 0
        # bot_displayed_msg = 0       
        event_adder = 0
        # if scroll_event is positive, msg are scrolling DOWN
        if scroll_event > 0:
            event_adder = -1
        elif scroll_event < 0:
            event_adder = +1
        else:
            event_adder = 0
        #########################################            
        ####### add to the total scrolled msg and check 
        ####### that can't scroll down from top
        self.scroll_up_down = self.scroll_up_down + event_adder
        if self.scroll_up_down < 0:
            self.scroll_up_down = 0       
        if self.scroll_up_down >= ac.mMsg_count.END_of_CAS_MSG  :  # just off the top of screen
            self.scroll_up_down =  ac.mMsg_count.END_of_CAS_MSG    # and no CAS is displayed, only END
        #########################################################################################################
        temp = min( self.scroll_up_down + gv.possable_num_of_CASMsg, ac.mMsg_count.END_of_CAS_MSG )
        self.CAS_on_screen          = (self.scroll_up_down, temp)   
                     
        self.CAS_off_screen_high    = (0, self.CAS_on_screen[0] ) #- 1   )
        
        self.CAS_off_screen_low     = (self.CAS_on_screen[1] + 1,  ac.mMsg_count.END_of_CAS_MSG)    
               
        gv.num_in_screen_list       = self.CAS_on_screen[1] - self.CAS_on_screen[0]   

        gv.HTuple = ac.mMsg_count.Count_active_CAS(self.CAS_off_screen_high[0],self.CAS_off_screen_high[1])
        gv.BTuple = ac.mMsg_count.Count_active_CAS(self.CAS_off_screen_low[0],self.CAS_off_screen_low[1])
        gv.STuple = ac.mMsg_count.Count_active_CAS(self.CAS_on_screen[0],self.CAS_on_screen[1])
       
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
        StatusBar.configure(text = tx0+ '  ' + tx1 )
        
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
        # self.MessageController()               
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
                        background = 'blue')
        self.wn.create_image(0,0, image = self.stippleNoteL, anchor = 'nw')
        self.wn_y = gv.CAS_frame_rect[e.height]/2
        self.wn.place(x=0, y=self.wn_y)
        self.Anamation()

    def Anamation(self):   
    #     The notification messags will anamate up from the bottom of the case window
    #     in steps, 3 to 4 for the height of the notification (1/2 seconds in transit). The MAXIMU total will be 5, 
    #     or 1/2 the CAS window height. The clock rate is 8 hz
        yspace = 20
        self.wn.create_text(20,                         # x position of the msg text
                    6,                      # y position of the msg text
                    fill   = 'black',                      # text color
                    text   = 'FMS1/2: TEST 1234567890 ',  # text string
                    font   = gv.noti_font,               # the font defined in gv and above if-else
                    anchor = 'nw'  )                  # anchor west LEFT justify
        self.wn.create_text(20,                         # x position of the msg text
                    6+yspace,                      # y position of the msg text
                    fill   = 'black',                      # text color
                    text   = 'FMS1/2: NEW LINE ',  # text string
                    font   = gv.noti_font,               # the font defined in gv and above if-else
                    anchor = 'nw'  )                  # anchor west LEFT justify        
                   
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
# #################################################

loopp =0
bottom = gv.CAS_frame_rect[e.height]
ht =bottom*0.2 -1
steps = 3
del_ht = ht/steps
st_counter = 0
delta = 1
wn_y = bottom-ht-1
adder = 0
def f_loop():
    # stepper = 1 #gv.CAS_frame_rect[3]/6
    global wn_y
    global st_counter
    global delta
    global adder 
    if ( st_counter == 0 ):
        adder = del_ht
        time.sleep(2)
        delta = 1
    if ( st_counter == steps  ):
        delta = -1
        time.sleep(2)
        adder = -del_ht
    wn_y = wn_y + adder
    st_counter = st_counter + delta
    print('Delta:={}'.format(delta))
    print('adder:= {}'.format(adder))
    print(st_counter)
    print('wn_y:= {}'.format(wn_y))
    print('steps:={}'.format(steps))
    nt.wn.place(x=0, y=wn_y)
    #  #################################################
    # global loopp
    # loopp = loopp + 1
    # floopp = 'time:={:.1f} seconds '.format(loopp/4)
    # StatusBar.configure(text = floopp)
# #################################################
cycles_per_second = 8
loop = ltm.loop_Timer_Hz( cycles_per_second, f_loop)
# loop.start()
f_loop()
# #################################################

StatusBar = Label(root, 
                text= '', 
                bd=1, 
                anchor=W, 
                height = -gv.statusbar_height,
                bg = 'gray')
StatusBar.pack(side=BOTTOM, fill=X)
#################################################
# si = ScrollIndicator( appWin.ImageFrame )
# si.UpdateScrollIndicator()
appWin.ScrollCAS(0)
appWin.MessageController()
mainloop()