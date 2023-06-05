import pygame
import random

from src.objects.particles.particle import Particle
from src.objects.effects.screen_shake import ScreenShake


class BallGoalExplosion(Particle):
    @classmethod
    def create(cls, ball_position: pygame.Vector2, ball_speed: pygame.Vector2):
        speed = ball_speed.magnitude()
        number_of_particles = round(ball_speed.magnitude()*3)

        ScreenShake.create(speed/10, lifetime=speed/200)

        for i in range(number_of_particles):
            particle_multiplier = random.gauss(1, 0.23)
            if particle_multiplier > 1:
                particle_multiplier = particle_multiplier * -1 + 2

            particle_multiplier += random.randint(-10, 10)/100
            particle_speed = pygame.Vector2(speed * particle_multiplier * 2, 0).rotate(random.randint(0, 360))
            particle_size = random.randint(round(speed/50), round(speed/20))
            particle_lifetime = random.randint(10, 20)/10

            BallGoalExplosion(ball_position, particle_speed, particle_size, 0.02, particle_lifetime)

    @classmethod
    def update(cls, delta):
        super().update(delta)

    def draw(self, surface):
        ratio = ((self.current_ratio-1)*-1)**0.5
        size = int(self.base_size*ratio)
        if size < 1:
            size = 1
        ellipse_rect = pygame.Rect(0, 0, size, size)
        ellipse_rect.center = self.x, self.y
        pygame.draw.ellipse(surface, (255, 255, 255), ellipse_rect)
