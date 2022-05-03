import os
import datetime

import pause
import discord
from discord.ext import tasks

import calendar_management.google_calendar

# Load environment variables
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GUILD = os.environ["DISCORD_GUILD"]

# Discord initialization
client = discord.Client()

@client.event
async def on_ready():
    # determine guild and print when connection succeeds
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f"{client.user} has connected to Discord!")
    print(f"Client is connected to guild {guild.name}(id: {guild.id})")

    check_calendar.start()


@tasks.loop(seconds=86400)
async def check_calendar():
    calendar = calendar_management.google_calendar.get_calendar()
    events = calendar_management.google_calendar.get_events(calendar)
    message = calendar_management.google_calendar.parse_message(events)

    print("Announcing")
    schedule_channel = client.get_channel(id=957412669940441139)
    schedule_channel.send(message)


@check_calendar.before_loop
async def startup():
    if datetime.datetime.now().hour < 6:
        print("It's before 6am, task loop will start at 6am")

        today_6am = datetime.datetime.now().replace(hour=6)
        pause.until(today_6am)
    else:
        print("It's after 6am, task loop will start tomorrow.")
        
        tomorrow_6am = calendar_management.google_calendar.get_tomorrow_6am()
        pause.until(tomorrow_6am)


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)