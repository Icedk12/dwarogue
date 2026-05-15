from src.objects.map.Tile import Tile
from src.internal.createinfos.TileCreateInfo import TileCreateInfo


class TileManager:
    """Stores and manages all tile definitions."""

    #   INFO:
    #   Author: tompl
    #   Status: Implemented
    #   TODO: Add JSON tile creation

    #################################################
    ##                  TILE IDS                  ##
    #################################################

    TILE_AIR = 0
    TILE_GRASS = 1
    TILE_STONE_WALL = 2

    #################################################
    ##                    INIT                    ##
    #################################################

    def __init__(self, game):

        #################################################
        ##               FLOOR TILES                 ##
        #################################################

        self.floor_tiles = {
            self.TILE_GRASS: Tile(game, TileCreateInfo("grass", True))
        }

        #################################################
        ##                WALL TILES                 ##
        #################################################

        self.wall_tiles = {
            self.TILE_STONE_WALL: Tile(game, TileCreateInfo("stone_wall", False))
        }

    #################################################
    ##               TILE LOOKUPS                 ##
    #################################################

    def get_tile(self, tile_id):
        """Returns tile object from tile id."""

        #################################################
        ##                FLOOR TILE                 ##
        #################################################

        tile = self.floor_tiles.get(tile_id)

        if tile is not None:
            return tile

        #################################################
        ##                 WALL TILE                 ##
        #################################################

        return self.wall_tiles.get(tile_id)