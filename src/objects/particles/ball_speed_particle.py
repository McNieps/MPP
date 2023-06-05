import pygame
import random

from src.objects.particles.particle import Particle


class BallSpeedParticle(Particle):
    def __init__(self, position, speed):
        speedx, speedy = speed
        speedx *= 1+(random.randint(-20, 20)/100)
        speedy *= 1+(random.randint(-20, 20)/100)
        speedx += random.randint(-400, 400)/10
        speedy += random.randint(-400, 400)/10
        speed = speedx, speedy

        size = random.randint(8, 16)
        lifetime = random.randint(20, 40)/100

        super().__init__(position, speed, size, 0.03, lifetime)

    def draw(self, surface):
        size = int(self.base_size*((self.current_ratio-1)*-1))
        if size < 1:
            size = 1
        ellipse_rect = pygame.Rect(0, 0, size, size)
        ellipse_rect.center = self.x, self.y
        pygame.draw.ellipse(surface, (255, 255, 255), ellipse_rect)
