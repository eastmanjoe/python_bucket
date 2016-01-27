#!/usr/bin/env python
#
#
#
'''
This program performs calcs on dates
'''

#---------------------------------------------------------------------------#
import argparse
from datetime import timedelta, datetime, date

__version__ = '1.0.0'

def AddBusinessDays(from_date, add_days):
    business_days_to_add = add_days
    current_date = from_date

    while business_days_to_add > 0:
        current_date += timedelta(days=1)

        # check if current date is a week day (saturday = 5, sunday = 6)
        # if the date is the weekend, then don't count the day as added
        if current_date.weekday() < 5:
            business_days_to_add -= 1

    return current_date


def AddCalendarDays(from_date, add_days):
    calendar_days_to_add = add_days
    current_date = from_date

    while calendar_days_to_add > 0:
        current_date += timedelta(days=1)

        calendar_days_to_add -= 1

    return current_date

#---------------------------------------------------------------------------#
if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     'from_date', help='date in the form of 'YYYY-MM-DD',
    #     default='01-27-2015'
    #     )
    # parser.add_argument(
    #     'add_days', help='first date',
    #     default='40'
    #     )
    # parser.add_argument(
    #     '-v', '--version', action='version',version='%(prog)s ' + __version__
    #     )
    # args = parser.parse_args()

    from_date = date.today()
    add_days = 40

    print '{} Business Days from {} is {}'.format(add_days, from_date, AddBusinessDays(from_date, add_days))
    print '{} Calendar Days from {} is {}'.format(add_days, from_date, AddCalendarDays(from_date, add_days))

