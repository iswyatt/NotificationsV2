from threading import Timer, Thread, Event
from time import perf_counter_ns

############################################################
# USE THE CODE SAMPLE BELOW TO USE THE LOOP TIMER FUNCTION.
# SETUP THE TIMER INTERVAL IN hZ, AND BUILD THE CALLBACK FUNCTION
###########################################################
# from loop_Timer_Module import loop_Timer_Hz
# def timer_function():
#     print("from top")
# cycles_per_second = 1.0
# t = loop_Timer_Hz( cycles_per_second, timer_function)
# t.start()
##########################################################

class loop_Timer_Hz:
    def __init__(self, hz, hFunction_name):     
        self.t= 1.0/float(hz)
        self.hFunction = hFunction_name
        self.loop_counter = 0
        self.loop_timer_is_running = False        
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        # this function is repeatedly called from the callback function 
        self.loop_counter = self.loop_counter + 1       
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        if( self.loop_timer_is_running == False ) :
            self.loop_timer_is_running = True
            self.thread.start()
        return self.loop_timer_is_running

    def cancel(self):
        self.thread.cancel()
        self.loop_timer_is_running = False
        return self.loop_timer_is_running        
        
    ######################

###############################################################################
# start = 0
# end = 0
# sum = 0.0
# counter = 0
# if __name__ == "__main__":
#     def timer_function():
#         global end
#         global start
#         global sum
#         global counter
#         end = perf_counter_ns()
#         time = end - start
#         sum = sum+time
#         counter = counter +1
#         rtn= (sum/counter)/1000000000
#         print('ipsem lorem = ' + str(time/1000000000) + ' adv: ' + str(rtn) )
#         start = perf_counter_ns()

#     cycles_per_second = .3333
#     t = loop_Timer_Hz( cycles_per_second, timer_function)
#     t.start()
# ############################################################################