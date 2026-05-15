import pygame
from src.internal.createinfos.EntityCreateInfo import EntityCreateInfo

class Entity:
    """A class that is used for objects that are rendered above the map and can move on the grid.
    For example: a player, npc, dropped item, etc.
    """

    #   INFO:
    #   Author: tompl
    #   Status: Implemented 
    #   Note: ヤラレっぱなしじゃ 大人しくはなれない!!!

    #################################################
    ##                    INIT                     ##
    #################################################

    def __init__(self, game, entity_settings : EntityCreateInfo):
        ######### BARE METAL SETUP #########
        self.entity_settings = entity_settings # An EntityCreateInfo object
        self.game = game

        ######### VARIABLE SETUP #########
        self.image = self.entity_settings.image # image name (filename but without .png)

        self.pos = self.entity_settings.position # pygame.Vector3 (x,y,z)
        self.name = self.entity_settings.name # String containing the name

        self.max_climb_height = 1
        self.alive = True

    #################################################
    ##                  GRAVITY                    ##
    #################################################

    def apply_gravity(self):
        """Moves the player down a level until they are not in the air."""
        falling = False
        while self.game.map_manager.map.get_tile_id(self.pos) == 0: # Checks if the floor tile at the players pos is air (0)
            if self.pos.z <= 0:
                break # Prevents falling out of map
            self.pos.z -= 1 # Falls you down a layer
            falling = True
        return falling

    #################################################
    ##                    MOVE                     ##
    #################################################

    def move_and_return(self, direction_vec2):
        """This function handles walking, gravity application and climbing"""
        ######## WALKING ########
        # 愛憎塗れで 此処を連れ出して

        # Store the place where entity is trying to walk
        new_x = self.pos.x + direction_vec2.x
        new_y = self.pos.y + direction_vec2.y

        new_position = pygame.Vector3(new_x, new_y, self.pos.z)
        del new_x, new_y # Delete those placeholder variables because we don't need them anymore


        if self.game.map_manager.map.is_walkable(new_position):
            # If new pos is walkable, move to it, and then apply gravity
            self.pos = new_position
            self.apply_gravity()
            return True # Succeeded

        ######## CLIMBING ########
        for z_layer in range(1, self.max_climb_height + 1):
            new_position.z = self.pos.z + z_layer # Get the new z layer to step to

            if self.game.map_manager.map.is_walkable(new_position):
                self.pos = new_position
                return True # Succeeded
            
        del new_position # Just because. maybe remove idk what the implications are
        return False # Failed
            
    #################################################
    ##                    DRAW                     ##
    #################################################
    def draw(self, scale=1.0):
        if self.pos.z != self.game.camera_manager.z:
            return # Not on same z level as camera dont draw

        # Stores the position of the entity in the world on the tile grid
        world_position = pygame.Vector2(
            self.pos.x * self.game.map_manager.map.tile_size,
            self.pos.y * self.game.map_manager.map.tile_size
        )
        # Holy shit thats a long vector 2 ------------------------------------------------------> bruh
        screen_position = pygame.Vector2(round((world_position.x - self.game.camera_manager.camera.x) * scale), round((world_position.y - self.game.camera_manager.camera.y) * scale))

        image = self.game.asset_manager.get_image(self.image, scale)
        
        if image:
            self.game.screen.blit(image, (screen_position.x, screen_position.y)) # Blit image to screen
