# Width and height of single isometric tile on 2D spritesheet.
TILE_WIDTH = 16
TILE_HEIGHT = 18

# Height of one tile in isometric view.
ISO_TILE_HEIGHT = 8

# All blocks that can generate.
# TODO: Add chances and $$$ values.
BLOCKS = {
    'sand': 4,  # [4, 5],
    'snow': 15,
    'hay': 17,
    'wood':  30,  # [27, 30, 33],
    'orange': 40,
    'cherry': 41,
    'coal': 49,
    'gold': 50,
    'ruby': 51,
    'emerald': 52,
    'diamond': 53,
    'goldblock': 81,
    'emeraldblock': 82,
    'diamondblock': 83,
}

# Time it takes to generate one block of resources on the island (in seconds).
GENERATIONTIME = 120
