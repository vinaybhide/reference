from tkinter import * 
from tkinter.ttk import *
  
# creates tkinter window or root window 
root = Tk() 
root.geometry('200x100') 
  
# function to be called when button-2 of mouse is pressed 
def pressed2(event): 
    print('Button-2 pressed at x = % d, y = % d'%(event.x, event.y)) 
  
# function to be called when button-3 of mouse is pressed 
def pressed3(event): 
    print('Button-3 pressed at x = % d, y = % d'%(event.x, event.y)) 
  
# use following logic if you want to handle both single & double clicks
# function to be called when button-1 is double clicked 
def double_click(event): 
    global btn_double_clicked

    btn_double_clicked = True
    print('Double clicked at x = % d, y = % d'%(event.x, event.y)) 

def actionfunc(event):
    global btn_release_flag
    global btn_double_clicked

    print(btn_release_flag)
    print(btn_double_clicked)
    if btn_release_flag:
        if btn_double_clicked:
            print("double mouse clicked event")
        else:
            print("Single mouse clicked event")

# function to be called when button-1 is single clicked 
def single_click(event): 
    global btn_double_clicked
    global btn_release_flag

    btn_double_clicked, btn_release_flag = False, False
    print('Single clicked at x = % d, y = % d'%(event.x, event.y)) 
    frame1.after(300, actionfunc, event)

def left_mouse_pressed(event):
    print('Mouse pressed at x = % d, y = % d'%(event.x, event.y)) 

def left_mouse_released(event):
    global btn_release_flag

    btn_release_flag = True
    print('Mouse released at x = % d, y = % d'%(event.x, event.y)) 


frame1 = Frame(root, height = 100, width = 200) 
  
# these lines are binding mouse 
# buttons with the Frame widget 

btn_release_flag = False
btn_double_clicked = False

frame1.bind('<Button-2>', pressed2) 
frame1.bind('<Button-3>', pressed3) 
frame1.bind('<Double 1>', double_click) 
frame1.bind('<Button 1>', single_click)
# frame1.bind('<ButtonPress 1>', left_mouse_pressed)  
frame1.bind('<ButtonRelease 1>', left_mouse_released)

frame1.pack() 
  
mainloop() 