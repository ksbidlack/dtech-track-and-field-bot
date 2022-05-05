import sys
import pickle
import datetime
import calendar
import dateutil

from apiclient.discovery import build

import settings


def find_weekday(date):
    day = datetime.datetime.strptime(str(date), "%Y-%m-%d").weekday()
    return calendar.day_name[day]


def get_calendar():
    """Retrives the calendar from the google calendar API"""
    credentials = pickle.load(open(settings.PATH_TO_TOKEN, "rb"))
    service = build("calendar", "v3", credentials=credentials)
    result = service.calendarList().list().execute()

    calendar_id = result["items"][6]["id"]
    result = service.events().list(calendarId=calendar_id).execute()

    return result


def get_events(calendar, date):
    """Retrieves events from date"""
    events = []

    for event in calendar["items"]:
        if event["status"] != "cancelled":
            if str(event["start"]["dateTime"])[0:10] == str(date)[0:10]:
                events.append(event)

    return events


def parse_message(events):
    """Creates a message for all the events on the current day"""
    if not events:
        message = f'<@&970492351711703120> You have no events today!'
    elif len(events) == 1:
        for event in events:
            time = str(event["start"]["dateTime"])[-14:-9]
            twelve_hour_time = datetime.datetime.strptime(time, "%H:%M")
            twelve_hour_time = twelve_hour_time.strftime("%I:%M %p")

            message = f'<@&970492351711703120> You have **{event["summary"]}** today!\n'
            message += f'**Location:** {event["location"]}\n'
            message += f'**Time:** {str(twelve_hour_time)}\n'
    else:
        message = f"<@&970492351711703120> You have **{len(events)} events** today! Here's an overview:\n"
        for index, event in enumerate(events):
            time = str(event["start"]["dateTime"])[-14:-9]
            twelve_hour_time = (time, "%H:%M")
            twelve_hour_time = twelve_hour_time.strftime("%I:%M %p")

            message += f'\nEvent #{index + 1}: **{event["summary"]}**\n'
            message += f'**Location:** {event["location"]}\n'
            message += f'**Time:** {str(twelve_hour_time)}\n'
    
    if find_weekday(datetime.datetime.now()) == "Monday":
        five_days_from_today = str(datetime.datetime.strptime(str(datetime.datetime.now().date()), "%Y-%m-%d").date() + datetime.timedelta(days=5))

        calendar = get_calendar()
        for event in get_events(calendar, five_days_from_today):
            if "CCS" or "PSAL" in event["summary"]:
                message += f"\n**Reminder! There is a meet on Saturday: {event['summary']}**"
    return message
    

def get_delta():
    now = datetime.datetime.now()
    
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    
    tomorrow_6am = now.replace(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=6, minute=0, second=0, microsecond=0)

    delta = tomorrow_6am - now
    
    return delta.total_seconds()
