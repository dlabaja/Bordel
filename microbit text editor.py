from microbit import *

input.on_button_pressed(Button.A, on_button_pressed_a)
input.on_button_pressed(Button.B, on_button_pressed_b)
input.on_button_pressed(Button.AB, on_button_pressed_ab)
input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_event_pressed)
input.on_logo_event(TouchButtonEvent.LONG_PRESSED, on_logo_event_long_pressed)

#abeceda, znaky + space
abecedaMala = "_abcdefghijklmnopqrstuvwxyz"
abecedaVelka = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
znaky = "_,.0123456789:!?-/;()[]{}=%"
listy = [abecedaMala, abecedaVelka, znaky]
curlist = abecedaMala

index = 0 #0-26
mode = 0 #0-3
msg = ""
basic.show_string(curlist[0])

def on_button_pressed_a():
    basic.show_string(curlist[set_index(-1)])

def on_button_pressed_b():
    basic.show_string(curlist[set_index(1)])

def on_button_pressed_ab():
    global curlist

    curlist = listy[add_mode()];
    basic.show_string(curlist[index])

def on_logo_event_pressed():
    global msg
    msg = msg + curlist[index] 

def on_logo_event_long_pressed():
    global msg
    basic.show_string(msg)
    msg = ""

def set_index(offset):
    global index
    index = index + offset
    if index > 26:
        index = 0
    if index < 0:
        index = 26
    return index

def add_mode():
    global mode
    mode = mode + 1
    if mode > 2:
        mode = 0
    return mode
