import pygame
import time


class Particle:
    PARTICLES = []

    def __init__(self,
                 position,
                 speed,
                 base_size,
                 friction,
                 lifetime):

        self.x, self.y = position
        self.vx, self.vy = speed
        self.base_size = base_size
        self.friction = friction
        self.lifetime = lifetime
        self.start_time = time.time()
        self.current_ratio = 0

        self.PARTICLES.append(self)

    def update_lifetime(self):
        self.current_ratio = (time.time() - self.start_time) / self.lifetime
        return self.current_ratio

    def update_pos(self, delta):
        self.vx = self.vx * self.friction ** delta
        self.vy = self.vy * self.friction ** delta

        self.x += self.vx * delta
        self.y += self.vy * delta

    @classmethod
    def update(cls, delta):
        for i in range(len(cls.PARTICLES)-1, -1, -1):
            if cls.PARTICLES[i].update_lifetime() > 1:
                cls.PARTICLES.pop(i)
                continue

            cls.PARTICLES[i].update_pos(delta)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.base_size)

    @classmethod
    def draw_all(cls, surface):
        for particle in cls.PARTICLES:
            particle.draw(surface)
