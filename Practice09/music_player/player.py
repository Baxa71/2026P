from pathlib import Path
import pygame


class MusicPlayer:
    def __init__(self, w: int = 620, h: int = 300):
        self.w = w
        self.h = h
        self.f_lg = pygame.font.SysFont("Arial", 24, bold=True)
        self.f_md = pygame.font.SysFont("Arial", 18)
        self.f_sm = pygame.font.SysFont("Consolas", 15)

        base = Path(__file__).resolve().parent / "music"
        self.trks = [
            base / "haggstrom.mp3",
            base / "MEGALOVANIA.mp3",
        ]
        self.idx = 0
        self.stat = "STOPPED"
        self.dur = 0.0
        self.off = 0.0

    def _load(self):
        trk = self.trks[self.idx]
        pygame.mixer.music.load(str(trk))
        self.dur = pygame.mixer.Sound(str(trk)).get_length()
        self.off = 0.0

    def _pos(self) -> float:
        if self.stat == "PLAYING":
            ms = pygame.mixer.music.get_pos()
            cur = self.off + (ms / 1000.0 if ms > 0 else 0.0)
            return min(cur, self.dur) if self.dur > 0 else cur
        if self.stat == "PAUSED":
            return self.off
        return 0.0

    def play(self):
        if self.stat == "STOPPED":
            self._load()
            pygame.mixer.music.play()
        elif self.stat == "PAUSED":
            pygame.mixer.music.play(start=self.off)
        self.stat = "PLAYING"

    def toggle_pause(self):
        if self.stat == "PLAYING":
            self.off = self._pos()
            pygame.mixer.music.pause()
            self.stat = "PAUSED"
        elif self.stat == "PAUSED":
            pygame.mixer.music.play(start=self.off)
            self.stat = "PLAYING"

    def seek(self, sec: float):
        if self.stat == "STOPPED":
            return
        nxt = max(0.0, self._pos() + sec)
        if self.dur > 0 and nxt >= self.dur:
            self.next_trk()
            return
        self.off = nxt
        if self.stat == "PLAYING":
            pygame.mixer.music.play(start=self.off)

    def stop(self):
        pygame.mixer.music.stop()
        self.off = 0.0
        self.stat = "STOPPED"

    def next_trk(self):
        self.idx = (self.idx + 1) % len(self.trks)
        self.stat = "STOPPED"
        self.play()

    def prev_trk(self):
        self.idx = (self.idx - 1) % len(self.trks)
        self.stat = "STOPPED"
        self.play()

    def update(self):
        if self.stat == "PLAYING" and not pygame.mixer.music.get_busy():
            self.next_trk()

    @staticmethod
    def _fmt(sec: float) -> str:
        s = max(0, int(sec))
        return f"{s // 60:02d}:{s % 60:02d}"

    def draw(self, surf: pygame.Surface):
        surf.fill((28, 30, 38))
        trk = self.trks[self.idx]

        info = f"Track {self.idx + 1}/{len(self.trks)}  |  {self.stat}"
        surf.blit(self.f_md.render(info, True, (160, 175, 200)), (30, 35))
        surf.blit(self.f_lg.render(trk.name, True, (95, 210, 150)), (30, 75))

        elap = self._pos()
        rat = elap / self.dur if self.dur > 0 else 0.0

        bx, by, bw, bh = 30, 130, self.w - 60, 14
        pygame.draw.rect(surf, (55, 60, 75), (bx, by, bw, bh), border_radius=7)
        if rat > 0:
            pygame.draw.rect(surf, (95, 210, 150), (bx, by, int(bw * rat), bh), border_radius=7)

        t_str = f"{self._fmt(elap)} / {self._fmt(self.dur)}"
        surf.blit(self.f_sm.render(t_str, True, (210, 215, 225)), (30, 155))

        keys = "[P] Play  [S] Stop  [N] Next  [B] Back  [Q] Quit"
        surf.blit(self.f_sm.render(keys, True, (145, 155, 175)), (30, self.h - 45))