#!/usr/bin/env python

# URL for assignment template
# http://www.codeskulptor.org/#examples-stopwatch_template.py

# URL for completed assignment
# http://www.codeskulptor.org/#user38_7nbDBIPd0E_4.py
# http://www.codeskulptor.org/#user38_7nbDBIPd0E_5.py
# http://www.codeskulptor.org/#user38_7nbDBIPd0E_6.py

# Copy and paste below the line into CodeSkulptor
#------------------------------------------------------------------------------

'''
Mini-project - Week 04

Pong: The Game

TODO:
    - Draw score
    - Determine if ball hits paddle
    - Vary ball speed with time
'''

# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
CANVAS_HEIGHT = 450
SCORE_AREA_HEIGHT = 50
HEIGHT = CANVAS_HEIGHT - SCORE_AREA_HEIGHT
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initial positions and velocities
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [0, 0]
ball_vel_increase_percent = 10
paddle1_pos = HEIGHT // 2
paddle2_pos = HEIGHT // 2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH // 2, HEIGHT // 2]

    # canvas is drawn at 60 times per second
    ball_vel = [random.randrange(120, 240) / 60.0, random.randrange(60, 180) / 60.0]

    if direction == LEFT:
        ball_vel[0] = -ball_vel[0]
        ball_vel[1] = -ball_vel[1]
    elif direction == RIGHT:
        ball_vel[1] = -ball_vel[1]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    paddle1_pos = HEIGHT // 2
    paddle2_pos = HEIGHT // 2
    paddle1_vel = 0
    paddle2_vel = 0

    score1 = 0
    score2 = 0


    if random.randrange(0, 2) == 1:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    #score area line
    canvas.draw_line([0, CANVAS_HEIGHT - SCORE_AREA_HEIGHT],[WIDTH, CANVAS_HEIGHT - SCORE_AREA_HEIGHT], 1, 'White')
    # midline
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, 'White')
    # left gutter
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, 'White')
    # right gutter
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, 'White')


    # check if ball collides with sides
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS > HEIGHT:
        ball_vel[1] = -ball_vel[1]

    # check if ball collides with gutters, but not the paddles
    elif ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        # check if ball hits paddle, if not player 2 scores
        if (ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT)  and (ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT):
            ball_vel[0] = -(ball_vel[0] * 1.1)
            # ball_vel[1] = -(ball_vel[1] * 1.1)
        else:
            spawn_ball(RIGHT)
            score2 += 1
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        # check if ball hits paddle, if not player 1 scores
        if (ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT) and (ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT):
            ball_vel[0] = -(ball_vel[0] * 1.1)
            # ball_vel[1] = -(ball_vel[1] * 1.1)
        else:
            spawn_ball(LEFT)
            score1 += 1

    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # print 'ball_pos:', ball_pos, 'ball_vel:', ball_vel

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 4, 'White', 'Green')

    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel) - HALF_PAD_HEIGHT >= 0 and (paddle1_pos + paddle1_vel) + HALF_PAD_HEIGHT <= HEIGHT:
        paddle1_pos += paddle1_vel

    if (paddle2_pos + paddle2_vel) - HALF_PAD_HEIGHT >= 0 and (paddle2_pos + paddle2_vel) + HALF_PAD_HEIGHT <= HEIGHT:
        paddle2_pos += paddle2_vel

    # print 'paddle1_pos:', paddle1_pos, 'paddle2_pos:', paddle2_pos

    # draw paddles
    # paddleX_pos_points = [[TOP LEFT], [BOTTOM LEFT], [BOTTOM RIGHT], [TOP LEFT]]
    paddle1_pos_points = [[0, paddle1_pos - HALF_PAD_HEIGHT],
                        [0, paddle1_pos + HALF_PAD_HEIGHT],
                        [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT],
                        [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT]]

    paddle2_pos_points = [[WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT],
                        [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT],
                        [WIDTH, paddle2_pos + HALF_PAD_HEIGHT],
                        [WIDTH, paddle2_pos - HALF_PAD_HEIGHT]]

    canvas.draw_polygon(paddle1_pos_points, 1, 'Yellow', 'Yellow')
    canvas.draw_polygon(paddle2_pos_points, 1, 'Yellow', 'Yellow')

    # draw scores
    canvas.draw_text('SCORE', (WIDTH // 2 - 25, CANVAS_HEIGHT - 5), 16, 'White')
    canvas.draw_text(str(score1), (WIDTH // 2 + 40, CANVAS_HEIGHT - 20), 35, 'White')
    canvas.draw_text('Player 1', (WIDTH // 10, CANVAS_HEIGHT - 20), 25, 'White')
    canvas.draw_text('w = up, s = down', (WIDTH // 10, CANVAS_HEIGHT - 5), 12, 'White')
    canvas.draw_text('Player 2', (WIDTH - (WIDTH // 4), CANVAS_HEIGHT - 20), 25, 'White')
    canvas.draw_text('up arrow = up, down arrow = down', (WIDTH - (WIDTH // 3), CANVAS_HEIGHT - 5), 12, 'White')
    canvas.draw_text(str(score2), (WIDTH // 2 - 55, CANVAS_HEIGHT - 20), 35, 'White')

def keydown(key):
    global paddle1_vel, paddle2_vel
    paddle_speed = 10

    if key == simplegui.KEY_MAP['w']:
            paddle1_vel = -paddle_speed
    elif key == simplegui.KEY_MAP['s']:
            paddle1_vel = paddle_speed
    elif key == simplegui.KEY_MAP['up']:
            paddle2_vel = -paddle_speed
    elif key == simplegui.KEY_MAP['down']:
            paddle2_vel = paddle_speed


def keyup(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0

def resetButtonHandler():
    new_game()

# create frame
frame = simplegui.create_frame('Pong', WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset', resetButtonHandler,100)

# start frame
new_game()
frame.start()
