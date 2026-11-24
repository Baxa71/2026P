import datetime
from pathlib import Path
import pygame


class MickeyClock:
    def __init__(self, w: int = 600, h: int = 600):
        self.w = w
        self.h = h
        self.ctr = pygame.math.Vector2(w // 2, h // 2)
        self.rad = min(w, h) // 2 - 20
        self.fnt_dig = pygame.font.SysFont("Consolas", 26, bold=True)

        path = Path(__file__).resolve().parent / "images" / "mickey_hand.png"
        raw = pygame.image.load(str(path)).convert_alpha()
        self.bg = pygame.transform.smoothscale(raw, (w, h))

    def _draw_hand(self, surf: pygame.Surface, deg: float, length: float, width: int, color: tuple):
        vec = pygame.math.Vector2(0, -1).rotate(deg)
        end = self.ctr + vec * length
        pygame.draw.line(surf, color, self.ctr, end, width)
        pygame.draw.circle(surf, color, (int(end.x), int(end.y)), width // 2 + 2)

    def draw(self, surf: pygame.Surface):
        now = datetime.datetime.now()
        surf.blit(self.bg, (0, 0))

        self._draw_hand(surf, now.minute * 6, self.rad * 0.62, 8, (20, 20, 20))
        self._draw_hand(surf, now.second * 6, self.rad * 0.78, 4, (210, 35, 35))
        pygame.draw.circle(surf, (210, 35, 35), self.ctr, 10)

        txt = self.fnt_dig.render(f"{now.minute:02d}:{now.second:02d}", True, (255, 255, 255))
        rect = txt.get_rect(center=(int(self.ctr.x), int(self.ctr.y + 115)))
        pygame.draw.rect(surf, (40, 40, 40), rect.inflate(20, 10), border_radius=8)
        surf.blit(txt, rect)