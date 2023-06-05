import pygame
import time
import math

from src.engine.app import App


class Score:
    BIG_SCORE_MIN_SPEED = 500

    GOAL_TRANSITION_TIME = 0.5
    GOAL_LIFETIME = 2.7

    FLAG_TRANSITION_TIME = 0.5
    FLAG_LIFETIME = 2
    FLAG_MAX_TIME_MIN_MAX = 0.5

    SPACE_BETWEEN_FLAGS = 1
    FLAG_WIDTH = 14

    ASSETS = {}

    def __init__(self, max_score=12):
        self.points: list[list[float]] = [[], []]
        self.bo = max_score

        self.latest_side = 0
        self.latest_speed = 0

        self.load_assets()

        self.animation = False
        self.animation_start_time = 0

    @classmethod
    def load_assets(cls):
        if cls.ASSETS:
            return

        assets_to_load = ["1", "1_plus", "1_round", "1_game", "2", "2_plus", "2_round", "2_game"]
        for i in assets_to_load:
            cls.ASSETS[i] = pygame.image.load(f"{App.ASSETS_PATH}/image/score/{i}.png")

    def add_score(self, side, speed):
        self.points[side].append(speed)
        self.latest_side = side
        self.latest_speed = speed

        print(f"Player {side + 1} score with a ball speed of {round(speed)} pixels per second")
        self.start_animation()

    def start_animation(self):
        self.animation_start_time = time.time()
        self.animation = True

    def render(self, surface):
        if not self.animation:
            return

        if time.time() > self.animation_start_time+self.GOAL_LIFETIME:
            self.animation = False
            return

        self.render_goal(surface)
        for position in range(self.bo-1):
            for side in range(2):
                self.render_score_flag(surface, side, position)

    def render_goal(self, surface):
        goal_assets_name = f"{self.latest_side+1}_{'game' if len(self.points[self.latest_side])>self.bo-1 else 'round'}"
        goal_surf = self.ASSETS[goal_assets_name]
        goal_rect = goal_surf.get_rect()
        goal_rect.centerx = 200
        time_anim = time.time() - self.animation_start_time
        if time_anim < self.GOAL_TRANSITION_TIME:
            coef = time_anim / self.GOAL_TRANSITION_TIME
            goal_rect.top = math.sin(coef * math.pi / 2) * 59 - 59

        elif time_anim < self.GOAL_LIFETIME-self.GOAL_TRANSITION_TIME:
            goal_rect.top = 0

        else:
            coef = (time_anim-self.GOAL_LIFETIME+self.GOAL_TRANSITION_TIME)/self.GOAL_TRANSITION_TIME
            goal_rect.top = 59*math.sin(coef*math.pi/2+math.pi/2)-59

        surface.blit(goal_surf, goal_rect)

    def render_score_flag(self, surface, side, position):
        if len(self.points[side]) - 1 < position:
            return

        strength = 1.25
        spawn_time = self.FLAG_MAX_TIME_MIN_MAX * (position / (self.bo - 1)) ** strength

        time_flag = time.time() - self.animation_start_time - spawn_time

        if time_flag < 0 or time_flag > self.FLAG_LIFETIME:
            return

        flag_surf = self.ASSETS[f"{side+1}{'_plus' if self.points[side][position] > 500 else ''}"]
        position += 1

        flag_rect = pygame.Rect(0, 0, 14, 0)
        position_from_center = (self.bo - 1) - position
        base_dist_from_center = 25 + self.SPACE_BETWEEN_FLAGS + self.FLAG_WIDTH / 2
        dist_from_center = base_dist_from_center + position_from_center * (self.FLAG_WIDTH + self.SPACE_BETWEEN_FLAGS)

        if time_flag < self.FLAG_TRANSITION_TIME:
            coef = time_flag/self.FLAG_TRANSITION_TIME
            flag_rect.top = math.sin(coef*math.pi/2)*32-32

        elif time_flag < self.FLAG_LIFETIME - self.FLAG_TRANSITION_TIME:
            flag_rect.top = 0

        else:
            coef = (time_flag-self.FLAG_LIFETIME+self.FLAG_TRANSITION_TIME)/self.FLAG_TRANSITION_TIME
            flag_rect.top = math.sin(coef*math.pi/2+math.pi/2)*32-32

        if side == 0:
            flag_rect.centerx = 200 - dist_from_center
            surface.blit(flag_surf, flag_rect)

        else:
            flag_rect.centerx = 200 + dist_from_center
            surface.blit(flag_surf, flag_rect)
