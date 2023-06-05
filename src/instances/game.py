import pygame
import numpy as np
import random

from matplotlib import pyplot as plt


from src.engine.app import App
from src.engine.handlers.loop_handler import LoopHandler
from src.engine.handlers.resource_handler import ResourceHandler

from src.objects.arena import Arena
from src.objects.pad import Pad
from src.objects.ball import Ball
from src.objects.particles.particle import Particle
from src.objects.effects.effect import Effect


def game():
    # Instance initialization
    window = pygame.display.get_surface()

    arena = Arena()
    # Ball(arena)

    psy_mode = 0

    # Loop
    while LoopHandler.is_running():
        delta = LoopHandler.limit_fps()
        pygame.display.set_caption(str(LoopHandler.CLOCK.get_fps()))

        # Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                LoopHandler.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    LoopHandler.quit_instance()
                if event.key == pygame.K_RETURN:
                    psy_mode = (psy_mode + 1) % 4
                    print(f"Psy-mode {psy_mode}")

                if event.key == pygame.K_SPACE:
                    Ball.destroy_all()
                    Ball(arena, (20, 20), (0, -10))

        # Computing
        Pad.handle_inputs(delta)
        Pad.update(delta)
        Ball.update(delta, steps=4)
        arena.update(delta)
        Particle.update(delta)
        Effect.update_all(delta)

        # Rendering
        if psy_mode == 0:
            window.fill((0, 0, 0))
        elif psy_mode == 2:
            pygame.draw.rect(window, (0, 0, 0), (0, 0, 200, 300))
        elif psy_mode == 3:
            pygame.draw.rect(window, (0, 0, 0), (200, 0, 200, 300))

        Particle.draw_all(window)
        Ball.draw_all(window)
        Pad.draw_all(window)
        arena.draw(window)

        Effect.render_all(window)

        # left_surf = window.subsurface((0, 0, 200, 300))
        # left_surf.blit(pygame.transform.flip(left_surf, 0, 1), (0, 0))
        # right_surf = window.subsurface((200, 0, 200, 300))
        # right_surf.blit(pygame.transform.flip(right_surf, 0, 1), (0, 0))

        pygame.display.flip()

    return window.copy()


if __name__ == '__main__':
    App.init("../../assets")
    ResourceHandler.load()
    game()
