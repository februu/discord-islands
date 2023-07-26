from PIL import Image
import random
import time

from settings import TILE_WIDTH, TILE_HEIGHT, ISO_TILE_HEIGHT, BLOCKS

# Example island object.
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

sprites = Image.open("assets/tinyBlocks.png")
bg = Image.open("assets/bg.png")

# Populates with blocks.
for i in range(20):
    y = random.randint(0, len(island['map']) - 1)
    x = random.randint(0, len(island['map'][0]) - 1)
    z = random.randint(0, len(island['map'][0][0]) - 1)
    while not island['map'][y][z][x] == -1 or y > 0:
        if island['map'][y-1][z][x] != -1:
            break
        y = random.randint(0, len(island['map']) - 1)
        x = random.randint(0, len(island['map'][0]) - 1)
        z = random.randint(0, len(island['map'][0][0]) - 1)
    island['map'][y][z][x] = random.choice(list(BLOCKS.values()))

#  Gets timestamp in seconds.
#  print(int(time.time()))

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
bg.save("image.png", "PNG")
