import pygame

class InputManager:
    def __init__(self):
        pass

    def handle_keyboard_input(self, event):
        if event.key == pygame.K_p:
            print("InputManager works!")
            
    def handle_mouse_input(self, event):
        pass