import datetime
import asyncio

import discord
from discord.ext import tasks

import settings
import calendar_management.google_calendar

client = discord.Client()


# the main event loop
@client.event
async def on_ready():
    # determine guild and print when connection succeeds
    for guild in client.guilds:
        if guild.name == settings.DISCORD_GUILD:
            break

    print(f"{client.user} has connected to Discord!")
    print(f"Client is connected to guild {guild.name}(id: {guild.id})\n")

    # calendar loop, announces events every day
    async def check_calendar(TESTING):
        if not TESTING:
            delta = calendar_management.google_calendar.get_delta()

            print(f"Next announcement in {round(delta)} seconds!\n")
            await asyncio.sleep(delta)
            
            schedule_channel = client.get_channel(id=settings.SCHEDULE_CHANNEL_ID)

            calendar = calendar_management.google_calendar.get_calendar()
            events = calendar_management.google_calendar.get_events(calendar, datetime.datetime.now())
            message = calendar_management.google_calendar.parse_message(events)
            
            print(f"Announcing! Message:\n{message}\n")
            await schedule_channel.send(message)
            
            del schedule_channel
            del calendar
            del events
            del message

            await check_calendar(True)
        else:
            schedule_channel = client.get_channel(id=settings.SCHEDULE_CHANNEL_ID)

            calendar = calendar_management.google_calendar.get_calendar()
            events = calendar_management.google_calendar.get_events(calendar, datetime.datetime.strptime(str(datetime.datetime.now().date()), "%Y-%m-%d").date() - datetime.timedelta(days=2))
            message = calendar_management.google_calendar.parse_message(events)
            
            print(f"Announcing! Message:\n{message}\n")
            await schedule_channel.send(message)
            
            del schedule_channel
            del calendar
            del events
            del message
    
    await check_calendar(settings.TESTING)


if __name__ == "__main__":
    client.run(settings.DISCORD_TOKEN)
