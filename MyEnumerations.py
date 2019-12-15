"""
from MyEnumerations import e
######
Use the above import line in files
to use the enum's listed herein
"""

class enummerations():
    def __init__(self):
        self.ptx    =   0
        self.pty    =   1
        self.width  =   2
        self.height =   3
        
        self.WARNING_no  = 0
        self.WARNING_yes = 1
        self.CAUTION_no  = 2
        self.CAUTION_yes = 3
        self.ALERT_no    = 4
        self.ALERT_yes   = 5
        self.NOTIFICATION_no  = 6
        self.NOTIFICATION_yes = 7
        self.END_of_CAS_MSG   = 8
        self.TOTAL_NO_MSG     = 9
        
        self.id_WARNING         =   12300
        self.id_CAUTION         =   12311
        self.id_NOTIFICATION    =   12322
        
        ####### ScrollIndicator Canvas ##################
        ## 5 is a bottom--> 0 is top canvas
        self.sAMBER_ABOVE    = 1        
        self.sWHITE_ABOVE    = 0
        self.sCURLY_CUE      = 2        
        self.sWHITE_BELOW    = 3        
        self.sAMBER_BELOW    = 4                
        self.sNOTIFICATION   = 5
#######################################    
e = enummerations()
    