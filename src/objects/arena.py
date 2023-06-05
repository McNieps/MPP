import pygame

from src.objects.pad import Pad
from src.objects.score.score import Score
from src.objects.ball import Ball
from src.objects.ball_launcher import BallLauncher


class Arena:
    LINE_WIDTH = 2

    def __init__(self, outer_size=(398, 298), inner_size=(386, 286), center=(200, 150)):
        self.center = center

        self.rect = pygame.Rect(0, 0, *inner_size)  # is inner rect
        self.outer_rect = pygame.Rect(0, 0, *outer_size)

        self.rect.center = center
        self.outer_rect.center = center
        self.separator_width = -1

        self.ball_launcher = BallLauncher(self)
        self.balls = []
        self.pads = [Pad(i, self) for i in range(2)]

        self.score = Score()
        self.score_was_animating = False

        self.ball_launcher.launch()

    def update(self, delta):
        if not self.score.animation and self.score_was_animating:
            self.ball_launcher.launch()

        self.ball_launcher.update(delta)
        self.score_was_animating = self.score.animation

    def draw_borders(self, surface):
        inner_rect_outline = self.rect.copy().inflate(2*self.LINE_WIDTH, 2*self.LINE_WIDTH)

        rect_width = inner_rect_outline.width / 2 - self.separator_width//2

        left_inner_rect = inner_rect_outline.copy()
        right_inner_rect = inner_rect_outline.copy()

        left_inner_rect.width = rect_width
        right_inner_rect.width = rect_width

        left_inner_rect.left = inner_rect_outline.left
        right_inner_rect.right = inner_rect_outline.right

        black_band_rect = pygame.Rect(0, 0, 0, left_inner_rect.height)
        black_band_rect.width = right_inner_rect.left + 2 - (left_inner_rect.right - 2)
        black_band_rect.center = self.center

        pygame.draw.rect(surface, (0, 0, 0), self.outer_rect, 6)
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, 400, 300), 2)
        pygame.draw.rect(surface, (255, 255, 255), self.outer_rect, self.LINE_WIDTH, 5, 5, 5, 5)
        pygame.draw.rect(surface, (0, 0, 0, 0), black_band_rect)
        pygame.draw.rect(surface, (255, 255, 255), left_inner_rect, self.LINE_WIDTH, 5, 5, 5, 5)
        pygame.draw.rect(surface, (255, 255, 255), right_inner_rect, self.LINE_WIDTH, 5, 5, 5, 5)

    def draw(self, surface):
        self.draw_borders(surface)
        self.score.render(surface)
        self.ball_launcher.render(surface)
