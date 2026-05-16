import pygame
from src.internal.createinfos.MapCreateInfo import MapCreateInfo
from src.objects.map.Map import Map

class MapManager:
    """Manages map storage and generation (wrapper)."""
    #   INFO:
    #   Author: tompl
    #   Status: In Progress

    #################################################
    ##                    INIT                     ##
    #################################################

    def __init__(self, game,  MapCreateInfo : MapCreateInfo):
        ###### SETUP ######
        self.game = game
        self.map = Map(self.game, MapCreateInfo)

        ###### GENERATION ######
        self.world_generator = None
        self.generating = False
        self.generation_progress = 0.0

    #################################################
    ##                 GENERATION                  ##
    #################################################

    def start_world_generation(self):
        """Starts async world generation"""

        # Create generator
        self.world_generator = (self.map.generate_world_async())

        # Update state
        self.generating = True
        self.generation_progress = 0.0

    def update_world_generation(self):
        """Updates world generation."""
        if not self.generating:
            return # only continue if generating
        
        # Try to go to next generation 
        try:
            self.generation_progress = next(self.world_generator)
        except StopIteration:

            self.generating = False

            self.generation_progress = 1.0
            self.game.entity_manager.player.apply_gravity()
            self.game.input_manager.recentre_on_player()