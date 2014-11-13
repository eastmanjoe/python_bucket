#!/usr/bin/env python

# URL for assignment template
# http://www.codeskulptor.org/#examples-ricerocks_template.py

# URL for completed assignment
# http://www.codeskulptor.org/#user38_3ql5uvd9X1_1.py
# http://www.codeskulptor.org/#user38_3ql5uvd9X1_2.py
# http://www.codeskulptor.org/#user38_3ql5uvd9X1_3.py
# http://www.codeskulptor.org/#user38_3ql5uvd9X1_4.py
# http://www.codeskulptor.org/#user38_3ql5uvd9X1_5.py - Splash Screen
# http://www.codeskulptor.org/#user38_3ql5uvd9X1_6.py - Collisions
# http://www.codeskulptor.org/#user38_3ql5uvd9X1_7.py - Missle Lifespan


# Copy and paste below the line into CodeSkulptor
'''

'''
#------------------------------------------------------------------------------

'''
Mini-project - Week 08

RiceRocks: The Game
'''
# Mini-project #8 - Spaceship

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
# change angle by degrees
ANGLE_VEL_CHANGE = 3
FRICTION = 0.02
score = 0
lives = 3
time = 0.5
rock_group = set([])
missile_group = set([])
started = False

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

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

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
        global missile_group

        missile_speed = 6.0
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [
            self.vel[0] + (forward[0] * missile_speed),
            self.vel[1] + (forward[1] * missile_speed)
            ]

        a_missile = Sprite(
            missile_pos, missile_vel, 0, 0,
            missile_image, missile_info, missile_sound, missile_info.get_lifespan()
            )

        missile_group.add(a_missile)

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None, lifespan = None):
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

        # wrap ship around screen
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        if self.lifespan != None:
            if self.age >= self.lifespan:
                return True
            else:
                self.age += 1

        return False

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def collide(self, other_sprite):
        if dist(other_sprite.get_position(), self.pos) < (other_sprite.get_radius() + self.radius):
            return True
        else:
            return False


def draw(canvas):
    global time, lives
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
    my_ship.draw(canvas)

    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)

    # update ship and sprites
    my_ship.update()

    if group_collide(rock_group, my_ship):
        lives -= 1

    # if group_group_collide(rock_group, missile_group):

    canvas.draw_text("Lives", [WIDTH // 10, HEIGHT // 10], 32, 'White')
    canvas.draw_text(str(lives), [(WIDTH // 10) + offset, HEIGHT // 6], 48, 'White')
    canvas.draw_text("Score", [WIDTH - (WIDTH // 5), HEIGHT // 10], 32, 'White')
    canvas.draw_text(str(score), [WIDTH - (WIDTH // 5) + offset, HEIGHT // 6], 48, 'White')

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())

# timer handler that spawns a rock
def rock_spawner():
    global rock_group

    vel_lower = -0.9
    vel_upper = 0.9
    vel_range_width = vel_upper - vel_lower

    pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
    vel = [random.random() * vel_range_width + vel_lower, random.random() * vel_range_width + vel_lower]

    ang_lower = -0.05
    ang_upper = 0.05
    ang_range_width = ang_upper - ang_lower
    angle_vel = random.random() * ang_range_width + ang_lower

    if len(rock_group) < 12:
        a_rock = Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)


def process_sprite_group(canvas, sprite_group):
    for sp in set(sprite_group):
        sp.draw(canvas)

        if sp.update():
            sprite_group.discard(sp)


def group_collide(group, other_object):
    for obj in set(group):
        if obj.collide(other_object):
            group.remove(obj)
            return True

    return False


def group_group_collide(group1, group2):
    count = 0

    for obj in set(group1):
        if group_collide(group2, obj):
            group1.discard(obj)
            count +=1

    return count



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


def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, ship_thrust_sound)
# missile_group = Sprite([-10, -10], [0, 0], 0, 0, missile_image, missile_info, missile_sound)
# rock_group = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.1, asteroid_image, asteroid_info)

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
