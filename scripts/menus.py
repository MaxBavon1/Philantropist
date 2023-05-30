from abc import ABC, abstractmethod
from pygame.locals import *
import pygame


__all__ = ["Menu"]


class Menu(ABC):

    window = None
    clock = None
    data = None
    assets = None

    def __init__(self, bg=(135, 135, 135), FPS=90):
        self.background = bg
        self.FPS = FPS
        self.mousePos = pygame.Vector2(pygame.mouse.get_pos())
        self.running = True

    @classmethod
    def init(cls, window, clock, data, assets):
        cls.window = window
        cls.clock = clock
        cls.data = data
        cls.assets = assets

    def _events(self):
        # --- Touch Keys ---
        for event in pygame.event.get():
            if event.type == QUIT:
               pygame.quit()
               exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
            self.events(event)

    @staticmethod
    def events(self, event):
        pass

    def run(self):
        self.running = True
        while self.running:
            self._events()

            self.clock.tick(self.FPS)
            self.mousePos = pygame.Vector2(pygame.mouse.get_pos())
            self.update()

            self.window.fill(self.background)
            self.render()
            pygame.display.update()

    def quit(self):
        self.running = False

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass
