#!/usr/bin/env python

# URL for assignment template
# http://www.codeskulptor.org/#examples-stopwatch_template.py

# URL for completed assignment
# http://www.codeskulptor.org/#user38_CyoiYPSDMg_1.py
# http://www.codeskulptor.org/#user38_CyoiYPSDMg_2.py - working timer

# Copy and paste below the line into CodeSkulptor
#------------------------------------------------------------------------------

'''
Mini-project - Week 03

Stopwatch: The Game

'''
import simplegui

# define global variables
stopwatch_counter = 0
stopwatch_total_stops = 0
stopwatch_win_stops = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    # tenths of seconds is the remainder after dividing by 10
    tenths_of_seconds = t % 10

    # number of seconds is the integer portion after dividing by 10
    num_of_seconds = t // 10

    # number of seconds less that a minute is the remainder after dividing by 60
    # the whole seconds is the remainder of the number of seconds divided by 10
    # the tens of seconds is the integer of the number of seconds divided by 10
    whole_seconds = (num_of_seconds % 60) % 10
    tens_of_seconds = (num_of_seconds % 60) // 10

    # number of minutes is the integer portion after dividing by 60
    minutes = num_of_seconds // 60

    # print minutes, tens_of_seconds, whole_seconds, tenths_of_seconds

    return str(minutes) + ':' + str(tens_of_seconds) + str(whole_seconds) + '.' + str(tenths_of_seconds)


# define event handlers for buttons; "Start", "Stop", "Reset"
def stopwatchStart():
    timer.start()

def stopwatchStop():
    global stopwatch_total_stops, stopwatch_win_stops

    timer.stop()

def stopwatchReset():
    global stopwatch_counter

    timer.stop()

    stopwatch_counter = 0
    stopwatch_total_stops = 0
    stopwatch_win_stops = 0

# define event handler for timer with 0.1 sec interval
def stopwatchTimerHandler():
    global stopwatch_counter

    stopwatch_counter += 1


def stopwatchDrawHandler(canvas):
    canvas.draw_text(format(stopwatch_counter), (40, 110), 36, 'White')


# create frame
frame = simplegui.create_frame('Stopwatch: The Game', 200, 200)
frame.add_button('Start', stopwatchStart, 100)
frame.add_button('Stop', stopwatchStop, 100)
frame.add_button('Reset', stopwatchReset, 100)
frame.set_draw_handler(stopwatchDrawHandler)
frame.start()

#create timer with 0.1 second tick
timer = simplegui.create_timer(100, stopwatchTimerHandler)
