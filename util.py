from datetime import datetime, timezone, timedelta
from dateutil import tz
from dotenv import load_dotenv
import pypco
from pypco import PCOCredentialsException, PCORequestException
import os
import sys


def get_local_time(utc_dt):
    """Takes a UTC timestamp from API and returns a local time timestamp in the form of 10:00 AM"""
    tz_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return tz_dt.strftime("%I:%M %p")


def get_utc_dt(event_time):
    """Takes a UTC time from API and returns a datetime object"""
    return datetime.strptime(event_time['data']['attributes']['starts_at'],
                               '%Y-%m-%dT%H:%M:%SZ')  # 2021-04-04T04:00:00Z


def get_mondays():
    """Returns a tuple with start and end Time Stamp Strings from last monday to midnight this monday.
    Unless it is a monday. In that case we actually want the previous period."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if today.weekday() < 6:
        # Lookup last week (Two monday's ago)
        monday = today - timedelta(days=today.weekday()) - timedelta(weeks=1)
        pass
    else:
        # lookup this week (The Last monday to the current Sunday - today)
        monday = today - timedelta(days=today.weekday())

        pass
    next_monday = monday + timedelta(weeks=1)
    monday = monday.astimezone(tz.tzutc())
    next_monday = next_monday.astimezone(tz.tzutc())

    return monday, next_monday


def get_sunday():
    """Returns the last sunday or today if it is sunday"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if today.weekday() < 6:
        sunday = today - timedelta(days=today.weekday()+1)
        return sunday
    elif today.weekday() == 6:
        return today
    # else:
    #     sunday = today -timedelta(days=today.weekday()+1) - timedelta(weeks=1)
    #     return sunday


def get_pco():
    try:
        load_dotenv('config.env')  # take environment variables from config.env
    except Exception as e:
        print(e)

    try:
        pco = pypco.PCO(os.getenv('APPLICATION_ID'), os.getenv('SECRET'))
        test = pco.get('https://api.planningcenteronline.com/people/v2/me')
        return pco

    except PCORequestException:
        print("ERROR - Could not authenticate using Planning Center API Keys in config.env")
        sys.exit(0)

    # except PCOCredentialsException:
    #     print("Nope")
    #     sys.exit(0)


def test_config():
    print("Checking Config File")
    try:
        load_dotenv('config.env')  # take environment variables from config.env

        if os.getenv('APPLICATION_ID') is None:
            print("Application_ID not found in config.env")
        if os.getenv('SECRET') is None:
            print("SECRET not found in config.env")

        if os.getenv('LIST_CATEGORY') is None:
            print("LIST_CATEGORY not found in config.env")

        if os.getenv('FUNDS') is None:
            print("Application_ID not found in config.env")

        if os.getenv('HEAD_COUNT_EVENTS') is None:
            print("Application_ID not found in config.env")
        get_pco()

    except Exception as e:
        # print(type(e))
        sys.exit(0)


if __name__ == '__main__':
    print(get_sunday())