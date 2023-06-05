import pygame
import math
import time

from src.engine.app import App
from src.engine.tools import transparent_color
from src.engine.handlers.loop_handler import LoopHandler


def splash_screen():
    # Instance initialization
    window = pygame.display.get_surface()

    start_time = time.time()

    title_font = pygame.font.Font(f"{App.ASSETS_PATH}/font/prolamina.ttf", 60)
    title_surf = title_font.render("Placeholder splash", False, (255, 255, 255), transparent_color)
    title_surf.set_colorkey(transparent_color)
    title_rect = title_surf.get_rect()
    title_rect.center = 200, 75

    # Loop
    while LoopHandler.is_running():
        # Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                LoopHandler.quit_game()
            if event.type == pygame.KEYDOWN:
                LoopHandler.quit_instance()

        # Computing
        dt = time.time() - start_time
        text_alpha = int((math.sin(dt))*255)

        if text_alpha < 0:
            break

        title_surf.set_alpha(text_alpha)

        # Rendering
        window.fill((0, 0, 0))
        window.blit(title_surf, title_rect)

        pygame.display.flip()

    return window.copy()


if __name__ == '__main__':
    App.init("../../assets")
    splash_screen()
