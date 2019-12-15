from MyEnumerations import e
import datetime
current_time  = datetime.datetime.now().strftime('%H%M%S')
######################################################################################################
USE_CASE = 3
if USE_CASE == 0:
    UC_active_CAS = [  
                    ['11: UN-ACKNOWLEDGED RED CAS', 'WARNING',  'no_ACKNOWLEDGED',  current_time],
                    ['00: UN-ACKNOWLEDGED AMB CAS', 'CAUTION',  'no_ACKNOWLEDGED', current_time],
                    ['01: ---ACKNOWLEDGED RED CAS', 'WARNING',  'yes_ACKNOWLEDGED',  current_time],
                    ['02: ---ACKNOWLEDGED AMB CAS', 'CAUTION',  'yes_ACKNOWLEDGED',  current_time],
                    ['03: ---ACKNOWLEDGED AMB CAS', 'CAUTION',  'yes_ACKNOWLEDGED', current_time],
                    ['04: ---ACKNOWLEDGED RED CAS', 'WARNING',  'yes_ACKNOWLEDGED', current_time],
                    ['05: UN-ACKNOWLEDGED RED CAS', 'WARNING',  'no_ACKNOWLEDGED',  current_time],
                    ['06: ---ACKNOWLEDGED WHI CAS', 'ALERT',    'yes_ACKNOWLEDGED', current_time],
                    ['07: UN-ACKNOWLEDGED RED CAS', 'WARNING',  'no_ACKNOWLEDGED',  current_time],
                    ['08: UN-ACKNOWLEDGED AMB CAS', 'CAUTION',  'no_ACKNOWLEDGED',  current_time],
                    ['09: ---ACKNOWLEDGED AMB CAS', 'CAUTION',  'yes_ACKNOWLEDGED', current_time],
                    ['10: UN-ACKNOWLEDGED WHI CAS', 'ALERT',    'no_ACKNOWLEDGED',  current_time],
                    ['11: ---ACKNOWLEDGED WHI CAS', 'ALERT',    'yes_ACKNOWLEDGED', current_time],
                    ['12: UN-ACKNOWLEDGED RED CAS', 'WARNING',  'no_ACKNOWLEDGED',  current_time],
                    ['13: UN-ACKNOWLEDGED AMB CAS', 'CAUTION',  'no_ACKNOWLEDGED',  current_time],
                    ['14: ---ACKNOWLEDGED AMB CAS', 'CAUTION',  'yes_ACKNOWLEDGED', current_time],
                    ['15: ---ACKNOWLEDGED RED CAS', 'WARNING',  'yes_ACKNOWLEDGED', current_time],              
                    ['16: ---ACKNOWLEDGED RED CAS', 'WARNING',  'yes_ACKNOWLEDGED', current_time],
                    ['17: UN-ACKNOWLEDGED WHI CAS', 'ALERT',    'no_ACKNOWLEDGED',  current_time],
                    ['18: ---ACKNOWLEDGED WHI CAS', 'ALERT',    'yes_ACKNOWLEDGED', current_time],
                    ['19: UN-ACKNOWLEDGED RED CAS', 'WARNING',  'no_ACKNOWLEDGED',  current_time],
                    ['20: UN-ACKNOWLEDGED AMB CAS', 'CAUTION',  'no_ACKNOWLEDGED',  current_time],
                    ['21: ---ACKNOWLEDGED AMB CAS', 'CAUTION',  'yes_ACKNOWLEDGED', current_time],
                    ['22: ---ACKNOWLEDGED RED CAS', 'WARNING',  'yes_ACKNOWLEDGED', current_time],                
                    ['23: UN-ACKNOWLEDGED RED CAS', 'WARNING',  'no_ACKNOWLEDGED',  current_time],
                    ['24: ---ACKNOWLEDGED WHI CAS', 'ALERT',    'yes_ACKNOWLEDGED',  current_time],
                    ['25: NOTIFICATION    WHI CAS', 'AA_NOTI',  'yes_ACKNOWLEDGED', current_time],                
                    ['26: NOTIFICATION    WHI CAS', 'AA_NOTI',  'no_ACKNOWLEDGED',  current_time]  
                    ]
