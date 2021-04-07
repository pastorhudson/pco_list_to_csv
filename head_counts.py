import pypco
from dotenv import load_dotenv
import os
from datetime import datetime, timezone


load_dotenv('api_secret.env')  # take environment variables from api_secret.env
pco = pypco.PCO(os.getenv('APPLICATION_ID'), os.getenv('SECRET'))


def get_local_time(utc_dt):
    """Takes a UTC timestamp from API and returns a local time timestamp in the form of 10:00 AM"""
    tz_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return tz_dt.strftime("%I:%M %p")


def get_event_time_name(event_time):
    return event_time['data']['attributes']['name']  # event time readable name


def get_event_time_id(headcount):
    return headcount['data']['relationships']['event_time']['data']['id']  # event time id


def get_event_id(event_name):
    """Takes an event name and returns an event_id"""
    event_id = 0
    events = pco.iterate('https://api.planningcenteronline.com/check-ins/v2/events?order=-created_at')
    for event in events:

        if event['data']['attributes']['name'] == event_name:
            event_id = event['data']['id']
    return event_id


def get_attendance_type_id(event_id, attendance_type):
    """Takes an event_id and attendance_type name also displayed as custom headcounts
    and returns an attendance_type id"""

    attendance_types = pco.iterate(f'https://api.planningcenteronline.com/check-ins/v2/events/'
                                   f'{event_id}/attendance_types')
    for a_type in attendance_types:
        if a_type['data']['attributes']['name'] == attendance_type:
            return a_type['data']['id']

    return None


def get_headcounts(event_id, attendance_type_id):
    """Takes event_id, and attendance type, and returns a list of tuples of (time,headcount) that match that event."""

    headcounts = pco.iterate(f'https://api.planningcenteronline.com/check-ins/v2/events/{event_id}/'
                             f'attendance_types/{attendance_type_id}/headcounts?order=-created_at&include=event_time')

    headcount_data = []
    initial_date = ""
    for headcount in headcounts:

        if headcount['data']['relationships']['attendance_type']['data']['id'] == attendance_type_id:
            count = headcount['data']['attributes']['total']  # headcount of event and attendance_type
            date = headcount['data']['attributes']['created_at']  # date of event
            event_time = pco.get("https://api.planningcenteronline.com/check-ins/v2/event_times/"
                                 f"{headcount['data']['relationships']['event_time']['data']['id']}")

            utc_dt = datetime.strptime(event_time['data']['attributes']['starts_at'], '%Y-%m-%dT%H:%M:%SZ')  # 2021-04-04T04:00:00Z
            event_time_name = get_local_time(utc_dt)
            count_tup = (event_time_name, count)

            if date[0:11] == initial_date[0:11] or initial_date == "":
                headcount_data.append(count_tup)
                initial_date = date
            else:
                break
    return headcount_data


def parse_headcount_events():
    """Parses the HEAD_COUNT_EVENTS string from the secrets.env and
    returns a list of tuples of event_id, attendence_type prepared for get_headcounts"""
    headcount_events = {}
    for headcount in os.environ.get("HEAD_COUNT_EVENTS").strip(" ").split(','):
        event_id = get_event_id(headcount.split(':')[0])
        attendance_type_id = get_attendance_type_id(event_id, headcount.split(':')[1])
        headcount_events[f"{headcount.split(':')[0]} - {headcount.split(':')[1]}"] = (event_id, attendance_type_id)

    return headcount_events


def get_headcount_data():
    headcount_data = {}
    for event_name, event in parse_headcount_events().items():
        headcount_data[event_name] = get_headcounts(event[0], event[1])

    return headcount_data


if __name__ == '__main__':
    print(get_headcount_data())
