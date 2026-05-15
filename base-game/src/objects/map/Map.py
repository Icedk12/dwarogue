from opensimplex import noise2array, seed

import numpy as np
import math

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

        #################################################
        ##             NOISE SETTINGS                  ##
        #################################################

        self.scale = create_info.scale

        self.octaves = create_info.octaves

        self.persistence = create_info.persistence

        self.lacunarity = create_info.lacunarity

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
        ##                    SEED                     ##
        #################################################

        seed(0)

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

                self.tiles[surface_z, y, x] = self.tile_manager.TILE_GRASS

            #################################################
            ##              GENERATION YIELD               ##
            #################################################

            yield 0.75 + (y / self.height) * 0.20

    #################################################
    ##                   DRAWING                   ##
    #################################################

    def draw(self, surface, camera_pos, current_z, zoom_level=1.0, debug=False):
        """Draws visible tiles."""

        #################################################
        ##             CAMERA CULLING                  ##
        #################################################

        visible_world_w = (surface.get_width() / zoom_level)

        visible_world_h = (
            surface.get_height() / zoom_level)

        start_x = max(0, int(camera_pos.x // self.tile_size))

        start_y = max(0, int(camera_pos.y // self.tile_size))

        end_x = min(self.width, int((camera_pos.x + visible_world_w) // self.tile_size) + 2)

        end_y = min(self.height, int((camera_pos.x + visible_world_h) // self.tile_size) + 2)

        #################################################
        ##                DRAW LOOP                    ##
        #################################################

        for y in range(start_y, end_y):

            world_y = y * self.tile_size

            screen_y = int(
                math.floor(
                    (
                        world_y
                        - camera_pos.y
                    )
                    * zoom_level
                )
            )

            for x in range(start_x, end_x):

                tile_id = self.tiles[
                    current_z,
                    y,
                    x
                ]

                #################################################
                ##                 SKIP AIR                    ##
                #################################################

                if tile_id == self.tile_manager.TILE_AIR:
                    continue

                #################################################
                ##               GET TILE OBJECT               ##
                #################################################

                tile = self.tile_manager.get_tile(
                    tile_id
                )

                if tile is None:
                    continue

                #################################################
                ##              SCREEN POSITION                ##
                #################################################

                world_x = x * self.tile_size

                screen_x = int(
                    math.floor(
                        (
                            world_x
                            - camera_pos.x
                        )
                        * zoom_level
                    )
                )

                #################################################
                ##                 DRAW TILE                   ##
                #################################################

                tile.draw(
                    (
                        screen_x,
                        screen_y
                    ),
                    scale=zoom_level,
                    debug=debug
                )

    #################################################
    ##               TILE HELPERS                  ##
    #################################################

    def in_bounds(self, x, y, z=None):
        """Returns True if coordinates are valid."""

        if not (0 <= x < self.width):
            return False

        if not (0 <= y < self.height):
            return False

        if z is not None:
            return 0 <= z < self.depth

        return True

    #################################################
    ##               TILE LOOKUPS                  ##
    #################################################

    def get_tile_id(self, x, y, z):
        """Returns tile id at coordinates."""

        if not self.in_bounds(x, y, z):
            return -1

        return self.tiles[z, y, x]

    def set_tile_id(self, x, y, z, tile_id):
        """Sets tile id at coordinates."""

        if not self.in_bounds(x, y, z):
            return

        self.tiles[z, y, x] = tile_id

    def get_tile(self, x, y, z):
        """Returns tile object."""

        tile_id = self.get_tile_id(x, y, z)

        if tile_id <= 0:
            return None

        return self.tile_manager.get_tile(tile_id)

    #################################################
    ##               WALKABILITY                   ##
    #################################################

    def is_walkable(self, x, y, z):
        """Returns if tile is walkable."""

        tile = self.get_tile(x, y, z)

        if tile is None:
            return True

        return getattr(tile, "walkable", False)

    #################################################
    ##             SURFACE HELPERS                 ##
    #################################################

    def get_surface_z(self, x, y):
        """Returns cached surface z."""

        if not self.in_bounds(x, y):
            return 0

        return self.heightmap[y, x]