if USE_CASE == 1:
    UC_active_CAS = [  ('80 FIRE: LH+RH WHEEL OVHT', 'WARNING',    'yes_ACKNOWLEDGED',  'post_time'),
                    ('90 PRESS: CABIN ALT TOO HI',   'CAUTION',    'no_ACKNOWLEDGED',   'post_time'), 
                    ('08 BLEED: 1 OVHT',             'WARNING',    'no_ACKNOWLEDGED',   'post_time'), 
                    ('15 COND: AFT FCS BOX OVHT',    'CAUTION',    'yes_ACKNOWLEDGED',  'post_time'), 
                    ('0 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',   'post_time'), 
                    ('1 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',   'post_time'), 
                    ('2 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',  'post_time'), 
                    ('3 NOTIFICATION',              'AA_NOTI',    'no_ACKNOWLEDGED',   'post_time'), 
                    ('4 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',   'post_time'), 
                    ('5 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',  'post_time'), 
                    ('6 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',   'post_time'), 
                    ('7 NOTIFICATION',              'AA_NOTI',    'no_ACKNOWLEDGED',   'post_time'), 
                    ('8 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',  'post_time'), 
                    ('26 ELEC: AFT DIST BOX OVHT','WARNING',    'yes_ACKNOWLEDGED',  'post_time'),  
                    ('15 COND: AFT FCS BOX OVHT', 'ALERT',      'yes_ACKNOWLEDGED',  'post_time'),  
                    ('26 ELEC: AFT DIST BOX OVHT','ALERT',      'no_ACKNOWLEDGED',   'post_time')      ]

if USE_CASE == 2:
    UC_active_CAS = [  ('80 FIRE: LH+RH WHEEL OVHT', 'WARNING',    'no_ACKNOWLEDGED',  'post_time'),
                    ('801 FIRE: LH+RH WHEEL OVHT', 'WARNING',    'no_ACKNOWLEDGED',  'post_time'),
                    ( 'END', 'AA last in sort', 'ZZ to be last in sort', 'na')]
               
if USE_CASE == 3:
    UC_active_CAS = [  
                    ['80 FIRE: LH+RH WHEEL OVHT', 'WARNING',    'yes_ACKNOWLEDGED',  'post_time'],
                    ['90 PRESS: CABIN ALT TOO HI','CAUTION',    'no_ACKNOWLEDGED',   'post_time'], 
                    ['08 BLEED: 1 OVHT',          'WARNING',    'no_ACKNOWLEDGED',   'post_time'], 
                    ['15 COND: AFT FCS BOX OVHT', 'CAUTION',    'yes_ACKNOWLEDGED',  'post_time'], 
                    ['0 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',   'post_time'], 
                    ['1 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',   'post_time'], 
                    ['2 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',  'post_time'], 
                    ['3 NOTIFICATION',              'AA_NOTI',    'no_ACKNOWLEDGED',   'post_time'], 
                    ['4 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',   'post_time'], 
                    ['5 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',  'post_time'], 
                    ['6 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',   'post_time'], 
                    ['7 NOTIFICATION',              'AA_NOTI',    'no_ACKNOWLEDGED',   'post_time'], 
                    ['8 NOTIFICATION',              'AA_NOTI',    'yes_ACKNOWLEDGED',  'post_time'], 
                    ['26 ELEC: AFT DIST BOX OVHT','WARNING',    'yes_ACKNOWLEDGED',  'post_time'],  
                    ['15 COND: AFT FCS BOX OVHT', 'ALERT',      'yes_ACKNOWLEDGED',  'post_time'],  
                    ['26 ELEC: AFT DIST BOX OVHT','ALERT',      'no_ACKNOWLEDGED',   'post_time']      
                    ]
################################################################################################

# copy the orginal active CAS list and use the copy.
active_CAS = UC_active_CAS.copy()

def CAS_Messages_Sort():
    # sort the actave CAS messages by their color and the if they are ack or not....
    active_CAS.sort(reverse=False, key=lambda element: element[2])
    active_CAS.sort(reverse=True,  key=lambda element: element[1])
    for ele1,ele2,ele3,ele4 in active_CAS:
        print( "{:<34}{:<34}{:<34}{:<12}" .format(ele1,ele2,ele3,ele4))
    print('active_CAS[0][0]: {}'.format(active_CAS[0][0]))    
    print('Length or active_CAS: {}'.format(len(active_CAS)))

def print_CAS_enumerations(rtn):
    print(rtn)
    print('WARNING_no: {}'.format(     rtn[e.WARNING_no])      )
    print('WARNING_yes: {}'.format(    rtn[e.WARNING_yes])     )
    print('CAUTION_no: {}'.format(     rtn[e.CAUTION_no])      )
    print('CAUTION_yes: {}'.format(    rtn[e.CAUTION_yes])     )
    print('ALERT_no: {}'.format(       rtn[e.ALERT_no])        )
    print('ALERT_yes: {}'.format(      rtn[e.ALERT_yes])       )       
    print('NOTIFICATION_no: {}'.format(    rtn[e.NOTIFICATION_no]) )
    print('NOTIFICATION_yes: {}'.format(   rtn[e.NOTIFICATION_yes]))
    print('self.END_of_CAS_MSG: {}'.format(     rtn[e.END_of_CAS_MSG])  ) 
    print('self.TOTAL_NO_MSG: {}'.format(       rtn[e.TOTAL_NO_MSG])    )

