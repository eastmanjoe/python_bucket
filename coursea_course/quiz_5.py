#!/usr/bin/env python

'''
Quiz 5 functions
'''

import math

# Quix 5a
print "Question 3"
fruits = ["apple", "pear", "blueberry"]
fruit = fruits.pop(0)
print fruit, fruits

print "Question 4"
print range(2, 15, 3)

print "Question 5"
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
product = 1
for n in numbers:
    product *= n
print product

print "Question 6"

def reverse_string(s):
    """Returns the reversal of the given string."""
    result = ""
    for char in s:
        result = char + result
    return result

print reverse_string("hello")

print "Question 7"
import random

def random_point():
    """Returns a random point on a 100x100 grid."""
    return (random.randrange(100), random.randrange(100))

def starting_points(players):
    """Returns a list of random points, one for each player."""
    points = []
    for player in players:
        point = random_point()
        points.append(point)
    return points

print starting_points([1, 2, 3])

print "Question 8"
def is_ascending(numbers):
    """Returns whether the given list of numbers is in ascending order."""
    for i in range(len(numbers) - 1):
        if numbers[i+1] < numbers[i]:
            return False
    return True

print is_ascending([2, 6, 9, 12, 400])
print is_ascending([4, 8, 2, 13])

print "Question 9"
lst = [0, 1]

for x in range(1, 41):
    lst.append(lst[x-1] + lst[x])

print lst

# Quiz 5b

print "Question 7"
my_list = [2,3,6,9,2,7]


def is_even(number):
    """Returns whether the number is even."""
    return number % 2 == 0

#print [if is_even(number): number for number in my_list]
print [n for n in my_list if is_even(n)]
print [number for number in my_list if is_even(number)]
print [is_even(number) for number in my_list]

print "Question 8"
import simplegui

frame_size = [200, 200]
image_size = [1521, 1818]

def draw(canvas):
    canvas.draw_image(image,
                      [image_size[0] / 2, image_size[1] / 2], image_size,
                      [frame_size[0] / 2, frame_size[1] / 2], frame_size)

frame = simplegui.create_frame("test", frame_size[0], frame_size[1])
frame.set_draw_handler(draw)
image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/gutenberg.jpg")

frame.start()


print "Question 9"
import simplegui

frame_size = [200, 200]
image_size = [100, 100]

def draw(canvas):
    canvas.draw_image(image, [220, 100], image_size, [frame_size[0] / 2, frame_size [1]/ 2], frame_size)

frame = simplegui.create_frame("test", frame_size[0], frame_size[1])
frame.set_draw_handler(draw)
image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/alphatest.png")

frame.start()