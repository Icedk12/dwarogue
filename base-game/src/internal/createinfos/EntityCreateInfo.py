import pygame

class EntityCreateInfo:
    def __init__(self, name, position : pygame.Vector3, image):
        self.image = image
        self.name = name
        self.position = position