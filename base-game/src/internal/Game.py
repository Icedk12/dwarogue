import pygame

from src.internal.createinfos.GameCreateInfo import GameCreateInfo

from src.managers.graphics.AssetManager import AssetManager
from src.managers.internal.CameraManager import CameraManager
from src.managers.internal.InputManager import InputManager
from src.managers.internal.EventManager import EventManager
from src.managers.entity.EntityManager import EntityManager

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
        self.asset_manager = AssetManager("base-set") # TODO: make this changeable and a variable
        self.camera_manager = CameraManager(self) # This manages the camera
        self.input_manager = InputManager()
        self.event_manager = EventManager(self)

        ######### USER INTERFACE #########

        # TODO: this

        ######### MAP SETTINGS #########

        # TODO: make the map

        ######### TURN SYSTEM #########

        self.turn = 0

        ######### ASYNC LOADING #########


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
    