import pygame


class App:
    WINDOW = None
    WINDOW_SIZE = (400, 300)
    ASSETS_PATH = None

    @classmethod
    def init(cls, assets_path=""):
        cls.ASSETS_PATH = assets_path

        # pygame.mixer.pre_init(size=16, buffer=256)
        pygame.init()
        pygame.mixer.set_num_channels(64)

        cls.WINDOW = pygame.display.set_mode(cls.WINDOW_SIZE, pygame.SCALED)
        pygame.mouse.set_visible(False)
