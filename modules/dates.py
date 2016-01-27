#!/usr/bin/env python
#
#
#
"""
This module program performs common functions with dates
"""

# ---------------------------------------------------------------------------
from datetime import timedelta, date

__version__ = '1.0.0'


def days_add(beginning_date, days_to_add, business=False):
    """
    Determine what the date will be in a certain number of days

    :param beginning_date: date to start counting from (YYYY-MM-DD)
    :type beginning_date: str
    :param days_to_add: number of days to go forward
    :type days_to_add: int
    :param business: should only business days be counted (M-F are considered business days)
    :return:
    """
    counter_days = days_to_add
    new_date = beginning_date.split('-')
    new_date = date(int(new_date[0]), int(new_date[1]), int(new_date[2]))

    while counter_days > 0:

        # add a day to the date
        new_date += timedelta(days=1)

        # check if current date is a week day (saturday = 5, sunday = 6)
        # if the date is the weekend, then don't count the day as added
        if business:
            if new_date.weekday() < 5:
                counter_days -= 1
        else:
            counter_days -= 1

    return str(new_date)


def days_sub(beginning_date, days_to_sub, business=False):
    """
    Determine what the date was a certain number of days ago

    :param beginning_date: date to start counting from (YYYY-MM-DD)
    :type beginning_date: str
    :param days_to_sub: number of days to go back
    :type days_to_sub: int
    :param business: should only business days be counted (M-F are considered business days)
    :return:
    """
    counter_days = days_to_sub
    new_date = beginning_date.split('-')
    new_date = date(int(new_date[0]), int(new_date[1]), int(new_date[2]))

    while counter_days > 0:

        # add a day to the date
        new_date -= timedelta(days=1)

        # check if current date is a week day (saturday = 5, sunday = 6)
        # if the date is the weekend, then don't count the day as added
        if business:
            if new_date.weekday() < 5:
                counter_days -= 1
        else:
            counter_days -= 1

    return str(new_date)


def days_delta(beginning_date, ending_date, business=False):
    """
    Determines the number of days between two dates

    :param beginning_date: starting date (YYYY-MM-DD)
    :type beginning_date: str
    :param ending_date: ending date (YYYY-MM-DD)
    :type ending_date: str
    :param business: count only business days
    :return:
    """

    start_date = beginning_date.split('-')
    stop_date = ending_date.split('-')

    start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    stop_date = date(int(stop_date[0]), int(stop_date[1]), int(stop_date[2]))

    if business:
        delta_days = 0

        if start_date > stop_date:
            start_date = stop_date

            stop_date = beginning_date.split('-')
            stop_date = date(int(stop_date[0]), int(stop_date[1]), int(stop_date[2]))

        while stop_date != start_date:
            start_date += timedelta(days=1)

            if start_date.weekday() < 5:
                delta_days += 1

        return delta_days
    else:
        delta_days = abs(start_date - stop_date)
        return int(delta_days.days)


# ---------------------------------------------------------------------------
if __name__ == '__main__':

    from_date = '2015-01-25'
    add_days = 40

    print '{} Business Days ahead of {} is {}'.format(add_days, from_date, days_add(from_date, add_days, business=True))
    print '{} Calendar Days ahead of {} is {}'.format(add_days, from_date, days_add(from_date, add_days))
    print '{} Calendar Days behind {} is {}'.format(add_days, from_date, days_sub(from_date, add_days))

    print 'The number of Calendar days between {} and {} is {}'.format(
            from_date,
            days_add(from_date, add_days),
            days_delta(from_date, days_add(from_date, add_days))
    )
    print 'The number of Calendar days between {} and {} is {}'.format(
            from_date,
            days_sub(from_date, add_days),
            days_delta(from_date, days_sub(from_date, add_days))
    )
    print 'The number of Business days between {} and {} is {}'.format(
            from_date,
            days_add(from_date, add_days),
            days_delta(from_date, days_add(from_date, add_days), business=True)
    )

