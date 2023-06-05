import pygame
import random

from src.engine.app import App
from src.objects.ball import Ball


class BallLauncher:
    MIN_SPEED = 50
    MAX_SPEED = 100
    FORBIDDEN_ANGLES = 35

    SURFACE = None

    def __init__(self, linked_arena):
        self.linked_arena = linked_arena

        self.done = False
        self.angle = 0
        self.speed = 0
        self.friction = 0.05

        self.load_assets()

    @classmethod
    def load_assets(cls):
        if cls.SURFACE:
            return

        cls.SURFACE = pygame.image.load(f"{App.ASSETS_PATH}/image/arrow.png").convert_alpha()

    def update(self, delta):
        if not self.done:
            self.speed *= self.friction ** delta
            self.angle = (self.angle + self.speed) % 360

            if self.speed < 0.1:
                self.done = True
                self.check_angle_legal_and_launch()

    def check_angle_legal_and_launch(self):
        fa = self.FORBIDDEN_ANGLES

        if 90-fa < self.angle < 90+fa or 270-fa < self.angle < 270+fa:
            self.launch(0.02)

        else:
            speed = tuple(pygame.Vector2(1, 0).rotate(self.angle))
            Ball(self.linked_arena, speed=speed)

    def launch(self, mult: float = 1):
        self.done = False
        self.speed = random.randint(round(self.MIN_SPEED*mult), round(self.MAX_SPEED*mult))

    def render(self, surface):
        if self.done:
            return

        arrow = pygame.transform.rotate(self.SURFACE, -self.angle)
        rect = arrow.get_rect()
        rect.center = 200, 150

        surface.blit(arrow, rect)
