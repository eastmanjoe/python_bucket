#!/usr/bin/env python

# URL for assignment template
# http://www.codeskulptor.org/#examples-blackjack_template.py

# URL for completed assignment
# http://www.codeskulptor.org/#user38_vITLjG598O_0.py

# Copy and paste below the line into CodeSkulptor
'''
    - Card Class Testing: http://www.codeskulptor.org/#examples-card_template.py
    - Hand Class Testing: http://www.codeskulptor.org/#examples-hand_template.py
    - Draw Class Testing: http://www.codeskulptor.org/#examples-deck_template.py
'''
#------------------------------------------------------------------------------

'''
Mini-project - Week 06

Blackjack: The Game
'''
# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.card_lst = []

    def __str__(self):
        card_string = ''
        for i in range(len(self.card_lst)):
            card_string += ' ' + str(self.card_lst[i])
        return 'Hand contains' + card_string

    def add_card(self, card):
        self.card_lst.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value =
        return hand_value

    def draw(self, canvas, pos):
        pass    # draw a hand on the canvas, use the draw method for cards


# define deck class
class Deck:
    def __init__(self):
        self.deck = []

        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop(0)

    def __str__(self):
        deck_string = ''
        for i in range(len(self.deck)):
            deck_string += ' ' + str(self.deck[i])
        return 'Deck contains' + deck_string



#define event handlers for buttons
def deal():
    global outcome, in_play

    # your code goes here

    in_play = True

def hit():
    pass    # replace with your code below

    # if the hand is in play, hit the player

    # if busted, assign a message to outcome, update in_play and score

def stand():
    pass    # replace with your code below

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below

    card = Card("S", "A")
    card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric