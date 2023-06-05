import pygame
import random
import time


from src.engine.handlers.resource_handler import ResourceHandler

from src.objects.particles.ball_bounce_dust import BallBounceDust
from src.objects.effects.screen_shake import ScreenShake
from src.objects.particles.ball_speed_particle import BallSpeedParticle
from src.objects.particles.ball_goal_explosion import BallGoalExplosion
from src.objects.particles.ball_pad_bounce import BallPadBounce
from src.engine.sound.synth import Synth


class Ball:
    BALLS = []
    BALLS_TO_DESTROY = set()

    INITIAL_SPEED = 150
    MAX_SPEED = 450
    DELTA_SPEED = MAX_SPEED - INITIAL_SPEED

    TIME_TO_MAX_SPEED = 20
    MAX_PLAYER_INDUCED_MULT = 2
    MAX_INDUCED_MULT_SPEED = 500        # pad speed required to have max speed mult on ball
    GOAL_SOUNDS = {}

    def __init__(self, linked_arena, position=None, speed=None):
        self.linked_arena = linked_arena
        self.spawn_time = time.time()

        self.x, self.y, self.vx, self.vy = self.create_new(position, speed)
        self.current_speed_mult = 1

        self.ax, self.ay = 0, 0

        self.radius = 5

        self.rect = pygame.Rect(0, 0, self.radius*2, self.radius*2)
        self.rect.center = self.x, self.y

        self.true_ball = True

        self.BALLS.append(self)
        self.linked_arena.balls.append(self)

        self.frequency = 110 * 2 ** (1/12)
        self.duration = 0.5

    def create_bounce_sound(self):
        self.frequency *= 2**(1/12)

        saw = Synth.saw(10000, self.frequency, self.duration)
        square = Synth.square(10000, self.frequency / 2, self.duration)
        noise = Synth.noise(10000, self.duration)
        fo = Synth.fadeout(self.duration)
        new_sound = (square * fo ** 2 + saw + noise * fo) * fo
        sound = Synth.create_pygame_sound(new_sound)
        sound.set_volume(0.4)
        sound.play()

    def goal(self, side=None):
        if not self.true_ball:
            self.destroy()
            return

        if side is None:
            side = int(self.x < 200)

        # Add score
        self.linked_arena.score.add_score(side, self.speed)

        # Add effects
        BallGoalExplosion.create(pygame.Vector2(self.x, self.y), pygame.Vector2(self.vx, self.vy))

        # Clear arena
        self.destroy_all()

        # Play sound
        if self.speed < 250:
            print(ResourceHandler.SOUND)
            ResourceHandler.SOUND["explosion"][random.choice([i for i in ResourceHandler.SOUND["explosion"] if "weak" in i])].play()

        if self.speed > 500:
            ResourceHandler.SOUND["explosion"][random.choice([i for i in ResourceHandler.SOUND["explosion"] if "big" in i])].play()

        else:
            ResourceHandler.SOUND["explosion"][random.choice([i for i in ResourceHandler.SOUND["explosion"] if "medium" in i])].play()

    def create_new(self, position=None, speed=None):
        if position is None:
            position = (200, 150)

        if speed is None:
            speed = pygame.math.Vector2(self.INITIAL_SPEED, 0)
            speed.rotate_ip(random.randint(-45, 45))
            if random.randint(0, 1):
                speed.rotate_ip(180)

        return position[0], position[1], speed[0], speed[1]

    @property
    def speed(self):
        return pygame.Vector2(self.vx, self.vy).magnitude()

    def update_speed(self):
        progression = min(max((time.time() - self.spawn_time), 0), self.TIME_TO_MAX_SPEED)/self.TIME_TO_MAX_SPEED
        current_speed = (self.INITIAL_SPEED + progression * self.DELTA_SPEED) * self.current_speed_mult

        speed_vec = pygame.Vector2(self.vx, self.vy)
        speed_vec.scale_to_length(current_speed)
        self.vx = speed_vec.x
        self.vy = speed_vec.y

    def update_pos(self, delta):
        self.x += self.vx * delta
        self.y += self.vy * delta

    def update_rect(self):
        self.rect.center = self.x, self.y

    def check_collision_arena(self):
        if self.rect.top < self.linked_arena.rect.top:
            self.rect.top = self.linked_arena.rect.top
            self.y = self.rect.centery
            self.vy = abs(self.vy)
            BallBounceDust.create((self.rect.centerx, self.rect.top), self, quantity=None)
            ScreenShake.create(self.speed/50)
            self.create_bounce_sound()

        if self.rect.bottom > self.linked_arena.rect.bottom:
            self.rect.bottom = self.linked_arena.rect.bottom
            self.y = self.rect.centery
            self.vy = abs(self.vy) * -1
            BallBounceDust.create((self.rect.centerx, self.rect.bottom), self, quantity=None)
            ScreenShake.create(self.speed/50)
            self.create_bounce_sound()

    def check_player_loss(self):
        if self.rect.right < self.linked_arena.rect.left or self.rect.left > self.linked_arena.rect.right:
            self.goal()

    def check_collision_pads(self):
        for pad in self.linked_arena.pads:
            if not self.rect.colliderect(pad.rect):
                continue

            pity = 0.02

            # switch to relative speed
            dvx = self.vx
            dvy = self.vy - pad.vy

            # determine nearest hor and ver side (default to bottom-right ball and top-left pad)
            x_ball = self.rect.right
            y_ball = self.rect.bottom
            x_pad = pad.rect.left
            y_pad = pad.rect.top
            x_default = True
            y_default = True

            if abs(self.rect.left-pad.rect.right) < abs(x_ball-x_pad):
                x_ball = self.rect.left
                x_pad = pad.rect.right
                x_default = False

            if abs(self.rect.top-pad.rect.bottom) < abs(y_ball-y_pad):
                y_ball = self.rect.top
                y_pad = pad.rect.bottom
                y_default = False

            dx = abs(x_ball - x_pad)
            dy = abs(y_ball - y_pad)

            dt_x = 512
            dt_y = 512
            if dvx != 0:
                dt_x = dx / abs(dvx)
            if dvy != 0:
                dt_y = dy / abs(dvy)

            if dt_x < dt_y+pity:
                self.bounce_x(pad, x_default)
                pad.animate(-self.vx)
                BallPadBounce.create(pygame.Vector2(x_ball, self.y), pygame.Vector2(self.vx, self.vy), pad.vy)
                self.create_bounce_sound()

            else:
                self.bounce_y(pad, y_default)
                self.create_bounce_sound()

    def bounce_x(self, pad, x_default):
        dvy = self.vy - pad.vy

        if x_default:
            x_ball = self.rect.right
            x_pad = pad.rect.left
            dx = abs(x_ball - x_pad)

            self.rect.right = x_pad - dx

        else:
            x_ball = self.rect.left
            x_pad = pad.rect.right
            dx = abs(x_ball - x_pad)
            self.rect.left = x_pad + dx

        self.x = self.rect.centerx
        max_mult_percentage = min(abs(pad.vy), self.MAX_INDUCED_MULT_SPEED)/self.MAX_INDUCED_MULT_SPEED
        self.current_speed_mult = 1 + max_mult_percentage * (self.MAX_PLAYER_INDUCED_MULT-1)

        self.vy = self.vy / 2 - dvy / 2
        self.vx *= -1

    def bounce_y(self, pad, y_default):
        dvy = self.vy - pad.vy

        if y_default:
            y_ball = self.rect.bottom
            y_pad = pad.rect.top
            dy = abs(y_ball - y_pad)

            self.rect.bottom = y_pad - dy
            self.check_collision_arena()
            if self.rect.colliderect(pad.rect):
                pad.rect.top = self.rect.bottom
                pad.y = pad.rect.centery

        else:
            y_ball = self.rect.top
            y_pad = pad.rect.bottom
            dy = abs(y_ball - y_pad)

            self.rect.top = y_pad + dy
            self.check_collision_arena()
            if self.rect.colliderect(pad.rect):
                pad.rect.bottom = self.rect.top
                pad.y = pad.rect.centery

        self.y = self.rect.centery
        self.vy = -dvy / 2
        pad.vy = dvy / 2

    def generate_particles(self, delta):
        if self.speed < self.linked_arena.score.BIG_SCORE_MIN_SPEED:
            return

        chance = 100 * delta

        if random.random() < chance:
            BallSpeedParticle((self.x, self.y), (self.vx, self.vy))

    @classmethod
    def destroy_all(cls):
        for ball in cls.BALLS:
            ball.destroy()

    def destroy(self):
        self.BALLS_TO_DESTROY.add(self)

    @classmethod
    def update(cls, delta, steps=1):
        for ball in cls.BALLS:
            ball.update_speed()
            ball.generate_particles(delta)

            for i in range(steps):
                ball.update_pos(delta/steps)
                ball.update_rect()
                ball.check_collision_arena()
                ball.check_player_loss()
                ball.check_collision_pads()

                if ball in cls.BALLS_TO_DESTROY:
                    break

        for ball in cls.BALLS_TO_DESTROY:
            cls.BALLS.remove(ball)
            ball.linked_arena.balls.remove(ball)
        cls.BALLS_TO_DESTROY.clear()

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), self.rect.center, self.radius+2)
        pygame.draw.circle(surface, (255, 255, 255), self.rect.center, self.radius)

    @classmethod
    def draw_all(cls, surface):
        for ball in cls.BALLS:
            ball.draw(surface)
