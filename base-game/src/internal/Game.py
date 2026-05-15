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
        self.map_manager = MapManager(self, MapCreateInfo(100, 100, 50))
        self.camera_manager = CameraManager(self) # This manages the camera
        self.input_manager = InputManager(self)
        self.event_manager = EventManager(self)
        self.entity_manager = EntityManager(self)
        
        ######### PLAYER #########

        
        self.entity_manager.set_player(Player(self,EntityCreateInfo("Player",pygame.Vector3(0, 0, self.map_manager.map.depth - 1),"player")))



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
    
    def start(self):
        print("Started game.")
        self.map_manager.start_world_generation()
    
    def update(self):
        if self.map_manager.generating:
            self.map_manager.update_world_generation() # If map is generating still then update generation
            print(f"Generation progress {self.map_manager.generation_progress * 100:.1f}")
        else:
            self.entity_manager.update_turn()
            

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.map_manager.map.draw(self.screen, self.camera_manager.camera, self.camera_manager.z, self.camera_manager.zoom_level, self.global_debug)
        self.entity_manager.draw(self.screen, self.camera_manager.zoom_level)

    def loop(self):
        self.start() # Call start only once

        ### LOOP ###
        while self.running:
            self.event_manager.gather_events() # Wrapper for pygame.event.get()

            self.update()
            self.draw()
            pygame.display.flip()

            self.clock.tick(60)