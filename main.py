#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os,sys, time,datetime
import tkinter as tk
from PIL import Image,ImageTk
#import RPi.GPIO as GPIO
import serial
from tkinter import Tk, ttk,PhotoImage
import read, chmod


chmod.main()
"""
GPIO.setmode(GPIO.BCM)
esc1_pin = 14
esc2_pin = 15
h1_led_pin = 19
h2_led_pin = 26
t1_led_pin = 6
t2_led_pin = 13
side_led_pin = 12


GPIO.setup(esc1_pin,GPIO.OUT)
GPIO.setup(esc2_pin,GPIO.OUT)
GPIO.setup(h1_led_pin,GPIO.OUT)
GPIO.setup(h2_led_pin,GPIO.OUT)
GPIO.setup(t1_led_pin,GPIO.OUT)
GPIO.setup(t2_led_pin,GPIO.OUT)
GPIO.setup(side_led_pin,GPIO.OUT)
esc1 = GPIO.PWM(esc1_pin,50)
esc1.start(0)
esc1.ChangeDutyCycle(7.36)
esc2 = GPIO.PWM(esc2_pin,50)
esc2.start(0)
esc2.ChangeDutyCycle(7.36)
GPIO.output(h1_led_pin,0)
GPIO.output(h2_led_pin,0)
GPIO.output(t1_led_pin,0)
GPIO.output(t2_led_pin,0)
GPIO.output(side_led_pin,0)
time.sleep(5)
"""
nucleo = serial.Serial('/dev/ttyACM0',timeout=0.08)
read.setup()

global rotation_state
rotation_state = 0
global headlight_state
headlight_state = 0
global taillight_state
taillight_state = 0
global shutdown
shutdown = 1

root = tk.Tk()
root.title("5inch_controller")
root.geometry("800x480")
root.attributes("-fullscreen",True)
canvas = tk.Canvas(root,bg="black",width = 800,height = 480)
back_image = Image.open('bg.png')
back_image = back_image.resize((800,480))
back_image = ImageTk.PhotoImage(back_image)
canvas.create_image(0,0,image = back_image,anchor=tk.NW)
canvas.create_oval(707,310,769,372,fill='yellow')

def quit_button_pushed():
    """
    esc1.stop()
    esc2.stop()
    GPIO.cleanup()
    """
    nucleo.close()
    root.destroy()
    tk.sys.exit(0)

quit_button = tk.Button(root,text="x",command=quit_button_pushed)

#F/R button
def f_button_pushed():
    global rotation_state
    global shutdown
    rotation_state = 1
    f_button.configure(image=f_button_on_img)
    r_button.configure(image=r_button_img)
    canvas.delete("n_lamp")
    canvas.create_oval(545,300,607,362,tag="n_lamp",fill="gray")
    shutdown = 0
    #GPIO.output(side_led_pin,1)

def r_button_pushed():
    global rotation_state
    global shutdown
    rotation_state = -1
    r_button.configure(image=r_button_on_img)
    f_button.configure(image=f_button_img)
    canvas.delete("n_lamp")
    canvas.create_oval(545,300,607,362,tag="n_lamp",fill="gray")
    shutdown = 0
    #GPIO.output(side_led_pin,1)
    

f_button_img = Image.open('f_button_r.png')
f_button_img = f_button_img.resize((45,40))
f_button_img = ImageTk.PhotoImage(f_button_img)
f_button_on_img = Image.open('f_button_p.png')
f_button_on_img = f_button_on_img.resize((45,40))
f_button_on_img = ImageTk.PhotoImage(f_button_on_img)
f_button = tk.Button(root,image=f_button_img,command=f_button_pushed)
r_button_img = Image.open('r_button_r.png')
r_button_img = r_button_img.resize((45,40))
r_button_img = ImageTk.PhotoImage(r_button_img)
r_button_on_img = Image.open('r_button_p.png')
r_button_on_img = r_button_on_img.resize((45,40))
r_button_on_img = ImageTk.PhotoImage(r_button_on_img)
r_button = tk.Button(root,image=r_button_img,command=r_button_pushed)
canvas.create_oval(545,300,607,362,tag="n_lamp",fill="green")
f_button.place(x=620,y=320)
r_button.place(x=620,y=390)

