"""Functions related to the google calendar"""

import os
import pickle
import datetime
import dateutil.parser

import pause

from apiclient.discovery import build


def get_calendar():
    PATH_TO_PKL = os.environ["PATH_TO_PKL"]

    credentials = pickle.load(open(PATH_TO_PKL, "rb"))
    service = build("calendar", "v3", credentials=credentials)
    result = service.calendarList().list().execute()

    calendar_id = result["items"][6]["id"]
    result = service.events().list(calendarId=calendar_id).execute()

    return result


def get_events(calendar):
    events = []

    for event in calendar["items"]:
        if event["status"] != "cancelled":
            if str(event["start"]["dateTime"])[0:10] == str(datetime.datetime.now())[0:10]:
                events.append(event)

    return events


def parse_message(events):
    if events == []:
        message = f"""<@&970492351711703120> You have no events today!"""
    else:
        message = f"""<@&970492351711703120> You have {len(events)} event(s) today! Here's an overview:\n"""
        for index, event in enumerate(events):
            message += f'Event #{index + 1}: {event["summary"]}, Location: {event["location"]}, Time: {str(event["start"]["dateTime"])[-14:-6]}\n'
    
    return message
    

def get_delta():
    now = datetime.datetime.now()
    
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    
    tomorrow_6am = now.replace(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=6, minute=0, second=0, microsecond=0)

    delta = tomorrow_6am - now
    
    return delta.total_seconds()
