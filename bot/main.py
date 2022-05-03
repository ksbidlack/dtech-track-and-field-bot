import os
import datetime
import asyncio

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


    # Functions
    async def check_calendar():
        delta = calendar_management.google_calendar.get_delta()

        calendar = calendar_management.google_calendar.get_calendar()
        events = calendar_management.google_calendar.get_events(calendar)
        message = calendar_management.google_calendar.parse_message(events)

        await asyncio.sleep(delta)

        schedule_channel = client.get_channel(id=957412669940441139)
        
        print("Announcing")
        await schedule_channel.send(message)


    print(f"Next announcement in {calendar_management.google_calendar.get_delta()} seconds")
    print("Calendar started")

    await check_calendar()


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)