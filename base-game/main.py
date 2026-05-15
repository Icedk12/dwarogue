import pygame
from src.internal.Game import Game
from src.internal.createinfos.GameCreateInfo import GameCreateInfo

pygame.init()

game = Game(GameCreateInfo((1920, 1080), "Arial", "dwarogue"))

game.loop()

pygame.quit()