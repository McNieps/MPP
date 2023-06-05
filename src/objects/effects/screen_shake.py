import pygame
import random
import time
import math

from src.engine.shaders.chromatic_aberration import ChromaticAberrationShader
from src.objects.effects.effect import Effect


class ScreenShake(Effect):
    def __init__(self, xr, yr, xg, yg, xb, yb, lifetime):
        super().__init__(lifetime)

        self.xr = xr
        self.yr = yr
        self.xg = xg
        self.yg = yg
        self.xb = xb
        self.yb = yb

    @classmethod
    def create(cls,
               strength: float,
               aberration_mult: float = 0.25,
               lifetime: float = 0.25):

        aberration_strength = strength * aberration_mult

        direction = pygame.math.Vector2(strength, 0).rotate(random.randint(0, 360))
        r_dir = pygame.math.Vector2(aberration_strength, 0).rotate(random.randint(0, 360))
        g_dir = pygame.math.Vector2(aberration_strength, 0).rotate(random.randint(0, 360))
        b_dir = pygame.math.Vector2(aberration_strength, 0).rotate(random.randint(0, 360))

        xr, yr = direction + r_dir
        xg, yg = direction + g_dir
        xb, yb = direction + b_dir

        ScreenShake(xr, yr, xg, yg, xb, yb, lifetime)

    def render(self, surface):
        current_angle = math.pi * (time.time() - self.start_time) / self.lifetime
        cos = (math.cos(current_angle)+1)/2
        drx, dry = round(self.xr*cos), round(self.yr*cos)
        dgx, dgy = round(self.xg*cos), round(self.yg*cos)
        dbx, dby = round(self.xb*cos), round(self.yb*cos)
        ChromaticAberrationShader.shade(surface, ((drx, dry), (dgx, dgy), (dbx, dby)))
