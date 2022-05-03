import datetime
import asyncio

import discord
from discord.ext import tasks

import settings
import calendar_management.google_calendar

# Discord initialization
client = discord.Client()


@client.event
async def on_ready():
    # determine guild and print when connection succeeds
    for guild in client.guilds:
        if guild.name == settings.DISCORD_GUILD:
            break


    print(f"{client.user} has connected to Discord!")
    print(f"Client is connected to guild {guild.name}(id: {guild.id})")


    async def check_calendar():
        delta = calendar_management.google_calendar.get_delta()

        print(f"Next announcement in {round(delta)} seconds!")
        await asyncio.sleep(delta)
        
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

    # start the calendar loop
    await check_calendar()


if __name__ == "__main__":
<<<<<<< HEAD
    client.run(settings.DISCORD_TOKEN)
=======
    client.run(DISCORD_TOKEN)
>>>>>>> 2ab0ad1dcec4f56b5b6067ea7335d08ea74cee04
