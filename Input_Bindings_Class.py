import tkinter as tk
# from tkinter import ttk
# from tkinter.ttk import *
import random
from PIL import Image, ImageTk
import os 
os.system('cls')


# root = tk.Tk()
# root.title('Bind Application Demo')
# root.iconbitmap('python.ico')
# root.geometry('800x600+200+200')
# root.configure(bg = 'slate gray')
class Bindings:
    def __init__(self, context):
    
        def print_event_1(event):
            position = f'<Button-1>\t\t(x = {event.x}, y = {event.y}: Screen ({event.x_root}, {event.y_root})'
            print(position)
            
        def print_event_1_2(event):
            position = f'<Button-2>\t\t(x = {event.x}, y = {event.y}: Screen ({event.x_root}, {event.y_root})'
            print(position)
            
        def print_event_1_3(event):
            position = f'<Button-3>\t\t(x = {event.x}, y = {event.y}: Screen ({event.x_root}, {event.y_root})'
            print(position)

        def print_event_2(event):
            position = f'<Double-Button-1>\t(x = {event.x}, y = {event.y})'
            print(position)
            
        def print_event_3(event):
            position = f'<ButtonRelease-1>\t(x = {event.x}, y = {event.y})'
            print(position) 
                
        def print_event_4(event):
            position = f'<B1-Motion> (i.e. drag)\t(x = {event.x}, y = {event.y})'
            print(position)     
            
        def print_event_5(event):
            position = f'<Enter> (frame)\t(x = {event.x}, y = {event.y})'       
            print(position)  
            
        def print_event_6(event):
            position = f'<Leave> (frame)\t(x = {event.x}, y = {event.y})'       
            print(position)      

        def print_event_mouse(event):
            print("Mousewheel event: ", event.delta)


            
        context.bind('<Button-1>',  lambda e: print_event_1(event = e)  )
        context.bind('<Button-2>',  lambda e: print_event_1_2(event = e)  ) 
        context.bind('<Button-3>',  lambda e: print_event_1_3(event = e)  )               
        context.bind('<Double-Button-1>',  lambda e: print_event_2(event = e)  )
        context.bind('<ButtonRelease-1>',  lambda e: print_event_3(event = e)  )
        context.bind('<B1-Motion>', lambda e: print_event_4(event = e)  )
        context.bind('<Enter>', lambda e: print_event_5(event = e)  )
        context.bind('<Leave>', lambda e: print_event_6(event = e)  )
        context.bind('<MouseWheel>', lambda e: print_event_mouse(event = e)  )
        
# b = Bindings(root)

# root.mainloop()