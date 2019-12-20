from MyEnumerations import e
"""
This module is the center for external controll of various software functions. 
This a set of software switches with in the Notification code that change 
behaviors.
"""
class Configure_Control:
    def __init__(self):
    # enumerations for control
        self.ALLOW_NEVER = 0
        self.ALLOW_WHEN_ACK = 1
        self.ALLOW_ALL = 2
        self.m_scroll_up_down = 0
        self.m_Mode = 0
        ####
    def Set_Scroll_Mode(self, Mode = 0):
        self.m_Mode = Mode
            
    def Scrolling_with_RedCAS_Control( self, 
                                       m_scroll_up_down, 
                                       all_tuple        ):
        self.m_scroll_up_down = m_scroll_up_down
        self.m_AllowScrolling = False # this value will be passed back for the simular gv. value
        self.m_all_tuple = all_tuple # same as the ac nMsg_Cas_Tuple
        
        # The method controls scrolling with red CAS presend. 
        # There are three modes: with any red cas, or with just un-acknowlaged red CAS,
        # the third mode is allow scrolling regardless of the red cas.
        # The modes are controlled by a sofware switch Red_CAS_Control; the return values 
        # ALLOW_ALL, ALLOW_WHEN_ACK, ALLOW_NEVER
        if self.m_Mode == self.ALLOW_ALL:
            self.m_AllowScrolling = True
        ########         
        elif self.m_Mode == self.ALLOW_WHEN_ACK:
            if  self.m_all_tuple[e.WARNING_no]  > 0:           
                self.m_scroll_up_down = 0
                self.m_AllowScrolling = False        
            else:
                self.m_AllowScrolling = True 
        ########
        elif self.m_Mode == self.ALLOW_NEVER:          
            if ( self.m_all_tuple[e.WARNING_no] + self.m_all_tuple[e.WARNING_yes]) > 0:           
                self.m_scroll_up_down = 0
                self.m_AllowScrolling = False
            else:
                self.m_AllowScrolling = True    
        ######## 
        return ( self.m_scroll_up_down, self.m_AllowScrolling)
#########################################################################   
cc = Configure_Control()
#########################################################################
cc.Set_Scroll_Mode( cc.ALLOW_ALL )