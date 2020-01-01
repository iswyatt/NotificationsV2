from tkinter import *
from tkinter import ttk
import tkinter.font as font
from MyEnumerations import e
import os 
os.system('cls')

class Main_Window_Menu:
    def __init__(self, master, parent_window, tl1, tl2):
        self.master = master 
        self.parent_window = parent_window # the appWin main window 
        self.win1 = tl1 # the win1 window
        self.win2 = tl2 # win2 window  


  #################################################################################
        # adding application menu
        self.menubar = Menu(   master = self.master )
        ##### File menu items ##############################
        self.file_menu = Menu( master = self.menubar, 
                               tearoff = 0)
        self.file_menu.add_command( label = "Exit Application", 
                                    command = self.parent_window.exit_application )
        self.menubar.add_cascade( label = 'File', 
                                  menu  =  self.file_menu)
        ##### View Menu Items #############################
        self.view_menu = Menu( master = self.menubar, 
                               tearoff = 0)
        
        ##############################################################
        # win1 menu items
        print(f'win1 status - 0 -: {self.win1.bv_window_status.get()}')
                
        self.win1.bv_window_status.set(True)
               
        self.view_menu.add_checkbutton( label = 'Show Top Level (1)',
                                        onvalue = True,
                                        offvalue = False,
                                        variable = self.win1.bv_window_status)
        ##############################################################
        # win2 menu items        
        # self.toplevel_2_displayed = BooleanVar()  
        # self.toplevel_2_displayed.set(True)
        
        self.win2.bv_window_status.set(True)
        
        # self.toplevel_2_displayed.trace( mode = 'w', 
        #                                  callback = self.parent_window.show_toplevel_2 ) 
               
        self.view_menu.add_checkbutton( label = 'Show Top Level (2)',
                                        onvalue = True,
                                        offvalue = False,
                                        variable = self.win2.bv_window_status)
     
        # self.view_menu.add_command( label = "Show Toplevel 1", 
        #                             command = self.show_toplevel_1 )
        # self.view_menu.add_command( label = "Show Toplevel 2", 
        #                             command = self.show_toplevel_2 )
        
        ####################################################
        self.menubar.add_cascade( label = 'View', 
                                  menu  =  self.view_menu)
        
        
        
        
        self.master.configure( menu = self.menubar) # add the actual menubar to the window
        # NOTE: this MainWindow is NOT derived fro Tk and root is used to show the menu.
        # bind to function
        self.menubar.bind("<<MenuSelect>>", self.Menu_print)
        self.counter =0
        #################################################################################
        
    def show_toplevel_1(self, *argv):
        window_state = self.win1.bv_window_status.get()
        print(f'{self.counter}..win1 status - 1 -: {window_state}')
        
        if self.win1.wm_state()=='normal':
            window_state = True
        else:
            window_state = False
        self.win1.bv_window_status.set(window_state)
        print(f'{self.counter}__win1 status - 2 -: {self.win1.bv_window_status.get()}')
         
    def Menu_print(self, *argv):
        self.counter +=1
        print(f'{self.counter}==from menu')
        self.show_toplevel_1()