def emg_pushed():
    global rotation_state
    global shutdown
    rotation_state = 0
    r_button.configure(image=r_button_img)
    f_button.configure(image=f_button_img)
    canvas.create_oval(545,300,607,362,tag="n_lamp",fill="green")
    shutdown = 1
    #GPIO.output(side_led_pin,0)
    
emg_img = Image.open('emgsw.png')
emg_img = emg_img.resize((62,62))
emg_img = ImageTk.PhotoImage(emg_img)
emg_button = tk.Button(root,image=emg_img,bd=0,command=emg_pushed)
emg_button.place(x=545,y=390)

#canvas.create_line()

#Headlight,Taillight
def head_on():
    global headlight_state
    headlight_state = 1
    head_on_sw.configure(fg='#ffffff',bg='#ff0000')
    head_off_sw.configure(fg='#000000',bg='#ffffff')
    
def head_off():
    global headlight_state
    headlight_state = 0
    head_on_sw.configure(fg='#000000',bg='#ffffff')
    head_off_sw.configure(fg='#ffffff',bg='#ff0000')
    #GPIO.output(h1_led_pin,0)
    #GPIO.output(h2_led_pin,0)
    
head_on_sw = tk.Button(root,text='ON',fg='#000000',bg='#ffffff',font=("","12","bold"),command=head_on)
head_on_sw.place(x=210,y=108)
head_off_sw = tk.Button(root,text='OFF',fg='#000000',bg='#ffffff',font=("","12","bold"),command=head_off)
head_off_sw.place(x=290,y=108)

def tail_on():
    global taillight_state
    taillight_state = 1
    tail_on_sw.configure(fg='#ffffff',bg='#ff0000')
    tail_off_sw.configure(fg='#000000',bg='#ffffff')
    
def tail_off():
    global taillight_state
    taillight_state = 0
    tail_on_sw.configure(fg='#000000',bg='#ffffff')
    tail_off_sw.configure(fg='#ffffff',bg='#ff0000')
    #GPIO.output(t1_led_pin,0)
    #GPIO.output(t2_led_pin,0)

tail_on_sw = tk.Button(root,text='ON',fg='#000000',bg='#ffffff',font=("","12","bold"),command=tail_on)
tail_on_sw.place(x=210,y=148)
tail_off_sw = tk.Button(root,text='OFF',fg='#000000',bg='#ffffff',font=("","12","bold"),command=tail_off)
tail_off_sw.place(x=290,y=148)

canvas.place(x=0,y=0)
quit_button.place(x=0,y=0)
mas_data = tk.StringVar()
bra_data = tk.StringVar()

def show_bar(mas,bra):
    if mas==0:
        canvas.delete("mas1")
        canvas.delete("mas2")
        canvas.delete("mas3")
        canvas.delete("mas4")
        canvas.delete("mas5")
    elif mas == 1:
        canvas.create_line(82,442,234,442,width=24,fill='blue',tag="mas1")
        canvas.delete("mas2")
        canvas.delete("mas3")
        canvas.delete("mas4")
        canvas.delete("mas5")
    elif mas == 2:
        canvas.create_line(82,442,234,442,width=24,fill='blue',tag="mas1")
        canvas.create_line(82,415,234,415,width=24,fill='blue',tag="mas2")
        canvas.delete("mas3")
        canvas.delete("mas4")
        canvas.delete("mas5")
    elif mas == 3:
        canvas.create_line(82,442,234,442,width=24,fill='blue',tag="mas1")
        canvas.create_line(82,415,234,415,width=24,fill='blue',tag="mas2")
        canvas.create_line(82,388,234,388,width=24,fill='blue',tag="mas3")
        canvas.delete("mas4")
        canvas.delete("mas5")
    elif mas == 4:
        canvas.create_line(82,442,234,442,width=24,fill='blue',tag="mas1")
        canvas.create_line(82,415,234,415,width=24,fill='blue',tag="mas2")
        canvas.create_line(82,388,234,388,width=24,fill='blue',tag="mas3")
        canvas.create_line(82,361,234,361,width=24,fill='blue',tag="mas4")
        canvas.delete("mas5")
    else:
        canvas.create_line(82,442,234,442,width=24,fill='blue',tag="mas1")
        canvas.create_line(82,415,234,415,width=24,fill='blue',tag="mas2")
        canvas.create_line(82,388,234,388,width=24,fill='blue',tag="mas3")
        canvas.create_line(82,361,234,361,width=24,fill='blue',tag="mas4")
        canvas.create_line(82,334,234,334,width=24,fill='blue',tag="mas5")
    canvas.create_polygon(81,455,81,308,200,455,fill='black')
    
