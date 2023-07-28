import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from PIL import Image
import random
import time
import os
from pymongo import MongoClient

from apikeys import SERVER_ID, CHANNEL_ID, MONGODB_CONNECTION_STRING
from settings import TILE_WIDTH, TILE_HEIGHT, ISO_TILE_HEIGHT, BLOCKS

sprites = Image.open("assets/tinyBlocks.png")


async def setup(client):
    await client.add_cog(IslandManager(client), guild=discord.Object(id=SERVER_ID))


class IslandManager(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("> Attempting connection to MongoDB...")
        try:
            cluster = MongoClient(MONGODB_CONNECTION_STRING)
            self.db = cluster['islands']['islands']
            print("> Connected successfully.")
        except:
            print("> Connection failed.")

    # -----------------------------------------
    #               Commands
    # -----------------------------------------

    # /island
    # - sends picture of your island, info about collected resources and button menu.

    @ app_commands.command(name="island", description="Collect resources from your island!")
    async def islandCommand(self, interaction: discord.Interaction):

        if not interaction.channel.id == CHANNEL_ID:
            await interaction.response.send_message(f"❌ You can only use that command in <#{CHANNEL_ID}>", ephemeral=True)
            return

        await interaction.response.defer()
        await self.generateIslandImage(interaction.user.id)
        if (os.path.exists(f"{interaction.user.id}.png")):
            await interaction.followup.send(file=discord.File(f"{interaction.user.id}.png"), view=IslandView())
            os.remove(f"{interaction.user.id}.png")
        else:
            await interaction.followup.send("Error! Please contact the admin.")

    # -----------------------------------------
    #               Functions
    # -----------------------------------------

    # generateIslandImage(userId)
    # @userId - discord user ID
    # Generates picture of user's island and saves it as <userid>.png

    async def generateIslandImage(self, userId):

        try:
            # Gets user island from database.
            island = self.db.find_one({"id": int(userId)})
            if island == None:
                print(f"> User #{userId} does not have an island.")
                await self.createNewIsland(userId)
                island = self.db.find_one({"id": int(userId)})

            # Draws the base.
            bg = Image.open("assets/bg.png")

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

        except:
            return

    # createNewIsland(userId)
    # @userId - discord user ID
    # Creates new island in database
    async def createNewIsland(self, userId):
        island = {'id': userId,
                  'lastCollectedTimestamp': int(time.time()),
                  'balance': 0,
                  'map': [[[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]],
                          [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]], [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]],
                  'upgrades': {'size': 1,
                               'blockGeneration': 1,
                               'higherValue': 1,
                               'quickerGeneration': 1,
                               'moreResources': 1,
                               'quickerCrafting': 1},
                  'items': []}
        self.db.insert_one(island)
        print(f"> New island created for user #{userId}")


# -----------------------------------------
#               Views
# -----------------------------------------

class IslandView(discord.ui.View):
    def __init__(self):
        super().__init__()

    # collectResourcesButton
    @discord.ui.button(label="Collect Resources", style=discord.ButtonStyle.green)
    async def collectResourcesButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.collectResources(interaction.user.id)
        await interaction.followup.send("Collected!", ephemeral=True)

    # upgradeButton
    @discord.ui.button(label="Upgrade Island", style=discord.ButtonStyle.blurple)
    async def upgradeButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.collectResources(interaction.user.id)
        await interaction.followup.send("Upgraded!", ephemeral=True)

    # craftButton
    @discord.ui.button(label="Craft", style=discord.ButtonStyle.blurple)
    async def craftButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.collectResources(interaction.user.id)
        await interaction.followup.send("Crafted!", ephemeral=True)

    # sellAllButton
    @discord.ui.button(label="Sell All", style=discord.ButtonStyle.red)
    async def sellAllButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.collectResources(interaction.user.id)
        await interaction.followup.send("Sold All!", ephemeral=True)

    # -----------------------------------------
    #               Functions
    # -----------------------------------------

    # collectResources(userId)
    # @userId - discord user ID
    # Collects reosurces from the island and puts the changes into the database.
    async def collectResources(self, userId):
        pass
