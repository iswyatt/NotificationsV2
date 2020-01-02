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
        ###################################################
        ##### View Menu Items #############################
        self.view_menu = Menu( master = self.menubar, 
                               tearoff = 0)
        
        #################
        # View::win1 menu items
                
        self.win1.bv_window_status.set(True)
               
        self.view_menu.add_checkbutton( label = 'Show Top Level (1)',
                                        onvalue = True,
                                        offvalue = False,
                                        variable = self.win1.bv_window_status)
        ##################
        # View::win2 menu items        
        
        self.win2.bv_window_status.set(True)
        
               
        self.view_menu.add_checkbutton( label = 'Show Top Level (2)',
                                        onvalue = True,
                                        offvalue = False,
                                        variable = self.win2.bv_window_status)
        
        self.menubar.add_cascade( label = 'View', 
                                  menu  =  self.view_menu)        

       ################################################################
        ##### Quit menu  ###############################################
        
        self.quit_menu = Menu( master = self.menubar, 
                               tearoff = 0 )

        self.quit_menu.add_command( label = "Exit Application", 
                                    command = self.parent_window.exit_application )
        
        self.menubar.add_cascade( label = 'Quit', 
                                  menu  =  self.quit_menu)        
        
       ####################################################
 
        self.master.configure( menu = self.menubar) # add the actual menubar to the window
        # NOTE: the MainWindow is NOT derived from Tk and root is used to show the menu.
        ##################################################
        # bind to function
        self.menubar.bind("<<MenuSelect>>", self.update_view_checkbutton_checkmarks)
        """
        This menubar binding IS VERY IMPORTANT to update the view menu checkbutton (checks) 
        with the most current window status PRIOR to the View menu opening.
        """
        self.counter =0
        #################################################################################
        
    def update_view_checkbutton_checkmarks(self, *argv):
        #self.menu_print()
        ### win 1 checkbutton update        
        if self.win1.wm_state()=='normal':
            self.win1.bv_window_status.set(True)
        else:
            self.win1.bv_window_status.set(False)
        ### win 2 checkbutton update
        if self.win2.wm_state()=='normal':
            self.win2.bv_window_status.set(True)
        else:
            self.win2.bv_window_status.set(False)
        #self.menu_print()

    def menu_print(self, *argv):
        self.counter +=1
        print(f'{self.counter}__win1 status: {self.win1.bv_window_status.get()}')
        print(f'{self.counter}__win2 status: {self.win2.bv_window_status.get()}')