def send(mascon,brake,rot_sta,headlight,taillight,SD):
    if rot_sta == 1:
        forward = 1
        backward = 0
    elif rot_sta == -1:
        forward = 0
        backward = 1
    else:
        forward = 0
        backward = 0
        
    nucleo.write(bytes([0xff,mascon,brake,forward,backward,headlight,taillight,SD]))
    
    
def controll():
    data = read.main()
    send(data[0],data[1],rotation_state,headlight_state,taillight_state,shutdown)
    """
    if data[0] == 0 or rotation_state == 0:
        #esc1.ChangeDutyCycle(7.36)
        #esc2.ChangeDutyCycle(7.36)
        if rotation_state == 1:
            if headlight_state == 1:
                #GPIO.output(h1_led_pin,1)
                #GPIO.output(h2_led_pin,0)
            if taillight_state == 1:
                #GPIO.output(t1_led_pin,1)
                #GPIO.output(t2_led_pin,0)
        else:
            if headlight_state == 1:
                #GPIO.output(h2_led_pin,1)
                #GPIO.output(h1_led_pin,0)
            if taillight_state == 1:
                #GPIO.output(t1_led_pin,1)
                #GPIO.output(t2_led_pin,0)
    else:
        if rotation_state == 1:
            #esc1.ChangeDutyCycle(data[0] * 0.3 + 7.36)
            #esc2.ChangeDutyCycle(7.36 - data[0] * 0.8)
            if headlight_state == 1:
                #GPIO.output(h1_led_pin,1)
                #GPIO.output(h2_led_pin,0)
            if taillight_state == 1:
                #GPIO.output(t1_led_pin,1)
                #GPIO.output(t2_led_pin,0)
        else:
            #esc2.ChangeDutyCycle(data[0] * 0.3 + 7.36)
            #esc1.ChangeDutyCycle(7.36 - data[0] * 0.8)
            if headlight_state == 1:
                #GPIO.output(h2_led_pin,1)
                #GPIO.output(h1_led_pin,0)
            if taillight_state == 1:
                #GPIO.output(t1_led_pin,1)
                #GPIO.output(t2_led_pin,0)
    #print(str(headlight_state))        
    """
    show_bar(data[0],data[1])
    dt_now = datetime.datetime.now()
    if dt_now.hour < 10:
        now_h = '0' + str(dt_now.hour)
    else:
        now_h = str(dt_now.hour)
    if dt_now.minute < 10:
        now_m = '0' + str(dt_now.minute)
    else:
        now_m = str(dt_now.minute)
    if dt_now.second < 10:
        now_s = '0' + str(dt_now.second)
    else:
        now_s = str(dt_now.second)

    
    now_time.set(str(dt_now.year) + str(dt_now.month) + '0' + str(dt_now.day) + ' ' + now_h + ':' + now_m + ' ' + now_s)
    """
    data[0] = str(data[0])
    data[1] = str(data[1])
    mas_data.set(data[0])
    bra_data.set(data[1])
    """
    root.after(100,controll)
    
data = read.main()
"""
data[0] = str(data[0])
data[1] = str(data[1])
mas_data.set(data[0])
bra_data.set(data[1])
mas_label = tk.Label(root,textvariable=mas_data,fg="white")
mas_label.place(x=680,y=90)
bra_label = tk.Label(root,textvariable=bra_data,fg="white")
bra_label.place(x=735,y=90)
"""
dt_now = datetime.datetime.now()
now_time = tk.StringVar()
if dt_now.hour < 10:
    now_h = '0' + str(dt_now.hour)
else:
    now_h = str(dt_now.hour)
if dt_now.minute < 10:
    now_m = '0' + str(dt_now.minute)
else:
    now_m = str(dt_now.minute)

now_time.set(str(dt_now.year) + str(dt_now.month) + '0' + str(dt_now.day) + ' ' + now_h + ':' + now_m)
time_label = tk.Label(root,textvariable=now_time,fg="white",bg='black',font=("","14",""))
time_label.place(x=33,y=25)

 
controll()

root.mainloop()
