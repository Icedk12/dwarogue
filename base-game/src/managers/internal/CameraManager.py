import pygame

class CameraManager:
    def __init__(self, game):
        self.camera = pygame.Vector2((game.map_manager.map.width // 2) * game.map_manager.map.tile_size, (game.map_manager.map.height // 2) * game.map_manager.map.tile_size)
        self.z = int(game.map_manager.map.depth * 0.8)

        self.is_panning = False

        self.zoom_level = 1.0
        self.last_mouse_pos = (0, 0)