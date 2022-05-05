import sys
import pickle
import datetime
import calendar
import dateutil
import asyncio

from apiclient.discovery import build

import settings


def find_day(date_time):
    return calendar.day_name[date_time.weekday()]

def get_delta(date_time):
    now = datetime.datetime.now()
    delta = date_time - now
    return delta


def get_events(date_time):
    """Retrieves events from date, where date is a datetime object."""
    events = []
    date = date_time.date()

    # get the calendar credentials
    credentials = pickle.load(open(settings.PATH_TO_TOKEN, "rb"))
    service = build("calendar", "v3", credentials=credentials)
    result = service.calendarList().list().execute()

    calendar_id = result["items"][6]["id"]
    calendar = service.events().list(calendarId=calendar_id).execute()


    for event in calendar["items"]:
        if event["status"] != "cancelled":
            event_date = str(event["start"]["dateTime"])[0:10]
            if event_date == str(date):
                events.append(event)

    return events


def parse_message(events, date_time):
    message = ""

    if len(events) == 1:
        for event in events:
            event_time = str(event["start"]["dateTime"])[-14:-9]
            twelve_hour_time = datetime.datetime.strptime(event_time, "%H:%M").strftime("%I:%M %p")

            message += f'<@&970492351711703120> You have **{event["summary"]}** today!\n'
            message += f'**Location:** {event["location"]}\n'
            message += f'**Time:** {str(twelve_hour_time)}\n'
    elif len(events) > 1:
        message += f"<@&970492351711703120> You have **{len(events)} events** today! Here's an overview:\n"
        for index, event in enumerate(events):
            event_time = str(event["start"]["dateTime"])[-14:-9]
            twelve_hour_time = datetime.datetime.strptime(event_time, "%H:%M").strftime("%I:%M %p")

            message += f'\nEvent #{index + 1}: **{event["summary"]}**\n'
            message += f'**Location:** {event["location"]}\n'
            message += f'**Time:** {str(twelve_hour_time)}\n'
    elif not events:
        message += f'<@&970492351711703120> You have no events today!'
    else:
        print("The system encountered an error")

    if find_day(date_time) == "Monday":
        five_days_from_today = datetime.datetime.strptime(str(date_time.date()), "%Y-%m-%d") + datetime.timedelta(days=5)
        for event in get_events(five_days_from_today):
            if "CCS" or "PSAL" in event["summary"]:
                message += f"\n**Reminder! There is a meet on Saturday: {event['summary']}**"

    return message


async def announce_calendar(channel, announce_time):
        delta_in_seconds = get_delta(announce_time).total_seconds()
        
        print(f"Next announcement in {round(delta_in_seconds)} seconds!\n")
        await asyncio.sleep(delta_in_seconds)
        
        events = get_events(announce_time)
        message = parse_message(events, announce_time)
        
        print(f"Announcing! Message:\n{message}\n")
        await channel.send(message)

        now = datetime.datetime.now()
        tomorrow_at_6am = now.replace(hour=6, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        await announce_calendar(channel, tomorrow_at_6am)