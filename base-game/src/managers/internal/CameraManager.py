import pygame

class CameraManager:
    def __init__(self, game):
        self.camera = pygame.Vector2((game.map_manager.width // 2) * game.map_manager.tile_size, (game.map_manager.height // 2) * game.map_manager.tile_size)
        self.z = game.map_manager.depth // 2

        self.is_panning = False

        self.zoom_level = 1.0
        self.last_mouse_pos = (0, 0)

        