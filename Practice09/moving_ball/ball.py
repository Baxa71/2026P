import pygame


class Ball:
    def __init__(self, w: int = 600, h: int = 600):
        self.w = w
        self.h = h
        self.rad = 25
        self.step = 20
        self.x = w // 2
        self.y = h // 2
        self.col = (220, 30, 30)

    def move(self, dx: int, dy: int):
        nx = self.x + dx * self.step
        ny = self.y + dy * self.step
        if self.rad <= nx <= self.w - self.rad and self.rad <= ny <= self.h - self.rad:
            self.x = nx
            self.y = ny

    def draw(self, surf: pygame.Surface):
        pygame.draw.circle(surf, self.col, (self.x, self.y), self.rad)