import pygame
from src.managers.map.MapManager import MapManager
from src.internal.createinfos.MapCreateInfo import MapCreateInfo

class InputManager:
    """A manager class that calls functions from game and others to do things like contacting ui, fed input from an EventManager."""

    #   INFO:
    #   Author: tompl
    #   Status: Implemented and applied

    #################################################
    ##                    INIT                     ##
    #################################################

    def __init__(self, game):
        self.game = game
        self.player_took_action = False  # FIXED: Start at False so a turn doesn't fire instantly on load

        self.middle_mouse_held = False
        self.last_mouse_pos = None

    #################################################
    ##               INPUT FUNCTIONS               ##
    #################################################

    def handle_keyboard_input(self, event):
        """Takes in a pygame.event and does stuff with it :p"""
        if event.key == pygame.K_ESCAPE:
            self.game.running = False
            return  # Exit early

        if self.game.map_manager.generating:
            return

        # Track if the player's intentional movement succeeded
        moved = False

        # MOVEMENT #
        if event.key == pygame.K_w:
            moved = self.game.entity_manager.player.move_and_return(pygame.Vector2(0, -1))
        elif event.key == pygame.K_s:
            moved = self.game.entity_manager.player.move_and_return(pygame.Vector2(0, 1))
        elif event.key == pygame.K_a:
            moved = self.game.entity_manager.player.move_and_return(pygame.Vector2(-1, 0))
        elif event.key == pygame.K_d:
            moved = self.game.entity_manager.player.move_and_return(pygame.Vector2(1, 0))

        # If a movement key was hit AND the player successfully stepped somewhere
        if moved:
            self.recentre_on_player()
            self.player_took_action = True

        # WAIT #
        if event.key == pygame.K_SPACE:
            self.wait_turn()

        # REGENERATE DEBUG TOOL
        if event.key == pygame.K_r:
            self.regenerate()
            
        if event.key == pygame.K_o:
            self.debug_toggle()

    def handle_mouse_input(self, event):
        """Takes in a pygame.event and does stuff but mouse flavoured."""
        self.pan(event)

        if event.type == pygame.MOUSEMOTION:
            self.update_pan(event)

        if event.type == pygame.MOUSEWHEEL:
            ctrl_held = pygame.key.get_mods() & pygame.KMOD_CTRL
            if event.y > 0:
                if ctrl_held:
                    self.on_ctrl_scroll_up()
                else:
                    self.on_scroll_up()
            elif event.y < 0:
                if ctrl_held:
                    self.on_ctrl_scroll_down()
                else:
                    self.on_scroll_down()

    def pan(self, event):
        """Handles starting/stopping middle mouse drag"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:  # middle mouse
                self.middle_mouse_held = True
                self.last_mouse_pos = pygame.Vector2(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                self.middle_mouse_held = False
                self.last_mouse_pos = None

    def update_pan(self, event):
        """Applies camera movement while middle mouse is held"""
        if not self.middle_mouse_held:
            return

        current = pygame.Vector2(event.pos)

        if self.last_mouse_pos is not None:
            delta = current - self.last_mouse_pos
            zoom = self.game.camera_manager.zoom_level
            if zoom != 0:
                delta /= (zoom * self.game.map_manager.map.tile_size)

            self.game.camera_manager.camera.x -= delta.x
            self.game.camera_manager.camera.y -= delta.y

        self.last_mouse_pos = current

    def wait_turn(self):
        self.player_took_action = True

    def on_ctrl_scroll_up(self):
        self.game.camera_manager.zoom_level = min(self.game.camera_manager.zoom_level + 0.5, 4.0)

    def on_ctrl_scroll_down(self):
        self.game.camera_manager.zoom_level = max(self.game.camera_manager.zoom_level - 1.0, 0.5)

    def on_scroll_up(self):
        self.game.camera_manager.z = min(
            self.game.camera_manager.z + 1,
            self.game.map_manager.map.depth - 1
        )

    def on_scroll_down(self):
        self.game.camera_manager.z = max(self.game.camera_manager.z - 1, 0)

    def debug_toggle(self):
        self.game.global_debug = not self.game.global_debug

    def regenerate(self):
        self.game.map_manager = MapManager(self.game, MapCreateInfo(200, 200, 50))
        self.game.generate_map()

    def recentre_on_player(self):
        player_pos = self.game.entity_manager.player.pos
        self.game.camera_manager.camera.x = player_pos.x
        self.game.camera_manager.camera.y = player_pos.y
        self.game.camera_manager.z = int(player_pos.z)