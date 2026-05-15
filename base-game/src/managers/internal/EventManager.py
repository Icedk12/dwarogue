import pygame

class EventManager:
    def __init__(self, game):
        self.game = game

    def gather_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.x_button_pressed() # Checks if the X button is pressed

            elif event.type == (pygame.KEYDOWN or pygame.KEYUP):
                self.game.input_manager.handle_keyboard_input(event) # Ask the game's input_manager to do stuff based on keys pressed

            elif event.type == (pygame.MOUSEBUTTONDOWN or pygame.MOUSEBUTTONUP):
                self.game.input_manager.handle_mouse_input(event) # Ask the game's input_manager to do stuff based on mouse

    def x_button_pressed(self):
        self.game.running = False
        # TODO: add saving