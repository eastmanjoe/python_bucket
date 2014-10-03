#!/usr/bin/env python

# URL for assignment template
# http://www.codeskulptor.org/#examples-guess_the_number_template.py

# URL for completed assignment
# http://www.codeskulptor.org/#user38_JkUTMa0hHG_0.py
# http://www.codeskulptor.org/#user38_JkUTMa0hHG_1.py
# http://www.codeskulptor.org/#user38_JkUTMa0hHG_2.py

# Copy and paste below the line into CodeSkulptor
#------------------------------------------------------------------------------
'''
Mini-project - Week 02

Guess the Number Game
input will come from buttons and an input field
all output for the game will be printed in the console
'''

import simplegui
import math
import random

secret_number_range = 100
guesses_remaining = 7

# helper function to start and restart the game
def new_game():
    ''' starts the new game, resets the secret number and the number of guesses'''
    global secret_number
    global guesses_remaining

    # set the number of guesses based on the secret number range
    if secret_number_range == 100:
        guesses_remaining = 7
    elif secret_number_range == 1000:
        guesses_remaining = 10

    # calculate the number of guesses based on the secret number range [2 ** n >= high - low + 1]
    # guesses_remaining = (secret_number_range - 0 + 1)

    # generate the secret number
    secret_number = random.randrange(0, secret_number_range)

    #print the starting messages of a new game
    print 'New Game.  Range is from 0 to', secret_number_range
    print 'Number of remaining guesses is', guesses_remaining
    print ''


# define event handlers for control panel
def range100():
    ''' button sets the secret number range to [0, 100) and starts a new game '''
    global secret_number_range

    secret_number_range = 100
    new_game()


def range1000():
    ''' button sets the secret number range to [0, 1000) and starts a new game '''

    global secret_number_range

    secret_number_range = 1000
    new_game()


def input_guess(guess):
    ''' input field to capture the players guess and determine in the guess matches the secret number'''

    global guesses_remaining

    print 'Guess was', guess
    guess = int(guess)

    guesses_remaining -= 1

    print 'Number of remaining guesses is', guesses_remaining

    if guesses_remaining >= 0 and secret_number == guess:
            print 'Correct!'
            print ''
            new_game()
    elif guesses_remaining == 0:
        print 'You ran out of guesses.  The number was', secret_number
        print ''
        new_game()
    else:
        if secret_number > guess:
            print 'Higher!'
            print ''
        else:
            print 'Lower!'
            print ''


# create frame
frame = simplegui.create_frame('Guess the Number Game', 200, 200)
frame.add_button('Range: 0 - 100', range100, 125)
frame.add_button('Range: 0 - 1000', range1000, 125)
frame.add_input('Input Guess', input_guess, 125)

# call new_game
new_game()
