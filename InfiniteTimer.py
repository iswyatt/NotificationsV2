from threading import Timer
import time

counter = 0


class InfiniteTimer():
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, cycles_per_seconds, target):
        self._should_continue = False
        self.is_running = False
        if cycles_per_seconds <=0:
            cycles_per_seconds = 0.1
        self.seconds = 1/cycles_per_seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):

        if self._should_continue: # Code could have been running when cancel was called.
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()


    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
            counter = 0
            return True
        else:
            print("Timer already started or running, please wait if you're restarting.")
            

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")


# def tick():
#     global counter
#     print('entering tick function call')
#     counter = counter + 1
#     print(counter)
#     if counter >=20:
#         t.cancel() 
#         counter = 0
#         time.sleep(2.5)
        
#     print(counter)   
#     t.start()
  
    
# # Example Usage
# t = InfiniteTimer(1, tick)
# t.start()