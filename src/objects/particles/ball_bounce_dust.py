import pygame
import random

from src.objects.particles.particle import Particle


class BallBounceDust(Particle):
    def __init__(self, collision_point, object_that_bounce):

        speed = pygame.math.Vector2(object_that_bounce.vx, object_that_bounce.vy)
        speed.rotate_ip(random.randint(-20, 20))
        speed *= random.randint(100, 800) / 1000

        size, lifetime = self._get_size_and_lifetime(speed)

        super().__init__(collision_point, speed, size, 0.05, lifetime)

    @classmethod
    def create(cls, collision_point, object_that_bounce, quantity=None):
        if quantity is None:
            speed = pygame.Vector2(object_that_bounce.vx, object_that_bounce.vy).magnitude()
            quantity = round(speed/10)

        for i in range(quantity):
            BallBounceDust(collision_point, object_that_bounce)

    def _get_size_and_lifetime(self, speed: pygame.math.Vector2):
        size = 1+10*speed.magnitude()/500+random.randint(0, 2)
        lifetime = size/6
        return size, lifetime

    def draw(self, surface):
        size = int(self.base_size*((self.current_ratio-1)*-1)**0.5)
        if size < 1:
            size = 1
        ellipse_rect = pygame.Rect(0, 0, size, size)
        ellipse_rect.center = self.x, self.y
        pygame.draw.ellipse(surface, (255, 255, 255), ellipse_rect)
