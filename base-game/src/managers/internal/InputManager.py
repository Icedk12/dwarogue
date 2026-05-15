import pygame

class InputManager:
    """A manager class that calls functions from game and others to do things like contacting ui, fed input from an EventManager."""

    #   INFO:
    #   Author: tompl
    #   Status: Basics done, uses not applied

    #################################################
    ##                    INIT                     ##
    #################################################

    def __init__(self):
        # TODO: maybe add a game ref here?
        pass

    #################################################
    ##               INPUT FUNCTIONS               ##
    #################################################

    # TODO: these are pretty simple rn but will hold all input related tasks.

    def handle_keyboard_input(self, event):
        """Takes in a pygame.event and does stuff with it :p"""
        if event.key == pygame.K_p:
            print("InputManager works!")

    def handle_mouse_input(self, event):
        """Takes in a pygame.event and does stuff but mouse flavoured."""
        pass