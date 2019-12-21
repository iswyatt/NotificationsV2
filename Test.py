import InfiniteTimer as ft
import time

counter = 0

def tick():
    global counter
    print('entering tick function call')
    counter = counter + 1
    print(counter)
    if counter >=20:
        t.cancel() 
        counter = 0
        time.sleep(2.5)
        
    print(counter)   
    t.start()
  
    
# Example Usage
t = ft.InfiniteTimer(1, tick)
t.start()