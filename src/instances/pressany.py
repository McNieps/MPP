import pygame
import math
import time

from src.engine.app import App
from src.engine.tools import outline_surf, transparent_color
from src.engine.handlers.loop_handler import LoopHandler

from src.instances.menu import menu


def press_any():
    # Instance initialization
    window = pygame.display.get_surface()

    title_font = pygame.font.Font(f"{App.ASSETS_PATH}/font/prolamina.ttf", 60)
    title_surf = title_font.render("Mega PyPong!", False, (255, 255, 255), transparent_color)
    title_surf.set_colorkey(transparent_color)
    title_rect = title_surf.get_rect()
    title_rect.center = 200, 75
    title_offset = 5

    message_font = pygame.font.Font(f"{App.ASSETS_PATH}/font/prolamina.ttf", 21)
    message_surf = message_font.render("Press any key to continue", False, (255, 255, 255), transparent_color)
    message_surf.set_colorkey(transparent_color)
    message_rect = message_surf.get_rect()
    message_rect.center = 200, 275

    # Loop
    while LoopHandler.is_running():
        # Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                LoopHandler.quit_game()
            if event.type == pygame.KEYDOWN:
                menu()
                LoopHandler.quit_game()

        # Computing
        title_angle = 10 * math.cos(time.time() / 2 + 13) + title_offset
        title_size = 0.75 + (1 + math.sin(time.time() / 3 + 19)) / 4
        title_temp_surf = pygame.transform.scale_by(title_surf, title_size)
        title_temp_surf = pygame.transform.rotate(title_temp_surf, title_angle)

        title_temp_surf = outline_surf(title_temp_surf, (0, 0, 0))
        title_temp_surf = outline_surf(title_temp_surf, (0, 0, 0))
        title_temp_surf = outline_surf(title_temp_surf, (255, 255, 255))
        title_temp_surf = outline_surf(title_temp_surf, (255, 255, 255))

        new_size = title_temp_surf.get_size()
        new_size = new_size[0] * abs(math.sin(time.time())), new_size[1]
        title_temp_surf = pygame.transform.scale(title_temp_surf, new_size)
        if math.sin(time.time()) < 0:
            title_temp_surf = pygame.transform.flip(title_temp_surf, True, False)
            title_temp_surf.set_alpha(126)

        title_temp_rect = title_temp_surf.get_rect()
        title_temp_rect.center = title_rect.center

        message_alpha = int((0.5 + 0.4 * math.sin(time.time()*4))*256)
        message_surf.set_alpha(message_alpha)

        # Rendering
        window.fill((0, 0, 0))
        window.blit(title_temp_surf, title_temp_rect)
        window.blit(message_surf, message_rect)

        pygame.display.flip()

    return window.copy()


if __name__ == '__main__':
    App.init("../../assets")
    press_any()
