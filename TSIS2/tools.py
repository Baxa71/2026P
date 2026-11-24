import math
from collections import deque
import pygame


def draw_shape(surface, tool, color, start, end, width):
    if tool == "pencil" or tool == "line":
        pygame.draw.line(surface, color, start, end, width)
    elif tool == "eraser":
        pygame.draw.line(surface, (255, 255, 255), start, end, width * 2)
    elif tool == "rect":
        x = min(start[0], end[0])
        y = min(start[1], end[1])
        w = abs(end[0] - start[0])
        h = abs(end[1] - start[1])
        if w > 0 and h > 0:
            pygame.draw.rect(surface, color, (x, y, w, h), width)
    elif tool == "square":
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        side = max(abs(dx), abs(dy))
        if side > 0:
            x = start[0] if dx >= 0 else start[0] - side
            y = start[1] if dy >= 0 else start[1] - side
            pygame.draw.rect(surface, color, (x, y, side, side), width)
    elif tool == "circle":
        radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
        if radius > 0:
            pygame.draw.circle(surface, color, start, radius, min(width, radius))


def flood_fill(surface, pos, fill_color):
    x, y = int(pos[0]), int(pos[1])
    w, h = surface.get_size()
    if x < 0 or x >= w or y < 0 or y >= h:
        return

    surface.lock()
    try:
        target_color = tuple(surface.get_at((x, y)))
        replacement = tuple(pygame.Color(*fill_color))
        if target_color == replacement:
            return

        queue = deque([(x, y)])
        visited = {(x, y)}

        while queue:
            cx, cy = queue.popleft()
            surface.set_at((cx, cy), replacement)
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    if tuple(surface.get_at((nx, ny))) == target_color:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
    finally:
        surface.unlock()