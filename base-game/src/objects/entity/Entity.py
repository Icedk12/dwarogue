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
        """Moves the player down until they land on solid ground."""
        falling = False

        while True:
            below = pygame.Vector3(self.pos.x, self.pos.y, self.pos.z - 1)

            # stop at bottom of map
            if self.pos.z <= 0:
                break
            # if tile below is solid → stop falling
            if self.game.map_manager.map.get_tile_id(below) != 0:
                break
            # otherwise fall
            self.pos.z -= 1
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
            return

        tile_size = self.game.map_manager.map.tile_size

        # world → pixel
        world_x = self.pos.x * tile_size
        world_y = self.pos.y * tile_size

        # camera is already pixel space
        cam = self.game.camera_manager.camera

        # screen space
        screen_x = (world_x - cam.x) * scale
        screen_y = (world_y - cam.y) * scale

        image = self.game.asset_manager.get_image(self.image, scale)

        if image:
            self.game.screen.blit(image, (screen_x, screen_y))
