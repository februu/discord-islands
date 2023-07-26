import discord
from discord.ext import commands
from discord import app_commands
import asyncio

from apikeys import SERVER_ID, CHANNEL_ID


async def setup(client):
    await client.add_cog(IslandManager(client), guild=discord.Object(id=SERVER_ID))


class IslandManager(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Functions

    async def sendHelpMessage(self, interaction: discord.Interaction):
        embed = discord.Embed("Help")
        interaction.response.send_message(embed=embed)
        pass

    # Main Command

    @ app_commands.command(name="island", description="Manage your island!")
    @ app_commands.rename(arg1="1", arg2="2")
    @ app_commands.describe(arg1='First argument', arg2='Second argument')
    async def islandCommand(self, interaction: discord.Interaction, arg1: str, arg2: str):

        if not interaction.channel.id == CHANNEL_ID:
            await interaction.response.send_message(f"❌ You can only use that command in <#{CHANNEL_ID}>", ephemeral=True)
            return

        arg1 = arg1.lower()
        arg2 = arg2.lower()

        if arg1 == "":
            # Send village picture.
            pass
        elif arg1 == "help":
            # Send help message.
            self.sendHelpMessage(self, interaction)
        elif not arg2 == "":
            if arg1 == "build":
                # Build.
                pass
            elif arg1 == "upgrade":
                # Upgrade.
                pass
            elif arg1 == "visit":
                #  Visit
                pass
            else:
                # Send help message
                self.sendHelpMessage(self, interaction)
        else:
            # Send help message.
            self.sendHelpMessage(self, interaction)


class Village:
    def __init__(self, userID):
        pass
