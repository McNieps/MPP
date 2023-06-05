import pygame

from src.engine.app import App
from src.engine.tools import transparent_color
from src.engine.handlers.loop_handler import LoopHandler

from src.instances.game import game


def menu():
    # Instance initialization
    window = pygame.display.get_surface()

    title_font = pygame.font.Font(f"{App.ASSETS_PATH}/font/prolamina.ttf", 60)
    title_surf = title_font.render("Menu", False, (255, 255, 255), transparent_color)
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
                if event.key == pygame.K_RETURN:
                    game()
                if event.key == pygame.K_ESCAPE:
                    LoopHandler.quit_game()

        # Computing

        # Rendering
        window.fill((0, 0, 0))
        window.blit(title_surf, title_rect)

        pygame.display.flip()

    return window.copy()


if __name__ == '__main__':
    App.init("../../assets")
    menu()
