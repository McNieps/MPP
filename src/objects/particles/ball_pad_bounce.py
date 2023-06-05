import pygame
import random
import math

from src.objects.particles.particle import Particle


class BallPadBounce(Particle):
    @classmethod
    def create(cls,
               point: pygame.Vector2,
               ball_speed: pygame.Vector2,
               pad_speed_y: float):

        relative_speed = ball_speed.copy()
        relative_speed.y -= pad_speed_y
        percentage_y = relative_speed.y / relative_speed.magnitude()

        speed_mult = relative_speed.magnitude() / 50

        number_of_particles = round(10*speed_mult)

        for i in range(number_of_particles):
            particle_mult = speed_mult * random.randint(200, 1000) / 1000

            vx_dir = math.copysign(1, relative_speed.x)
            vy_dir = percentage_y + random.gauss(0, 0.3)
            vy_sign = -math.copysign(1, vy_dir)


            particle_speed = pygame.Vector2(0, 0)
            particle_speed.x = random.randint(50, round(200 * particle_mult)) / 10 * vx_dir
            particle_speed.y = (40 + random.gauss(0, 1500)/100 * vy_dir) * particle_mult * vy_sign

            particle_size = random.randint(round(20 * particle_mult), round(50 * particle_mult)) / 40
            particle_lifetime = random.randint(round(50 * particle_mult), round(100 * particle_mult)) / 1000

            BallPadBounce(point, particle_speed, particle_size, 0.005, particle_lifetime)

    def draw(self, surface):
        ratio = ((self.current_ratio-1)*-1)**0.5
        size = int(self.base_size*ratio)
        if size < 1:
            size = 1
        ellipse_rect = pygame.Rect(0, 0, size, size)
        ellipse_rect.center = self.x, self.y
        pygame.draw.ellipse(surface, (255, 255, 255), ellipse_rect)
