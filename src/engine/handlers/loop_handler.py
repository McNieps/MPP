import pygame
import sys


class LoopHandler:
    RUN = True
    FPS = 120
    DELTA = 1 / FPS
    CLOCK = pygame.time.Clock()

    @classmethod
    def is_running(cls):
        if cls.RUN:
            return True
        cls.RUN = True
        return False

    @classmethod
    def quit_instance(cls):
        cls.RUN = False

    @classmethod
    def quit_game(cls):
        sys.exit()

    @classmethod
    def limit_fps(cls):
        cls.DELTA = cls.CLOCK.tick(cls.FPS)/1000
        return cls.DELTA
