import pygame
from src.internal.createinfos.SimplexNoiseCreateInfo import SimplexNoiseCreateInfo

class MapCreateInfo:
    def __init__(self, width, height, depth, noise_settings : SimplexNoiseCreateInfo = SimplexNoiseCreateInfo(50, 4, 0.5, 2.0)):
        self.width = width
        self.height = height
        self.depth = depth

        self.scale = noise_settings.scale
        self.octaves = noise_settings.octaves
        self.persistence = noise_settings.persistence
        self.lacunarity = noise_settings.lacunarity
        self.seed = noise_settings.seed