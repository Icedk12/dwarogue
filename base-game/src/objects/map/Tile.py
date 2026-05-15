from src.internal.createinfos.TileCreateInfo import TileCreateInfo

class Tile:
    """A class that is represented in the map by an id which is referenced to get walkable data and other stuff."""

    #   INFO:
    #   Author: tompl
    #   Status: In progress 

    #################################################
    ##                    INIT                     ##
    #################################################

    def __init__(self, game, tile_settings : TileCreateInfo):
        ######### BARE METAL SETUP #########
        self.tile_settings = tile_settings

        ######### VARIABLE SETUP #########
        self.id = self.tile_settings.id
        self.walkable = self.tile_settings.is_walkable

