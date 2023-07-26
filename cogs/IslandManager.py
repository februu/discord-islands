import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from PIL import Image
import random
import time
import os

from apikeys import SERVER_ID, CHANNEL_ID
from settings import TILE_WIDTH, TILE_HEIGHT, ISO_TILE_HEIGHT, BLOCKS

sprites = Image.open("assets/tinyBlocks.png")


async def setup(client):
    await client.add_cog(IslandManager(client), guild=discord.Object(id=SERVER_ID))


class IslandManager(commands.Cog):
    def __init__(self, client):
        self.client = client

    # -----------------------------------------
    #               Commands
    # -----------------------------------------

    # /island
    # - sends picture of your island and info about collected resources.
    @ app_commands.command(name="island", description="Collect resources from your island!")
    async def islandCommand(self, interaction: discord.Interaction):

        if not interaction.channel.id == CHANNEL_ID:
            await interaction.response.send_message(f"❌ You can only use that command in <#{CHANNEL_ID}>", ephemeral=True)
            return

        await interaction.response.defer()
        await self.generateIslandImage(interaction.user.id)
        if (os.path.exists(f"{interaction.user.id}.png")):
            await interaction.followup.send(file=discord.File(f"{interaction.user.id}.png"))
            os.remove(f"{interaction.user.id}.png")
        else:
            await interaction.followup.send("Error! Please contact the admin.")

    # /upgrade
    # - allows you to upgrade your island.
    # @arg1 - upgrade that user want to buy.
    @ app_commands.command(name="upgrade", description="Upgrade your island!")
    async def upgradeCommand(self, interaction: discord.Interaction, arg1: str):

        if not interaction.channel.id == CHANNEL_ID:
            await interaction.response.send_message(f"❌ You can only use that command in <#{CHANNEL_ID}>", ephemeral=True)
            return

        await interaction.response.defer()

        # TODO: Database request and logic here.

        await interaction.followup.send("Upgraded!")

    # /craft
    # - allows you to craft items.
    # @arg1 - item that user want to craft.
    @ app_commands.command(name="craft", description="Craft items using your resources!")
    async def craftCommand(self, interaction: discord.Interaction, arg1: str):

        if not interaction.channel.id == CHANNEL_ID:
            await interaction.response.send_message(f"❌ You can only use that command in <#{CHANNEL_ID}>", ephemeral=True)
            return

        await interaction.response.defer()

        # TODO: Database request and logic here.

        await interaction.followup.send("Started crafting!")

    # /sell
    # - allows you to sell items.
    # @arg1 - items that user want to sell. If 'all', sell all of them.
    @ app_commands.command(name="sell", description="Sell resources for money!")
    async def sellCommand(self, interaction: discord.Interaction, arg1: str):

        if not interaction.channel.id == CHANNEL_ID:
            await interaction.response.send_message(f"❌ You can only use that command in <#{CHANNEL_ID}>", ephemeral=True)
            return

        await interaction.response.defer()

        # TODO: Database request and logic here.

        await interaction.followup.send("Sold!")

    # -----------------------------------------
    #               Functions
    # -----------------------------------------

    # generateIslandImage(userId)
    # @userId - discord user ID
    # Generates picture of user's island and saves it as <userid>.png

    async def generateIslandImage(self, userId):
        bg = Image.open("assets/bg.png")

        # Gets user island from database.
        # FIXME
        island = {'id': 175652881456693249,
                  'lastCollectedTimestamp': 1690361813,
                  'balance': 0,
                  'map': [[[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
                          [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]], [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]],
                  'upgrades': {'size': 4,
                               'blockGeneration': 1,
                               'higherValue': 2,
                               'quickerGeneration': 3,
                               'moreResources': 3,
                               'quickerCrafting': 3},
                  'items': [{'id': 0,
                             'amount': 1}]}

        # Draws the base.
        for z in range(0, len(island['map'][0])):
            for x in range(0, len(island['map'][0][0])):
                row, column = divmod(random.choice([9, 9, 9, 10, 11]), 9)
                tile = sprites.crop((TILE_WIDTH * column, TILE_HEIGHT * row,
                                    TILE_WIDTH * (column + 1), TILE_HEIGHT * (row + 1)))
                tileX = (x - z) * (TILE_WIDTH / 2)
                tileY = (x + z) * (ISO_TILE_HEIGHT / 2)
                # tileY -= y * (ISO_TILE_HEIGHT + 1)
                bg.paste(tile, (int(tileX) + 56, int(tileY) +
                                72-len(island['map'])*4), mask=tile)

        # Draws blocks.
        for y in range(0,  len(island['map'])):
            for z in range(0,  len(island['map'][0])):
                for x in range(0,  len(island['map'][0][0])):

                    if not island['map'][y][z][x] == -1:
                        row, column = divmod(island['map'][y][z][x], 9)
                        tile = sprites.crop((TILE_WIDTH * column, TILE_HEIGHT * row,
                                            TILE_WIDTH * (column + 1), TILE_HEIGHT * (row + 1)))

                        tileX = (x - z) * (TILE_WIDTH / 2)
                        tileY = (x + z) * (ISO_TILE_HEIGHT / 2)
                        tileY -= (y + 1) * (ISO_TILE_HEIGHT + 1)
                        bg.paste(tile, (int(tileX) + 56, int(tileY) +
                                        72-len(island['map'])*4), mask=tile)

        bg = bg.resize((128*4, 128*4), resample=Image.Resampling.NEAREST)
        bg.save(f"{userId}.png", "PNG")
