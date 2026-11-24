import pygame
from player import MusicPlayer


def main():
    pygame.init()
    pygame.mixer.init()

    scr = pygame.display.set_mode((620, 300))
    pygame.display.set_caption("Music Player")

    plr = MusicPlayer(620, 300)
    fps = pygame.time.Clock()

    run = True
    while run:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                run = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_p:
                    plr.play()
                elif ev.key == pygame.K_SPACE:
                    plr.toggle_pause()
                elif ev.key == pygame.K_s:
                    plr.stop()
                elif ev.key == pygame.K_x:
                    plr.seek(-5)
                elif ev.key == pygame.K_c:
                    plr.seek(5)
                elif ev.key == pygame.K_n:
                    plr.next_trk()
                elif ev.key == pygame.K_b:
                    plr.prev_trk()
                elif ev.key in (pygame.K_q, pygame.K_ESCAPE):
                    run = False

        plr.update()
        plr.draw(scr)
        pygame.display.flip()
        fps.tick(30)

    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()