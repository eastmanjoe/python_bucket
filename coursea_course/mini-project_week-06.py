#!/usr/bin/env python

# URL for assignment template
# http://www.codeskulptor.org/#examples-blackjack_template.py

# URL for completed assignment
# http://www.codeskulptor.org/#user38_vITLjG598O_0.py
# http://www.codeskulptor.org/#user38_vITLjG598O_1.py

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
        self.hand = []
        self.value = 0
        self.ace_in_hand = False

    def __str__(self):
        card_string = ''
        for i in range(len(self.hand)):
            card_string += ' ' + str(self.hand[i])
        return 'Hand contains' + card_string

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        self.value = 0

        for c in self.hand:
            # print self.value, c.get_rank(), c.get_suit(), self.ace_in_hand
            self.value += VALUES[c.get_rank()]

            if c.get_rank() == 'A': self.ace_in_hand = True

        if not self.ace_in_hand:
            return self.value
        else:
            if self.value + 10 <= 21:
                return self.value + 10
            else:
                return self.value

    def draw(self, canvas, pos):
        card.draw(canvas, pos)

# define deck class
class Deck:
    def __init__(self):
        self.deck = [Card(s, r) for s in SUITS for r in RANKS]

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.deck)

    def deal_card(self):
        # pull the card from the end of the deck
        return self.deck.pop(-1)

    def __str__(self):
        deck_string = ''

        for i in range(len(self.deck)):
            deck_string += ' ' + str(self.deck[i])

        return 'Deck contains' + deck_string



#define event handlers for buttons
def deal():
    global outcome, in_play, dealer_hand, player_hand, game_deck

    game_deck = Deck()
    game_deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()

    player_hand.add_card(game_deck.deal_card())
    dealer_hand.add_card(game_deck.deal_card())
    player_hand.add_card(game_deck.deal_card())
    dealer_hand.add_card(game_deck.deal_card())

    print 'Dealer', dealer_hand
    print 'Player', player_hand

    outcome = ''
    in_play = True

def hit():
    global outcome, in_play, score, player_hand
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(game_deck.deal_card())

        if player_hand.get_value() > 21:
            outcome = "Player's hand is busted"
            in_play = False
            score -= 1

        print 'Dealer', dealer_hand
        print 'Player', player_hand
        print 'Outcome:', outcome
        print 'Score:', score

def stand():
    global outcome, in_play, score, player_hand

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while in_play:
        if dealer_hand.get_value() > 21:
            outcome = "Dealer's hand is busted"
            in_play = False
            score += 1
        elif dealer_hand.get_value() >= 17:
            in_play = False

            if dealer_hand.get_value() >= player_hand.get_value():
                outcome = "Dealer WINS !!!"
                score -= 1
            elif dealer_hand.get_value() < player_hand.get_value():
                outcome = "Player WINS !!!"
                score += 1
        else:
            dealer_hand.add_card(game_deck.deal_card())


    print 'Dealer', dealer_hand
    print 'Player', player_hand
    print 'Outcome:', outcome
    print 'Score:', score

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