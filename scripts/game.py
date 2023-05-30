import pygame
import time
from pygame.locals import *

from .level import *
from .camera import *
from .entityManager import *
from .ui import *
from .menus import *


__all__ = ["GameManager"]


class GameManager(Menu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ==== Window ====
        self.WIDTH, self.HEIGHT = self.window.get_size()

        self.currentFps = 0
        self.deltaTime = 0
        self.lastFrame = 0
        self.debugMode = False
        self.fixedUpdate = False
        self.mousePos = pygame.Vector2(pygame.mouse.get_pos())

        self.level = Level(self)
        self.entityManager = EntityManager(self)
        self.camera = Camera(self)

        # ---- UI ----
        self.paused = False
        self.UIManager = UIManager()    
        resume_but = Button((self.WIDTH / 2, 350), (250, 100), self.assets.fonts["rubik40"], "Resume", command=self.unpause)
        retry_but = Button((self.WIDTH / 2, 500), (250, 100), self.assets.fonts["rubik40"], "Retry", command=lambda:self.load_level(self.level.level))
        quit_but = Button((self.WIDTH / 2, 650), (250, 100), self.assets.fonts["rubik40"], "Main Menu", command=lambda:self.quit(True))
        self.UIManager.adds(retry_but, resume_but, quit_but)

        self.deathMenu = Death(self)
        self.winMenu = Win(self)

    def unpause(self):
        self.paused = not self.paused
        pygame.mouse.set_visible(self.paused)

    def load_level(self, lvl):
        """ Game Loading Datas, Entities, Levels """
        self.paused = False
        self.lastFrame = time.time()
        pygame.mouse.set_visible(False)
        self.gravityScale = 1700

        self.level.load_level(lvl)
        self.entityManager.load_level(self.level.layers["entities"], self.level.layers["objects"])
        self.camera.follow(self.entityManager.player)

    def events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.unpause()
            if not self.paused:
                if event.key == K_F3:
                    self.debugMode = not self.debugMode
                if event.key == K_F5:
                    self.fixedUpdate = not self.fixedUpdate
                if event.key == K_SPACE or event.key == K_UP:
                    if self.entityManager.player.grounded:	
                        self.entityManager.player.jump()
        if event.type == MOUSEBUTTONDOWN and not self.paused:
            if event.button == 1:	
                self.entityManager.player.shoot()
        if event.type == MOUSEBUTTONUP and self.paused:
            if event.button == 1:
                self.UIManager.clicked(self.mousePos)

    def update(self):
        self.deltaTime =  time.time() - self.lastFrame
        if self.fixedUpdate: self.deltaTime = 1 / 144
        self.lastFrame = time.time()
        self.ticks = pygame.time.get_ticks() * 0.001
        self.currentFps = round(self.clock.get_fps())
        self.mousePos = pygame.Vector2(pygame.mouse.get_pos())

        if not self.paused:
            keyboard = pygame.key.get_pressed()
            if keyboard[K_F6]:
                self.FPS -= 1
            if keyboard[K_F7]:
                self.FPS += 1

            self.level.update(self.deltaTime)
            self.entityManager.update(self.deltaTime, self.gravityScale)
            self.camera.update(self.deltaTime)
        else:
            self.UIManager.update(self.mousePos)
    
    def render(self):
        self.level.render(self.window, self.camera)

        self.entityManager.render(self.window, self.camera)

        if self.paused:
            pause_bg = pygame.Surface((self.WIDTH, self.HEIGHT))
            pause_bg.fill((0, 0, 0))
            pause_bg.set_alpha(100)
            self.window.blit(pause_bg, (0, 0))
            self.UIManager.render(self.window)
        else:
 
            if self.debugMode:
                self.render_debug()
            if self.fixedUpdate:
                self.render_update_mode()
            # Cursor
            self.window.blit(self.assets.ui["cursor"], self.mousePos - (pygame.Vector2(self.assets.ui["cursor"].get_size()) / 2))

    def render_text(self, text, pos, font="rubik20"):
        current_font = self.assets.fonts[font]
        surf = current_font.render(text, 1, (255, 255, 255))
        self.window.blit(surf, pos)

    def render_text_debug(self, text, y, font="rubik20"):
        current_font = self.assets.fonts[font]
        surf = current_font.render(text, 1, (255, 255, 255))
        self.window.blit(surf, (self.WIDTH - current_font.size(text)[0], y))

    def render_debug(self):
        fps_txt = f"FPS : {self.currentFps} / MaxFPS : {self.FPS}"
        entity_txt = f"E : {self.entityManager.size}"
        pos_txt = f"X,Y : {round(self.entityManager.player.position.x)} / {round(self.entityManager.player.position.y)}"
        vel_txt = f"Vel : {round(self.entityManager.player.velocity.x)} / {round(self.entityManager.player.velocity.y)}"

        self.render_text_debug(fps_txt, 0)
        self.render_text_debug(entity_txt, 20)
        self.render_text_debug(pos_txt, 40)
        self.render_text_debug(vel_txt, 60)

        self.camera.render_debug(self.window)

    def render_update_mode(self):
        surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        surface.set_alpha(25)
        surface.fill((255, 0, 0))
        self.window.blit(surface, (0, 0))

    def run(self, lvl):
        print("[LAUNCHING GAME...]")

        if lvl <= 3:
            self.load_level(lvl)
            super().run()
        else:
            print("You win !")

    def quit(self, pause=False):
        if pause:
            pygame.mouse.set_visible(True)
            self.running = False
            self.paused = False


class Death(Menu):

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.UIManager = UIManager()
        retry_but = Button((self.game.WIDTH / 2, 400), (250, 100), self.assets.fonts["rubik40"], "Retry", command=self.close)
        quit_but = Button((self.game.WIDTH / 2, 550), (250, 100), self.assets.fonts["rubik40"], "Main Menu", command=self.quit)
        self.UIManager.adds(retry_but, quit_but)

    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.UIManager.clicked(self.mousePos)

    def update(self):
        self.UIManager.update(pygame.Vector2(pygame.mouse.get_pos()))

    def render(self):
        self.window.fill((255, 0, 0))

        self.UIManager.render(self.window)

    def quit(self):
        super().quit()
        self.game.quit(True)
    
    def close(self):
        super().quit()
        self.game.load_level(self.game.level.level)
    
    def run(self):
        pygame.mouse.set_visible(True)
        super().run()


class Win(Menu):

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.UIManager = UIManager()
        self.background = (40, 91, 133)
        win_label = Label((self.game.WIDTH / 2, 200), self.assets.fonts["rubik80"], "Victory !", (250, 241, 72))
        retry_but = Button((self.game.WIDTH / 2, 400), (250, 100), self.assets.fonts["rubik40"], "Retry", command=self.close)
        next_lvl_but = Button((self.game.WIDTH / 2, 550), (250, 100), self.assets.fonts["rubik40"], "Next Level", command=lambda:self.game.run(self.game.level.level+1))
        quit_but = Button((self.game.WIDTH / 2, 700), (250, 100), self.assets.fonts["rubik40"], "Main Menu", command=self.quit)
        self.UIManager.adds(win_label, retry_but, next_lvl_but, quit_but)

    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.UIManager.clicked(self.mousePos)

    def update(self):
        self.UIManager.update(pygame.Vector2(pygame.mouse.get_pos()))

    def render(self):
        self.window.fill(self.background)

        self.UIManager.render(self.window)

    def quit(self):
        super().quit()
        self.game.quit(True)
    
    def close(self):
        super().quit()
        self.game.load_level(self.game.level.level)
    
    def run(self):
        pygame.mouse.set_visible(True)
        super().run()