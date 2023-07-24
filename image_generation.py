from PIL import Image


MAP_X = 7
MAP_Y = 5
MAP_Z = 7
TILE_WIDTH = 16
TILE_HEIGHT = 18
ISO_TILE_HEIGHT = 8

sprites = Image.open("assets/tinyBlocks.png")
bg = Image.open("assets/bg.png")

map = [[[1, 9, 1, 10, 2, 9, 10], [9, 2, 9, 1, 3, 9, 9], [1, 8, 9, 2, 58, 56, 9], [1, 1, 2, 1, 56, 5, 4], [7, 6, 9, 9, 4, 22, 22], [6, 7, 9, 5, 22, 22, 22], [6, 6, 9, 4, 22, 22, 22]],
       [[-1, -1, -1, -1, 41, 41, -1], [-1, 30, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -
                                                                                                   1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1]],
       [[-1, -1, -1, -1, -1, -1, -1], [-1, 30, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -
                                                                                                   1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1]],
       [[-1, 36, -1, -1, -1, -1, -1], [36, 30, 36, -1, -1, -1, -1], [-1, 36, -1, -1, -1, -1, -1], [-1, -1, -1, -
                                                                                                   1,  -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1]],
       [[-1, -1, -1, -1, -1, -1, -1], [-1, 36, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -
                                                                                                   1,  -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1]],
       ]


def changeSeason(season):
    global map
    for y in range(0, MAP_Y):
        for z in range(0, MAP_Z):
            for x in range(0, MAP_X):
                if map[y][z][x] == 36:
                    map[y][z][x] = 37


changeSeason(1)
# Draws the map.
for y in range(0, MAP_Y):
    for z in range(0, MAP_Z):
        for x in range(0, MAP_X):

            if not map[y][z][x] == -1:
                row, column = divmod(map[y][z][x], 9)
                tile = sprites.crop((TILE_WIDTH * column, TILE_HEIGHT * row,
                                    TILE_WIDTH * (column + 1), TILE_HEIGHT * (row + 1)))

                tileX = (x - z) * (TILE_WIDTH / 2)
                tileY = (x + z) * (ISO_TILE_HEIGHT / 2)
                tileY -= y * (ISO_TILE_HEIGHT + 1)
                bg.paste(tile, (int(tileX) + 56, int(tileY)+48), mask=tile)

bg = bg.resize((128*4, 128*4), resample=Image.Resampling.NEAREST)
bg.save("image.png", "PNG")
