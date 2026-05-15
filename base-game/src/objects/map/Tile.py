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
        self.game = game

        ######### VARIABLE SETUP #########
        self.asset_name = self.tile_settings.asset_name
        self.walkable = self.tile_settings.is_walkable

    def draw(self, pos, scale=1.0, debug=False, alpha=None):
        image = self.game.asset_manager.get_image(self.asset_name)
