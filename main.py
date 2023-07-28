import os
from discord.ext import commands
import discord
import asyncio

from apikeys import DISCORD_TOKEN, SERVER_ID

intents = discord.Intents().all()
client = commands.Bot("/", activity=discord.Activity(
    type=discord.ActivityType.playing, name="/village 🌳"), intents=intents)


@client.event
async def on_ready():
    print(f"> Connected to {client.user.name} (#{client.user.id}).")


@client.event
async def setup_hook():
    for filepath in os.listdir("cogs/"):
        if filepath.endswith(".py"):
            print(f"> Found {filepath} cog file. Loading...")
            filename = filepath[:-3]
            await client.load_extension(f"cogs.{filename}")
            print(f"> {filename} cog sucessfully loaded.")
    synced = await client.tree.sync(guild=discord.Object(id=SERVER_ID))
    print(f"> Synced {len(synced)} commands (server #{SERVER_ID}).")


async def main():
    async with client:
        await client.start(DISCORD_TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
