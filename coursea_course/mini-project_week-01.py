#!/usr/bin/env python

'''
Mini-project - Week 01

Rock-Paper-Scissors-Lizard-Spock
'''
# URL for assignment tempalte
# http://www.codeskulptor.org/#examples-rpsls_template.py

# URL for completed assignement
# http://www.codeskulptor.org/#user38_SehaoMH3RD_0.py
# http://www.codeskulptor.org/#user38_SehaoMH3RD_1.py

# Copy and paste below the line into CodeSkulptor
#------------------------------------------------------------------------------
# Rock-paper-scissors-lizard-Spock Mini-Project

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

# helper functions
def name_to_number(name):
    if name == "rock":
        number = 0
    elif name == "Spock":
        number = 1
    elif name == "paper":
        number = 2
    elif name == "lizard":
        number = 3
    elif name == "scissors":
        number = 4
    else:
        print "Does not match a valid hand signal name"

    return number


def number_to_name(number):
    if number == 0:
        name = "rock"
    elif number == 1:
        name = "Spock"
    elif number == 2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    elif number == 4:
        name = "scissors"
    else:
        print "Does not match a valid hand signal number"

    return name

def rpsls(player_choice):
    print ""
    print "Player chooses", player_choice
    player_number = name_to_number(player_choice)

    # generate the computers guess
    comp_number = random.randrange(0, 5)
    comp_choice = number_to_name(comp_number)
    print "Computer chooses", comp_choice

    # determine the winner
    difference = (player_number - comp_number) % 5

    if (difference == 1) or (difference == 2):
        print "Player wins!"
    elif (difference == 3) or (difference == 4):
        print "Computer wins!"
    else:
        print "Player and computer tie!"

rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
