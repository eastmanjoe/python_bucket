#!/usr/bin/env python

# URL for assignment template
# http://www.codeskulptor.org/#examples-spaceship_template.py

# URL for completed assignment
# http://www.codeskulptor.org/#user38_3ql5uvd9X1_1.py
# http://www.codeskulptor.org/#user38_3ql5uvd9X1_2.py
# http://www.codeskulptor.org/#user38_3ql5uvd9X1_3.py
# http://www.codeskulptor.org/#user38_3ql5uvd9X1_4.py


# Copy and paste below the line into CodeSkulptor
'''
    Ship
    In this phase, you will implement the control scheme for the spaceship.This
        includes a complete Spaceship class and the appropriate keyboard
        handlers to control the spaceship. Your spaceship should behave as
        follows:

    * The left and right arrows should control the orientation of your
        spaceship. While the left arrow is held down, your spaceship should turn
        counter-clockwise. While the right arrow is down, your spaceship should
        turn clockwise. When neither key is down, your ship should maintain its
        orientation. You will need to pick some reasonable angular velocity at
        which your ship should turn.

    * The up arrow should control the thrusters of your spaceship. The thrusters
        should be on when the up arrow is down and off when it is up. When the
        thrusters are on, you should draw the ship with thrust flames. When the
        thrusters are off, you should draw the ship without thrust flames.
    * When thrusting, the ship should accelerate in the direction of its forward
        vector. This vector can be computed from the orientation/angle of the
        ship using the provided helper function angle_to_vector. You will need
        to experiment with scaling each component of this acceleration vector to
        generate a reasonable acceleration.
    * Remember that while the ship accelerates in its forward direction, but the
        ship always moves in the direction of its velocity vector. Being able to
        accelerate in a direction different than the direction that you are
        moving is a hallmark of Asteroids.
    * Your ship should always experience some amount of friction. (Yeah, we
        know, "Why is there friction in the vacuum of space?". Just trust us
        there is in this game.) This choice means that the velocity should
        always be multiplied by a constant factor less than one to slow the ship
        down. It will then come to a stop eventually after you stop the
        thrusters.

    Now, implement these behaviors above in order. Each step should require just
        a few lines of code. Here are some hints:

    &- Modify the draw method for the Ship class to draw the ship image
        (without thrust flames) instead of a circle. This method should
        incorporate the ship's position and angle. Note that the angle
        should be in radians, not degrees. Since a call to the ship's draw
        method already exists in the draw handler, you should now see the ship
        image. Experiment with different positions and angles for the ship.
    &- Implement an initial version of the update method for the ship. This
        version should update the position of the ship based on its velocity.
        Since a call to the update method also already exists in the draw
        handler, the ship should move in response to different initial
        velocities.
    &- Modify the update method for the ship to increment its angle by its
        angular velocity.
    &- Make your ship turn in response to the left/right arrow keys. Add keydown
        and keyup handlers that check the left and right arrow keys. Add methods
        to the Ship class to increment and decrement the angular velocity by a
        fixed amount. (There is some flexibility in how you structure these
        methods.) Call these methods in the keyboard handlers appropriately and
        verify that you can turn your ship as you expect.
    &- Modify the keyboard handlers to turn the ship's thrusters on/off. Add a
        method to the Ship class to turn the thrusters on/off (you can make it
        take a Boolean argument which is True or False to decide if they should
        be on or off).
    &- Modify the ship's draw method to draw the thrust image when it is on.
        (The ship image is tiled and contains both images of the ship.)
    &- Modify the ship's thrust method to play the thrust sound when the thrust
        is on. Rewind the sound when the thrust turns off.
    &- Add code to the ship's update method to use the given helper function
        angle_to_vector to compute the forward vector pointing in the direction
        the ship is facing based on the ship's angle.
    &- Next, add code to the ship's update method to accelerate the ship in the
        direction of this forward vector when the ship is thrusting. You will
        need to update the velocity vector by a small fraction of the forward
        acceleration vector so that the ship does not accelerate too fast.
    &- Then, modify the ship's update method such that the ship's position wraps
        around the screen when it goes off the edge (use modular arithmetic!).
    &- Up to this point, your ship will never slow down. Finally, add friction
        to the ship's update method as shown in the "Acceleration and Friction"
        video by multiplying each component of the velocity by a number slightly
        less than 1 during each update.



    Rocks
    To implement rocks, we will use the provided Sprite class. Note that the
        update method for the sprite will be very similar to the update method
        for the ship. The primary difference is that the ship's velocity and
        rotation are controlled by keys, whereas sprites have these set randomly
        when they are created. Rocks should screen wrap in the same manner as
        the ship.

    In the template, the global variable a_rock is created at the start with
        zero velocity. Instead, we want to create version of a_rock once every
        second in the timer handler. Next week, we will add multiple rocks. This
        week, the ship will not die if it hits a rock. We'll add that next week.
        To implement rocks, we suggest the following:

    &- Complete the Sprite class (as shown in the "Sprite class" video) by
        modifying the draw handler to draw the actual image and the update
        handler to make the sprite move and rotate. Rocks do not accelerate
        or experience friction, so the sprite update method should be simpler
        than the ship update method. Test this by giving a_rock different
        starting parameters and ensuring it behaves as you expect.
    &- Implement the timer handler rock_spawner. In particular, set a_rock to be
        a new rock on every tick. (Don't forget to declare a_rock as a global
        in the timer handler.) Choose a velocity, position, and angular velocity
        randomly for the rock. You will want to tweak the ranges of these random
        numbers, as that will affect how fun the game is to play. Make sure you
        generated rocks that spin in both directions and, likewise, move in all
        directions.



    Missles
    To implement missiles, we will use the same sprite class as for rocks.
        Missiles will always have a zero angular velocity. They will also have a
        lifespan (they should disappear after a certain amount of time or you
        will eventually have missiles all over the place), but we will ignore
        that this week. Also, for now, we will only allow a single missile and
        it will not yet blow up rocks. We'll add more next week.

    Your missile should be created when you press the spacebar, not on a timer
        like rocks. They should screen wrap just as the ship and rocks do.
        Otherwise, the process is very similar:

    &- Add a shoot method to your ship class. This should spawn a new missile
        (for now just replace the old missile in a_missile). The missile's
        initial position should be the tip of your ship's "cannon". Its velocity
        should be the sum of the ship's velocity and a multiple of the ship's
        forward vector.
    &- Modify the keydown handler to call this shoot method when the spacebar
        is pressed.
    &- Make sure that the missile sound is passed to the sprite initializer so
        that the shooting sound is played whenever you shoot a missile.



    User Interface
    & Our user interface for RiceRocks simply shows the number of lives remaining
    and the score. This week neither of those elements ever change, but they
    will next week. Add code to the draw event handler to draw these on the
    canvas. Use the lives and score global variables as the current lives
    remaining and score.


    Grading Ruberic
    1 pt - The program draws the ship as an image.
    1 pt - The ship flies in a straight line when not under thrust.
    1 pt - The ship rotates at a constant angular velocity in a counter clockwise direction when the left arrow key is held down.
    1 pt - The ship rotates at a constant angular velocity in the clockwise direction when the right arrow key is held down.
    1 pt - The ship's orientation is independent of its velocity.
    1 pt - The program draws the ship with thrusters on when the up arrow is held down.
    1 pt - The program plays the thrust sound only when the up arrow key is held down.
    1 pt - The ship accelerates in its forward direction when the thrust key is held down.
    1 pt - The ship's position wraps to the other side of the screen when it crosses the edge of the screen.
    1 pt - The ship's velocity slows to zero while the thrust is not being applied.
    1 pt - The program draws a rock as an image.
    1 pt - The rock travels in a straight line at a constant velocity.
    1 pt - The rock is respawned once every second by a timer.
    1 pt - The rock has a random spawn position, spin direction and velocity.
    1 pt - The program spawns a missile when the space bar is pressed.
    1 pt - The missile spawns at the tip of the ship's cannon.
    1 pt - The missile's velocity is the sum of the ship's velocity and a multiple of its forward vector.
    1 pt - The program plays the missile firing sound when the missile is spawned.
    1 pt - The program draws appropriate text for lives on the upper left portion of the canvas.
    1 pt - The program draws appropriate text for score on the upper right portion of the canvas.
'''
#------------------------------------------------------------------------------

