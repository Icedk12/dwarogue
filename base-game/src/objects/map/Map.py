from opensimplex import noise2array, seed
import random

import pygame
import numpy as np

from src.managers.map.TileManager import TileManager


class Map:

    #   INFO:
    #   Author: tompl
    #   Status: In Progress

    #################################################
    ##                    INIT                     ##
    #################################################

    def __init__(self, game, create_info):
        """Creates and stores all world data."""

        self.game = game

        #################################################
        ##               CREATE INFO                   ##
        #################################################

        self.create_info = create_info

        #################################################
        ##                WORLD SIZE                   ##
        #################################################

        self.width = create_info.width
        self.height = create_info.height
        self.depth = create_info.depth

        self.tile_size = 32
        self.lower_view_layers = 1
        self.rendered_tiles_num = 0

        #################################################
        ##             NOISE SETTINGS                  ##
        #################################################

        self.scale = create_info.scale
        self.octaves = create_info.octaves
        self.persistence = create_info.persistence
        self.lacunarity = create_info.lacunarity

        self.seed = create_info.seed # Important

        #################################################
        ##               TILE MANAGER                  ##
        #################################################

        self.tile_manager = TileManager(game)

        #################################################
        ##               WORLD STORAGE                 ##
        #################################################

        # Full voxel storage
        # tiles[z, y, x]

        self.tiles = np.zeros(
            (
                self.depth,
                self.height,
                self.width
            ),
            dtype=np.uint16
        )

        #################################################
        ##                HEIGHTMAP                    ##
        #################################################

        self.heightmap = np.zeros(
            (
                self.height,
                self.width
            ),
            dtype=np.uint16
        )

        #################################################
        ##                 BIOMES                      ##
        #################################################

        self.biome_map = np.zeros(
            (
                self.height,
                self.width
            ),
            dtype=np.uint8
        )

        #################################################
        ##               STRUCTURES                    ##
        #################################################

        self.structures = []

    #################################################
    ##             WORLD GENERATION                ##
    #################################################

    def generate_world_async(self):
        """Runs all world generation passes."""

        #################################################
        ##            BASE TERRAIN PASS                ##
        #################################################

        #### Random seed ####
        if self.seed is None: 
            self.seed = random.randint(-999999999, 999999999)
            
        seed(self.seed) # Actually set the seed

        yield from self.generate_base_terrain()

        #################################################
        ##            SURFACE TILE PASS                ##
        #################################################

        yield from self.generate_surface_tiles()

        #################################################
        ##              FUTURE PASSES                  ##
        #################################################

        # TODO:
        #
        # yield from self.generate_caves()
        # yield from self.generate_biomes()
        # yield from self.generate_water()

        #################################################
        ##                   DONE                      ##
        #################################################

        yield 1.0

    #################################################
    ##              BASE TERRAIN                   ##
    #################################################

    def generate_base_terrain(self):
        """Generates terrain heightmap."""

        #################################################
        ##             TERRAIN SETTINGS                ##
        #################################################

        sea_level = int(self.depth * 0.7)

        max_height = int(self.depth * 0.2)

        #################################################
        ##             NOISE GENERATION                ##
        #################################################

        total_noise = np.zeros(
            (
                self.height,
                self.width
            ),
            dtype=np.float32
        )

        amplitude = 1.0

        frequency = 1.0

        max_amplitude = 0.0

        for octave in range(self.octaves):

            #################################################
            ##              GENERATE OCTAVE                ##
            #################################################

            xs = (
                np.arange(self.width)
                / self.scale
                * frequency
            )

            ys = (
                np.arange(self.height)
                / self.scale
                * frequency
            )

            octave_noise = noise2array(xs, ys)

            total_noise += (
                octave_noise
                * amplitude
            )

            #################################################
            ##             TRACK AMPLITUDE                 ##
            #################################################

            max_amplitude += amplitude

            amplitude *= self.persistence

            frequency *= self.lacunarity

            #################################################
            ##              GENERATION YIELD               ##
            #################################################

            yield octave / (
                self.octaves * 2
            )

        #################################################
        ##               NORMALIZATION                 ##
        #################################################

        total_noise /= max_amplitude

        normalized_noise = (
            total_noise + 1.0
        ) / 2.0

        #################################################
        ##             GENERATE HEIGHTMAP              ##
        #################################################

        generated_heightmap = (
            sea_level +
            (
                normalized_noise
                * max_height
            ).astype(np.int32)
        )

        #################################################
        ##              STORE HEIGHTMAP                ##
        #################################################

        self.heightmap[:] = generated_heightmap

        #################################################
        ##                FILL WORLD                   ##
        #################################################

        for y in range(self.height):
            for x in range(self.width):

                surface_z = generated_heightmap[y, x]

                #################################################
                ##               SURFACE TILE                  ##
                #################################################

                if self.tiles[surface_z, y, x] == 0:
                    self.tiles[surface_z, y, x] = self.tile_manager.TILE_GRASS

                #################################################
                ##               UNDERGROUND                   ##
                #################################################

                for z in range(surface_z):
                    self.tiles[z, y, x] = self.tile_manager.TILE_STONE_WALL

            #################################################
            ##              GENERATION YIELD               ##
            #################################################

            yield 0.5 + (y / self.height) * 0.25

    #################################################
    ##              SURFACE PASS                   ##
    #################################################

    def generate_surface_tiles(self):
        """Handles future biome tile replacement."""

        for y in range(self.height):
            for x in range(self.width):

                surface_z = self.heightmap[y, x]

                #################################################
                ##             FUTURE BIOME LOGIC              ##
                #################################################

                # Example:
                #
                # biome = self.biome_map[y, x]
                #
                # if biome == DESERT:
                #     sand
                #
                # if biome == TUNDRA:
                #     snow

                if self.tiles[surface_z, y, x] == 0:
                    self.tiles[surface_z, y, x] = self.tile_manager.TILE_GRASS

            #################################################
            ##              GENERATION YIELD               ##
            #################################################

            yield 0.75 + (y / self.height) * 0.20

    #################################################
    ##                   DRAWING                   ##
    #################################################

    def draw(self, surface, camera_pos: pygame.Vector2, current_z: int, zoom_level: float, debug=False):
        """Draws visible tiles with layers below shown at reduced opacity."""
        self.rendered_tiles_num = 0
        
        tile_size = self.tile_size
        visible_tiles_w = surface.get_width() / (tile_size * zoom_level)
        visible_tiles_h = surface.get_height() / (tile_size * zoom_level)

        cam_x = camera_pos.x
        cam_y = camera_pos.y
        cull_buffer = 2

        start_x = max(0, int(cam_x - visible_tiles_w // 2 - cull_buffer))
        start_y = max(0, int(cam_y - visible_tiles_h // 2 - cull_buffer))
        end_x = min(self.width, int(cam_x + visible_tiles_w // 2 + cull_buffer))
        end_y = min(self.height, int(cam_y + visible_tiles_h // 2 + cull_buffer))

        screen_center_x = surface.get_width() // 2
        screen_center_y = surface.get_height() // 2

        # Draw layers below first (so current layer is on top)
        levels_below = self.lower_view_layers
        for z_offset in range(1, levels_below + 1):
            z = current_z - z_offset
            if z < 0:
                break

            alpha = int((1.0 - (z_offset / (levels_below + 1))) * 255)

            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    tile_id = self.tiles[z, y, x]
                    above_tile_id = self.tiles[z + 1, y, x]

                    if above_tile_id != self.tile_manager.TILE_AIR:
                        continue

                    if tile_id == self.tile_manager.TILE_AIR:
                        continue
                    
                    tile = self.tile_manager.get_tile(tile_id)
                    if tile is None:
                        continue

                    screen_x = screen_center_x + (x - cam_x) * tile_size * zoom_level
                    screen_y = screen_center_y + (y - cam_y) * tile_size * zoom_level

                    tile.draw((int(screen_x), int(screen_y)), scale=zoom_level, debug=debug, alpha=alpha)
                    self.rendered_tiles_num += 1

        # Draw current layer at full opacity
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile_id = self.tiles[current_z, y, x]
                if tile_id == self.tile_manager.TILE_AIR:
                    continue

                tile = self.tile_manager.get_tile(tile_id)
                if tile is None:
                    continue

                screen_x = screen_center_x + (x - cam_x) * tile_size * zoom_level
                screen_y = screen_center_y + (y - cam_y) * tile_size * zoom_level

                tile.draw((int(screen_x), int(screen_y)), scale=zoom_level, debug=debug)
                self.rendered_tiles_num += 1

    #################################################
    ##               TILE HELPERS                  ##
    #################################################

    def in_bounds_2d(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def in_bounds_3d(self, x, y, z):
        return (
            0 <= x < self.width and
            0 <= y < self.height and
            0 <= z < self.depth
        )
    
    #################################################
    ##               TILE LOOKUPS                  ##
    #################################################

    def set_tile_id(self, pos, tile_id):
        """Sets tile id at coordinates."""

        if pos.z is None:
            return

        if pos.z is None:
            return False

        if not self.in_bounds_3d(pos.x, pos.y, pos.z):
            return False

        self.tiles[int(pos.z), int(pos.y), int(pos.x)] = tile_id

    def get_tile_id(self, pos):
        """Returns tile id at coordinates."""

        if pos.z is None:
            return -1  # invalid for voxel access

        if pos.z is None:
            return False

        if not self.in_bounds_3d(pos.x, pos.y, pos.z):
            return False

        return self.tiles[int(pos.z), int(pos.y), int(pos.x)]

    def get_tile(self, pos):
        """Returns tile object."""

        tile_id = self.get_tile_id(pos)

        if tile_id <= 0:
            return None

        return self.tile_manager.get_tile(tile_id)

    #################################################
    ##               WALKABILITY                   ##
    #################################################

    def is_walkable(self, pos):
        """Returns if tile is walkable."""

        tile = self.get_tile(pos)

        if tile is None:
            return True

        return getattr(tile, "walkable", False)

    def is_wall_blocking(self, pos):
        """Returns if there's a solid wall blocking horizontal movement."""

        tile = self.get_tile(pos)

        if tile is None:
            return False

        return not getattr(tile, "walkable", False)

    #################################################
    ##             SURFACE HELPERS                 ##
    #################################################
    
    def get_surface_z(self, x, y):
        if not self.in_bounds_2d(x, y):
            return 0
        return self.heightmap[int(y), int(x)]