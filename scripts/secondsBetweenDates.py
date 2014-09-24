#!/usr/bin/env Python

''' Calculate the the seconds between two dates.  The default start date is January 1, 1990.  This is to validate the CSI calulation SecsSince1990'''
import argparse
import datetime

def calculateSecs():
    old_date = datetime.datetime(1990, 1, 1, 0, 0, 0)

    mfg_date = datetime.datetime(2014, 9, 18, 0, 0, 0)

    date_delta = mfg_date - old_date
    cur_date = datetime.datetime.today()

    # date_delta is a "datetime.timedelta" object
    # "date_delta.days" gives an integer number of days

    print("Seconds Between 1990 and Mfg Date = %s" % (date_delta.days * 86400))

    date_delta = cur_date - old_date
    print("Seconds Between  1990 and Current Date = %s" % (date_delta.days * 86400))

    date_delta = cur_date - mfg_date
    print("Seconds Between  Mfg Date and Current Date = %s" % (date_delta.days * 86400))


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('start_date')
    # parser.add_argument('end_date')
    # args = parser.parse_args()

    # calculateSecs(args.start_date, args.end_date)
    calculateSecs()