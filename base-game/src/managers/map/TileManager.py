from src.objects.map.Tile import Tile
from src.internal.createinfos.TileCreateInfo import TileCreateInfo

class TileManager:
    def __init__(self, game):
        self.floor_tiles = {
            1: Tile(game, TileCreateInfo("grass", True))      
        }

        self.wall_tiles = {
            2: Tile(game, TileCreateInfo("stone_wall", False))
        }