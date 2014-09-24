#!/usr/bin/env python

'''
Quiz 1 functions
'''

import math

def f(x):
    return (-5 * (x ** 5)) + (69 * (x ** 2)) - 47

print f(0), f(1), f(2), f(3)


def future_value(present_value, annual_rate, periods_per_year, years):
    rate_per_period = annual_rate / periods_per_year
    periods = periods_per_year * years

    return present_value * (1 + rate_per_period) ** periods

# future_value(500, .04, 10, 10) = 745.317442824
print "$5000 at 4% compounded monthly for 10 years yields $", future_value(500, .04, 10, 10)
print "$1000 at 2% compounded daily for 3 years yields $", future_value(1000, .02, 365, 3)


def area_of_polygon(num_of_sides, length_of_sides):
    return ((1.0/4) * num_of_sides * (length_of_sides ** 2)) / math.tan(math.pi / num_of_sides)

# 84.3033926289
print area_of_polygon(5, 7)
print area_of_polygon(7, 3)


def project_to_distance(point_x, point_y, distance):
    dist_to_origin = math.sqrt(point_x ** 2 + point_y ** 2)
    scale = distance / dist_to_origin
    print point_x * scale, point_y * scale

project_to_distance(2, 7, 4)