import pygame

from src.internal.createinfos.GameCreateInfo import GameCreateInfo
from src.internal.createinfos.MapCreateInfo import MapCreateInfo
from src.internal.createinfos.EntityCreateInfo import EntityCreateInfo

from src.managers.graphics.AssetManager import AssetManager
from src.managers.internal.CameraManager import CameraManager
from src.managers.internal.InputManager import InputManager
from src.managers.internal.EventManager import EventManager
from src.managers.entity.EntityManager import EntityManager
from src.managers.map.MapManager import MapManager

from src.objects.entity.player.Player import Player

class Game:
    """A self sustaining game class that supports asset managment and all that jazz."""

    #################################################
    ##                    INIT                     ##
    #################################################
    
    def __init__(self, game_settings : GameCreateInfo):
        ######### SETUP #########
        self.game_settings = game_settings

        ######### INITIALISATION #########
        self.init_font()
        self.init_window() # Creates window and sets title

        ######### GAME LIFETIME VARIABLES #########
        self.clock = pygame.time.Clock()
        self.running = True

        ######### MANAGERS #########
        self.asset_manager = AssetManager("base_set") # TODO: make this changeable and a variable
        self.map_manager = MapManager(self, MapCreateInfo(200, 200, 50))
        self.camera_manager = CameraManager(self) # This manages the camera
        self.input_manager = InputManager(self)
        self.event_manager = EventManager(self)
        self.entity_manager = EntityManager(self)
        
        ######### PLAYER #########
        spawn_x = self.map_manager.map.width // 2
        spawn_y = self.map_manager.map.height // 2
        spawn_z = self.map_manager.map.depth

        self.entity_manager.set_player(
            Player(
                self,
                EntityCreateInfo(
                    "Player",
                    pygame.Vector3(spawn_x, spawn_y, spawn_z),
                    "player"
                )
            )
        )

        ######### USER INTERFACE #########
        # TODO: this

        ######### TURN SYSTEM #########
        self.turn = 0

        ######### DEBUG #########
        self.global_debug = False

    #################################################
    ##               INIT FUNCTIONS                ##
    #################################################

    def init_window(self):
        # Set the display size and caption to that in the GameCreateInfo
        self.screen = pygame.display.set_mode(self.game_settings.display_size)
        pygame.display.set_caption(self.game_settings.window_name)

    def init_font(self):
        # Init font module and create font
        pygame.font.init()
        self.font = pygame.font.SysFont(self.game_settings.font, 24, bold=False)

    #################################################
    ##               GAME FUNCTIONS                ##
    #################################################
    
    def draw_debug_label(self):
        debug_surface = self.font.render(
            f"FPS: {int(self.clock.get_fps())} | " 
            f"CAM_POS: {pygame.Vector3(int(self.camera_manager.camera.x), int(self.camera_manager.camera.y), int(self.camera_manager.z))} | "
            f"PLAYER_POS: {self.entity_manager.player.pos} | "
            f"VISIBLE_TILES: {self.map_manager.map.rendered_tiles_num} | "
            f"TURN: {self.turn}", 
            True,
            (255, 255, 255),
            (0, 0, 0)
        )
        self.screen.blit(debug_surface, (10, 10))

    def draw_loading_bar(self, x, y, max_width, height, progress):
        # Clamp progress
        progress = max(0.0, min(1.0, progress))
        
        # Calculate the dynamic width
        current_width = int(max_width * progress)
        
        # Draw the single rectangle
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, current_width, height))           

    def generate_map(self):
        print("Generating map...")
        self.map_manager.start_world_generation()
    
    def update(self):
        if self.map_manager.generating:
            self.map_manager.update_world_generation()
        else:
            if self.input_manager.player_took_action:
                self.entity_manager.update_turn()
                self.input_manager.player_took_action = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.map_manager.generating:
            bar_size = 30
            screen_size_tu = self.screen.get_size()
            self.draw_loading_bar(100, screen_size_tu[1] // 2 - bar_size, self.screen.get_size()[0] + 100, bar_size, self.map_manager.generation_progress)
            return
        
        self.map_manager.map.draw(self.screen, self.camera_manager.camera, self.camera_manager.z, self.camera_manager.zoom_level, False)
        self.entity_manager.draw(self.screen, self.camera_manager.zoom_level)
        if self.global_debug:
            self.draw_debug_label()

    def loop(self):
        self.generate_map() # Call start only once

        ### LOOP ###
        while self.running:

            self.event_manager.gather_events() # Wrapper for pygame.event.get()

            self.update()
            self.draw()
            pygame.display.flip()

            self.clock.tick(60)