'''
Mini-project - Week 07

Spaceship: The Game
'''
# Mini-project #7 - Spaceship

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
# change angle by degrees
ANGLE_VEL_CHANGE = 3
FRICTION = 0.05
score = 0
lives = 3
time = 0.5

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.forward = 0
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.sound = sound


    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(
                self.image, [self.image_center[0] + self.image_size[0],
                self.image_center[1]], self.image_size, self.pos,
                self.image_size, self.angle
                )
        else:
            canvas.draw_image(
                self.image, self.image_center, self.image_size,
                self.pos, self.image_size, self.angle
                )

    def update(self):
        self.angle += self.angle_vel

        # wrap ship around screen
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        self.vel[0] *= (1 - FRICTION)
        self.vel[1] *= (1 - FRICTION)

        forward = angle_to_vector(self.angle)

        if self.thrust:
            self.vel[0] += forward[0]
            self.vel[1] += forward[1]

            self.sound.play()


    def rotate_cw(self):
        self.angle_vel += math.radians(ANGLE_VEL_CHANGE)

    def rotate_ccw(self):
        self.angle_vel -= math.radians(ANGLE_VEL_CHANGE)

    def thruster_on(self):
        self.thrust = True

    def thruster_off(self):
        self.thrust = False
        self.sound.rewind()

    def fire_missle(self):
        global a_missile

        missile_speed = 5.0
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + forward[0], self.pos[1] + forward[1]]
        missile_vel = [
            self.vel[0] + (forward[0] * missile_speed),
            self.vel[1] + (forward[1] * missile_speed)
            ]

        a_missile = Sprite(
            missile_pos, missile_vel, 0, 0,
            missile_image, missile_info, missile_sound
            )


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel

        # self.pos[0] += self.vel[0]
        # self.pos[1] += self.vel[1]
        # wrap ship around screen
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT


