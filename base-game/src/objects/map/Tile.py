import pygame
from src.internal.createinfos.TileCreateInfo import TileCreateInfo

class Tile:
    """A class that is represented in the map by an id which is referenced to get walkable data and other stuff."""

    #   INFO:
    #   Author: tompl
    #   Status: Done. i think 

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

    #################################################
    ##                    DRAW                     ##
    #################################################

    def draw(self, pos, scale=1.0, debug=False, alpha=None):
        # Get the image using assetmanager
        image = self.game.asset_manager.get_image(self.asset_name, scale, alpha)
        self.game.screen.blit(image, pos) # blit to screen

        if debug:
            # Draw a red square if not walkable and green if walkable
            # For debug purposes. not really i just like grids
            color = (0, 255, 0) if self.walkable else (255, 0, 0)
            rect = image.get_rect(topleft=pos)
            pygame.draw.rect(self.game.screen, color, rect, 1)
