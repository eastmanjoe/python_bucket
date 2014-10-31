#!/usr/bin/env python

# URL for assignment template
# http://www.codeskulptor.org/#examples-memory_template.py

# URL for completed assignment
# http://www.codeskulptor.org/#user38_maoHxmZnIx_0.py
# http://www.codeskulptor.org/#user38_maoHxmZnIx_1.py
# http://www.codeskulptor.org/#user38_maoHxmZnIx_2.py
# http://www.codeskulptor.org/#user38_maoHxmZnIx_3.py

# Copy and paste below the line into CodeSkulptor
'''
    - Example state code: http://www.codeskulptor.org/#examples-memory_states.py
'''
#------------------------------------------------------------------------------

'''
Mini-project - Week 05

Memory: The Game
'''
# implementation of card game - Memory

import simplegui
import random

num_pairs = 8
num_turns = 0
frame_width = 800
frame_height = 100
memory_lst = []
exposed = [False, False, False, False,
                    False, False, False, False,
                    False, False, False, False,
                    False, False, False, False,]
state = 0
first_click = 0
second_click = 0

# helper function to initialize globals
def new_game():
    global num_turns, memory_lst, exposed, state

    memory_lst = range(num_pairs) + range(num_pairs)
    random.shuffle(memory_lst)
    # print memory_lst
    num_turns = 0
    state = 0
    first_click = 0
    second_click = 0

    exposed = [False, False, False, False,
                    False, False, False, False,
                    False, False, False, False,
                    False, False, False, False,]


# define event handlers
def mouseclick(pos):
    global exposed, state, first_click, second_click, num_turns

    click_pos = list(pos)
    card_clicked = click_pos[0] // 50

    # determine which card clicked
    if not exposed[card_clicked]:
        if state == 0:
            state = 1
            exposed[card_clicked] = True
            first_click = card_clicked
        elif state == 1:
            exposed[card_clicked] = True
            second_click = card_clicked
            state = 2
            num_turns += 1
        else:
            if memory_lst[first_click] != memory_lst[second_click]:
                exposed[first_click] = False
                exposed[second_click] = False

            exposed[card_clicked] = True
            first_click = card_clicked
            state = 1

    # print state, first_click, second_click
    # print exposed


# cards are logically 50x100 pixels in size
def draw(canvas):
    card_width = frame_width / (num_pairs * 2)
    num_pos = [5, frame_height - frame_height / 4]
    poly_left = 0
    poly_right = card_width

    # draw cards
    for x in range(num_pairs * 2):
        if exposed[x]:
            canvas.draw_text(str(memory_lst[x]), num_pos, 72, 'White')
            canvas.draw_polygon([[poly_left, 0], [poly_right, 0], [poly_right , frame_height], [poly_left , frame_height]], 1, 'Red')
        else:
            canvas.draw_polygon([[poly_left, 0], [poly_right, 0], [poly_right , frame_height], [poly_left , frame_height]], 1, 'Black', 'Green')

        poly_left += card_width
        poly_right += card_width
        num_pos[0] += card_width

    label.set_text("Turns = " + str(num_turns))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", frame_width, frame_height)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
