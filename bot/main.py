import datetime
import asyncio

import discord
from discord.ext import tasks

import settings
import calendar_management.google_calendar

client = discord.Client()


@client.event
async def on_ready():
    # determine guild and print when connection succeeds
    for guild in client.guilds:
        if guild.name == settings.DISCORD_GUILD:
            break

    print(f"{client.user} has connected to Discord!")
    print(f"Client is connected to guild {guild.name}(id: {guild.id})")
    if settings.TESTING:
        schedule_channel = client.get_channel(id=settings.SCHEDULE_CHANNEL_ID)
        # this date will vary, depending on what is being tested
        await calendar_management.google_calendar.announce_calendar(
            channel=schedule_channel, 
            announce_time=datetime.datetime.now(), 
            test_time=datetime.datetime.now() - datetime.timedelta(days=1)
            )
    else:
        schedule_channel = client.get_channel(id=settings.SCHEDULE_CHANNEL_ID)
        now = datetime.datetime.now()
        tomorrow_at_6am = now.replace(hour=6, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        await calendar_management.google_calendar.announce_calendar(
            channel=schedule_channel, 
            announce_time=tomorrow_at_6am)
        

if __name__ == "__main__":
    client.run(settings.DISCORD_TOKEN)
