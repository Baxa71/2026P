import pygame
from clock import MickeyClock


def main():
    pygame.init()
    scr = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Mickey's Clock")

    clk = MickeyClock(600, 600)
    fps = pygame.time.Clock()
    tick = pygame.USEREVENT + 1
    pygame.time.set_timer(tick, 1000)

    clk.draw(scr)
    pygame.display.flip()

    run = True
    while run:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                run = False
            elif ev.type == tick:
                clk.draw(scr)
                pygame.display.flip()
        fps.tick(30)

    pygame.quit()
if __name__ == "__main__":
    main()