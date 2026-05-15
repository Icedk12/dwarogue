import pygame

class InputManager:
    """A manager class that calls functions from game and others to do things like contacting ui, fed input from an EventManager."""

    #   INFO:
    #   Author: tompl
    #   Status: Implemented, not applied

    #################################################
    ##                    INIT                     ##
    #################################################

    def __init__(self, game):
        self.game = game

        self.middle_mouse_held = False
        self.last_mouse_pos = None

    #################################################
    ##               INPUT FUNCTIONS               ##
    #################################################

    # TODO: these are pretty simple rn but will hold all input related tasks.

    def handle_keyboard_input(self, event):
        self.recentre_on_player()
        """Takes in a pygame.event and does stuff with it :p"""
        if event.key == pygame.K_w:
            self.game.entity_manager.player.move_and_return(pygame.Vector2(0, -1))
            self.recentre_on_player()
        elif event.key == pygame.K_s:
            self.game.entity_manager.player.move_and_return(pygame.Vector2(0, 1))
            self.recentre_on_player()
        elif event.key == pygame.K_a:
            self.game.entity_manager.player.move_and_return(pygame.Vector2(1, 0))
            self.recentre_on_player()
        elif event.key == pygame.K_d:
            self.game.entity_manager.player.move_and_return(pygame.Vector2(-1, 0))
            self.recentre_on_player()

    def recentre_on_player(self):
        player_pos = self.game.entity_manager.player.pos
        self.game.camera_manager.camera.x = player_pos.x
        self.game.camera_manager.camera.y = player_pos.y
        self.game.camera_manager.z = self.game.map_manager.map.depth - 1

    def handle_mouse_input(self, event):
        """Takes in a pygame.event and does stuff but mouse flavoured."""

        # always handle panning state first
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

            # optional: scale pan with zoom (feels better)
            zoom = self.game.camera_manager.zoom_level
            if zoom != 0:
                delta /= zoom

            self.game.camera_manager.camera.x -= delta.x
            self.game.camera_manager.camera.y -= delta.y

        self.last_mouse_pos = current

    def on_ctrl_scroll_up(self):
        self.game.camera_manager.zoom_level = min(self.game.camera_manager.zoom_level + 0.5, 4.0)
        print("Zoomed in")

    def on_ctrl_scroll_down(self):
        self.game.camera_manager.zoom_level = max(self.game.camera_manager.zoom_level - 0.5, 0.5)
        print("Zoomed out")

    def on_scroll_up(self):
        self.game.camera_manager.z = min(
            self.game.camera_manager.z + 1,
            self.game.map_manager.map.depth - 1
        )
        print(self.game.camera_manager.z)

    def on_scroll_down(self):
        self.game.camera_manager.z = max(self.game.camera_manager.z - 1, 0)
        print(self.game.camera_manager.z)