import pygame
from ball import Ball


def main():
    pygame.init()
    w, h = 600, 600
    scr = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Moving Ball")

    ball = Ball(w, h)
    fps = pygame.time.Clock()

    run = True
    while run:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                run = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    ball.move(0, -1)
                elif ev.key == pygame.K_DOWN:
                    ball.move(0, 1)
                elif ev.key == pygame.K_LEFT:
                    ball.move(-1, 0)
                elif ev.key == pygame.K_RIGHT:
                    ball.move(1, 0)
                elif ev.key == pygame.K_ESCAPE:
                    run = False

        scr.fill((255, 255, 255))
        ball.draw(scr)
        pygame.display.flip()
        fps.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()