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

    def has_solid_ground_below(self):
        """Check if there's a solid tile directly below current position."""
        if self.pos.z <= 0:
            return True

        below = pygame.Vector3(self.pos.x, self.pos.y, self.pos.z - 1)
        tile_id = self.game.map_manager.map.get_tile_id(below)
        return tile_id != 0

    def apply_gravity(self):
        """Fall down until standing on solid ground (not in air)."""
        while self.pos.z > 0:
            current_tile_id = self.game.map_manager.map.get_tile_id(self.pos)
            if current_tile_id != 0:  # Standing on something, not air
                break
            self.pos.z -= 1  # In air, fall down

    #################################################
    ##                    MOVE                     ##
    #################################################

    def move_and_return(self, direction_vec2):
        """This function handles walking, gravity application and climbing"""
        ######## WALKING ########

        new_x = self.pos.x + direction_vec2.x
        new_y = self.pos.y + direction_vec2.y

        # Keep this as a proper Vector3 object for safety
        new_position = pygame.Vector3(new_x, new_y, self.pos.z)

        # Check if wall blocks horizontal movement at current z
        if self.game.map_manager.map.is_wall_blocking(new_position):
            # Wall blocks, try climbing
            for z_layer in range(1, self.max_climb_height + 1):
                new_position.z = self.pos.z + z_layer
                if not self.game.map_manager.map.is_wall_blocking(new_position):
                    # Update fields directly instead of wiping the object out
                    self.pos.x = new_position.x
                    self.pos.y = new_position.y
                    self.pos.z = new_position.z
                    self.apply_gravity()
                    return True
            return False  # Can't climb over

        # Assign fields directly to keep the original Vector3 intact
        self.pos.x = new_position.x
        self.pos.y = new_position.y
        self.apply_gravity()
        return True
            
    #################################################
    ##                    DRAW                     ##
    #################################################
    def draw(self, scale=1.0):

        if self.pos.z != self.game.camera_manager.z:
            return

        tile_size = self.game.map_manager.map.tile_size
        cam = self.game.camera_manager.camera
        screen = self.game.screen

        screen_center_x = screen.get_width() // 2
        screen_center_y = screen.get_height() // 2

        # tile space → screen space (consistent with Map.draw)
        screen_x = screen_center_x + (self.pos.x - cam.x) * tile_size * scale
        screen_y = screen_center_y + (self.pos.y - cam.y) * tile_size * scale

        image = self.game.asset_manager.get_image(self.image, scale)

        if image:
            self.game.screen.blit(image, (int(screen_x), int(screen_y)))