def draw(canvas):
    global time
    offset = 25

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    a_missile.draw(canvas)
    my_ship.draw(canvas)
    a_rock.draw(canvas)

    # update ship and sprites
    a_missile.update()
    my_ship.update()
    # my_ship.fire_missle()
    a_rock.update()

    canvas.draw_text("Score", [WIDTH // 10, HEIGHT // 10], 32, 'White')
    canvas.draw_text(str(score), [(WIDTH // 10) + offset, HEIGHT // 6], 48, 'White')
    canvas.draw_text("Lives", [WIDTH - (WIDTH // 5), HEIGHT // 10], 32, 'White')
    canvas.draw_text(str(lives), [WIDTH - (WIDTH // 5) + offset, HEIGHT // 6], 48, 'White')

# timer handler that spawns a rock
def rock_spawner():
    global a_rock

    vel_lower = -0.9
    vel_upper = 0.9
    vel_range_width = vel_upper - vel_lower

    pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
    vel = [random.random() * vel_range_width + vel_lower, random.random() * vel_range_width + vel_lower]

    ang_lower = -0.05
    ang_upper = 0.05
    ang_range_width = ang_upper - ang_lower
    angle_vel = random.random() * ang_range_width + ang_lower

    a_rock = Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info)


def keyup(key):
    KEYS = {'left': my_ship.rotate_cw, 'right': my_ship.rotate_ccw, 'up': my_ship.thruster_off}

    for i in KEYS:
        if key == simplegui.KEY_MAP[i]:
            KEYS[i]()

def keydown(key):
    KEYS = {'left': my_ship.rotate_ccw, 'right': my_ship.rotate_cw, 'up': my_ship.thruster_on, 'space':my_ship.fire_missle}

    for i in KEYS:
        if key == simplegui.KEY_MAP[i]:
            KEYS[i]()


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
a_missile = Sprite([-10, -10], [0, 0], 0, 0, missile_image, missile_info, missile_sound)
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, ship_thrust_sound)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.1, asteroid_image, asteroid_info)

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
