import pygame
import random

from src.objects.particles.particle import Particle


class PadSlamDust(Particle):
    def __init__(self, collision_point, speed):
        speed = pygame.math.Vector2(0, speed * random.randint(100, 800) / 1000)
        speed.rotate_ip(random.randint(60, 90))
        if random.randint(0, 1):
            speed.x *= -1

        size, lifetime = self._get_size_and_lifetime(speed)

        super().__init__(collision_point, speed, size, 0.05, lifetime)

    @classmethod
    def spawn_bunch(cls, collision_point, speed, quantity):
        for i in range(quantity):
            PadSlamDust(collision_point, speed)

    def _get_size_and_lifetime(self, speed: pygame.math.Vector2):
        size = 1+10*speed.magnitude()/500+random.randint(0, 2)
        lifetime = size/6
        return size, lifetime

    def draw(self, surface):
        size = int(self.base_size*((self.current_ratio-1)*-1))
        if size < 1:
            size = 1
        ellipse_rect = pygame.Rect(0, 0, size, size)
        ellipse_rect.center = self.x, self.y
        pygame.draw.ellipse(surface, (255, 255, 255), ellipse_rect)