class CASCount():
    def __init__(self):
        self.WARNING_no  = 0
        self.WARNING_yes = 0
        self.CAUTION_no  = 0
        self.CAUTION_yes = 0
        self.ALERT_no    = 0
        self.ALERT_yes   = 0
        self.NOTIFICATION_no  = 0
        self.NOTIFICATION_yes = 0
        self.END_of_CAS_MSG = 0        
        self.TOTAL_NO_MSG     = 0
        
    def Count_active_CAS(self, top = 0, bottom = 100):       
        WARNING_no = 0
        WARNING_yes = 0
        CAUTION_no = 0
        CAUTION_yes = 0
        ALERT_no = 0
        ALERT_yes = 0
        NOTIFICATION_no = 0
        NOTIFICATION_yes = 0
        
        for row in active_CAS[ top: bottom      ]: 
            if (row[1]=='WARNING')      and (row[2]=='no_ACKNOWLEDGED'):
                WARNING_no           =  WARNING_no +1 
                       
            if (row[1]=='WARNING')      and (row[2]=='yes_ACKNOWLEDGED'):
                WARNING_yes          =  WARNING_yes +1 
                       
            if (row[1]=='CAUTION')      and (row[2]=='no_ACKNOWLEDGED'):
                CAUTION_no           =  CAUTION_no +1 
                       
            if (row[1]=='CAUTION')      and (row[2]=='yes_ACKNOWLEDGED'):
                CAUTION_yes          =  CAUTION_yes +1 
                  
            if (row[1]=='ALERT')        and (row[2]=='no_ACKNOWLEDGED'):
                ALERT_no             =  ALERT_no +1 
                       
            if (row[1]=='ALERT')        and (row[2]=='yes_ACKNOWLEDGED'):
                ALERT_yes            =  ALERT_yes +1 
                 
            if (row[1]=='AA_NOTI')      and (row[2]=='no_ACKNOWLEDGED'):
                NOTIFICATION_no      =  NOTIFICATION_no +1 
                       
            if (row[1]=='AA_NOTI')      and (row[2]=='yes_ACKNOWLEDGED'):
                NOTIFICATION_yes     =  NOTIFICATION_yes +1  
            
        if bottom >=100: ## 100 is the default value; the entire string list is couted
                         ## the counted values are places into the class variables
            self.TOTAL_NO_MSG = len(active_CAS)               
            self.END_of_CAS_MSG =  WARNING_no + WARNING_yes + CAUTION_no
            self.END_of_CAS_MSG =  self.END_of_CAS_MSG + CAUTION_yes + ALERT_no + ALERT_yes
            self.WARNING_no  = WARNING_no
            self.WARNING_yes = WARNING_yes
            self.CAUTION_no  = CAUTION_no
            self.CAUTION_yes = CAUTION_yes
            self.ALERT_no    = ALERT_no
            self.ALERT_yes   = ALERT_yes
            self.NOTIFICATION_no  = NOTIFICATION_no
            self.NOTIFICATION_yes = NOTIFICATION_yes                 
            # The return value is a Tuple with the number of CAS messages
            # in various catagories. The numbers are filutered by the Range [top:bottom] perameter
            # The default argument will complie data for the entire list database
            # The print_CAS_enumerations(rtn): above will print the tuple values with labels.                
        rtn =  (WARNING_no, WARNING_yes, 
                CAUTION_no, CAUTION_yes, 
                ALERT_no, ALERT_yes,
                NOTIFICATION_no, NOTIFICATION_yes,
                self.END_of_CAS_MSG,  self.TOTAL_NO_MSG )        
        # print_CAS_enumerations(rtn)
        return(rtn)

        ##################################################################
        
mMsg_count = CASCount()

CAS_Messages_Sort()

rtn = mMsg_count.Count_active_CAS()
print(rtn)   
print_CAS_enumerations(rtn)

def Ackknowlege_CAS(bt_id):
    # temp_remove = []
    # temp_append = []
    
    if bt_id == e.id_WARNING:

        for msg in active_CAS:
 
            if (msg[1] == 'WARNING') and (msg[2] == 'no_ACKNOWLEDGED'):
                msg[2] = 'yes_ACKNOWLEDGED'
                          
    elif bt_id == e.id_CAUTION:
        
        for msg in active_CAS:
            
            if (msg[1] == 'CAUTION') and (msg[2] == 'no_ACKNOWLEDGED'):
                msg[2] = 'yes_ACKNOWLEDGED'
                                                   
    CAS_Messages_Sort()
    rtn = mMsg_count.Count_active_CAS()
    print_CAS_enumerations(rtn)

    

