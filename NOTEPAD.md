### Cog with infinite loop that executes every x seconds (template)

```python

import discord
import httpx
import json
from discord.ext import commands, tasks

from apikeys import SERVER_ID, CHANNEL_ID


async def setup(client):
    await client.add_cog(TimeNotifications(client), guild=discord.Object(id=SERVER_ID))


class TimeNotifications(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.sendNews.start()

    @tasks.loop(seconds=10)
    async def sendNews(self):
        channel = self.client.get_channel(CHANNEL_ID)
        await channel.send("This message is sent every 10 seconds.")

    @sendNews.before_loop
    async def before_sendNews(self):
        await self.client.wait_until_ready()

```
