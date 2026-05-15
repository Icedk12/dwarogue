import pygame

class EventManager:
    """Manages the pygame.event.get() stream and passes events to all necessary scripts"""

    #   INFO:
    #   Author: tompl
    #   Status: Implemented, not applied

    #################################################
    ##                    INIT                     ##
    #################################################   

    def __init__(self, game):
        self.game = game

    #################################################
    ##                   EVENTS                    ##
    #################################################

    def gather_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.x_button_pressed() ### QUIT

            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                if event.type == pygame.KEYDOWN:
                    self.game.input_manager.handle_keyboard_input(event) ### KEYS

            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL, pygame.MOUSEMOTION):
                self.game.input_manager.handle_mouse_input(event) ### MOUSE

    #################################################
    ##           EVENT SPECIFIC FUNCTIONS          ##
    #################################################

    def x_button_pressed(self):
        self.game.running = False
        # TODO: add saving