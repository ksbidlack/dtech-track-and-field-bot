"This document is only for testing purposes"

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
    print(f"Client is connected to guild {guild.name}(id: {guild.id})")


    # announce events
    async def check_calendar():
        
        schedule_channel = client.get_channel(id=settings.SCHEDULE_CHANNEL_ID)

        calendar = calendar_management.google_calendar.get_calendar()
        events = calendar_management.google_calendar.get_events(calendar)
        message = calendar_management.google_calendar.parse_message(events)
        
        print("Announcing!")
        await schedule_channel.send(message)
        
        del schedule_channel
        del calendar
        del events
        del message


    
    await check_calendar()


if __name__ == "__main__":
    client.run(settings.DISCORD_TOKEN)
