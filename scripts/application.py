from pygame.locals import *
import pygame
import time
import json

from .data import *
from .assets import *
from .ui import *
from .menus import *
from .game import *


__all__ = ["Launch", "Quit"]


# _____ Application Configurations  ____
pygame.init()
pygame.mixer.init()
DEFAULT_W, DEFAULT_H = 1920, 1080
# MONITO_SIZE = pygame.display.Info().current_w, pygame.display.Info().current_h
window = pygame.display.set_mode((0, 0), DOUBLEBUF | FULLSCREEN, vsync=1)
MONITO_SIZE = window.get_size()
RESIZING = MONITO_SIZE[0] / DEFAULT_W, MONITO_SIZE[1] / DEFAULT_H
print("MONITOR :", MONITO_SIZE)
pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
clock = pygame.time.Clock()
FPS = 90

# Assets Game Loading
pygame.mixer.music.load("assets/music/game_music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(99)
loading_img = pygame.image.load("assets/ui/loading.jpg").convert()
loading_img = pygame.transform.scale(loading_img, MONITO_SIZE)
window.blit(loading_img, (0, 0))
pygame.display.update()

time.sleep(0) # Prentending loading the game assets takes time...
assets = Assets()
w, h = assets.sprites["forest_bg"].get_size()
assets.sprites["forest_bg"] = pygame.transform.scale(assets.sprites["forest_bg"], (w * 2, h * 2))
w, h = assets.sprites["snow_bg"].get_size()
assets.sprites["snow_bg"] = pygame.transform.scale(assets.sprites["snow_bg"], (w * 4, h * 4))
w, h = assets.sprites["lava_bg"].get_size()
assets.sprites["lava_bg"] = pygame.transform.scale(assets.sprites["lava_bg"], (w * 2, h * 2))
assets.sprites["backgroundfinal2"] = pygame.transform.scale(assets.sprites["backgroundfinal2"], MONITO_SIZE)
assets.ui["volume_on"] = pygame.transform.scale_by(assets.ui["volume_on"], 3)
assets.ui["volume_off"] = pygame.transform.scale_by(assets.ui["volume_off"], 3)
data = Data()
data.load_progress()
data.load_game_data()
Menu.init(window, clock, data, assets)

def Launch():
    MainMenu().run()

def Quit():
    pygame.quit()
    exit()



class Rules(Menu):

    def __init__(self, main, *args, **kargs):
        super().__init__(*args, **kargs)
        self.main = main
        self.UIManager = UIManager()
        
        title = Label((MONITO_SIZE[0] / 2, 200 * RESIZING[1]), assets.fonts["rubik80"], "Rules", COLORS["purple"])
        mouvement = Label((MONITO_SIZE[0] / 2, 400 * RESIZING[1]), assets.fonts["rubik40"], "Press Q/D or Left Arrow/Right Arrow to Move", COLORS["blue"])
        jump = Label((MONITO_SIZE[0] / 2, 500 * RESIZING[1]), assets.fonts["rubik40"], "Press space of Arrow Up to Jump", COLORS["blue"])
        shoot = Label((MONITO_SIZE[0] / 2, 600 * RESIZING[1]), assets.fonts["rubik40"], "Aim and press Left Mouse to Shoot", COLORS["blue"])
        god_mod = Label((MONITO_SIZE[0] / 2, 700 * RESIZING[1]), assets.fonts["rubik40"], "God Mode : press shift to fly and Tab to shoot infinite bullets", COLORS["blue"])
        debug = Label((MONITO_SIZE[0] / 2, 800 * RESIZING[1]), assets.fonts["rubik40"], "Press F3 to debug", COLORS["blue"])

        quit_but = Button((MONITO_SIZE[0] / 2, 900 * RESIZING[1]), (250, 100), assets.fonts["rubik40"], "Main Menu", command=self.quit)
        self.UIManager.adds(title, mouvement, jump, shoot, god_mod, debug, quit_but)

    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.UIManager.clicked(self.mousePos)

    def update(self):
        self.UIManager.update(pygame.Vector2(pygame.mouse.get_pos()))

    def render(self):
        self.UIManager.render(self.window)


class Settings(Menu):

    def __init__(self, main, *args, **kargs):
        super().__init__(*args, **kargs)
        self.main = main
        self.UIManager = UIManager()
    
        title = Label((MONITO_SIZE[0] / 2, 200 * RESIZING[1]), assets.fonts["rubik80"], "Settings", COLORS["white"])
        sound_on = ButtonImg((MONITO_SIZE[0] / 2, 400 * RESIZING[1]), assets.ui["volume_on"], COLORS["white"], command=pygame.mixer.music.unpause)
        sound_off = ButtonImg((MONITO_SIZE[0] / 2, 600 * RESIZING[1]), assets.ui["volume_off"], COLORS["white"], command=pygame.mixer.music.pause)
        quit_but = Button((MONITO_SIZE[0] / 2, 800 * RESIZING[1]), (250, 100), assets.fonts["rubik40"], "Main Menu", command=self.quit)
        self.UIManager.adds(title, sound_on, sound_off, quit_but)

    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.UIManager.clicked(self.mousePos)

    def update(self):
        self.UIManager.update(pygame.Vector2(pygame.mouse.get_pos()))

    def render(self):
        self.UIManager.render(self.window)



class Credits(Menu):

    def __init__(self, main, *args, **kargs):
        super().__init__(*args, **kargs)
        self.main = main
        self.UIManager = UIManager()
        
        made = Label((MONITO_SIZE[0] / 2, 200 * RESIZING[1]), assets.fonts["rubik80"], "Made By : ", COLORS["white"])
        creators1 = Label((MONITO_SIZE[0] / 2, 300 * RESIZING[1]), assets.fonts["rubik40"], "Maxime Etienne", COLORS["purple"])
        creators2 = Label((MONITO_SIZE[0] / 2, 350 * RESIZING[1]), assets.fonts["rubik40"], "Alexandre Kalaydjian", COLORS["purple"])
        creators3 = Label((MONITO_SIZE[0] / 2, 400 * RESIZING[1]), assets.fonts["rubik40"], "Lilou Becker", COLORS["purple"])
        creators4 = Label((MONITO_SIZE[0] / 2, 450 * RESIZING[1]), assets.fonts["rubik40"], "Nawal Moulouad ", COLORS["purple"])
        creators5 = Label((MONITO_SIZE[0] / 2, 500 * RESIZING[1]), assets.fonts["rubik40"], "Sami Frydman", COLORS["purple"])
        quit_but = Button((MONITO_SIZE[0] / 2, 700 * RESIZING[1]), (250, 100), assets.fonts["rubik40"], "Main Menu", command=self.quit)
        self.UIManager.adds(made, creators1, creators2, creators3, creators4, creators5, quit_but)

    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.UIManager.clicked(self.mousePos)

    def update(self):
        self.UIManager.update(pygame.Vector2(pygame.mouse.get_pos()))

    def render(self):
        self.UIManager.render(self.window)


class Levels(Menu):

    def __init__(self, main, *args, **kargs):
        super().__init__(*args, **kargs)
        self.main = main
        self.UIManager = UIManager()
        
        levels_label = ButtonLabel((MONITO_SIZE[0] / 2, 250 * RESIZING[1]), assets.fonts["rubik80"], "Levels", COLORS["blue"], COLORS["blue"])
        level1_label = ButtonLabel((MONITO_SIZE[0] / 2, 450 * RESIZING[1]), assets.fonts["rubik40"], "Level 1", COLORS["blue"], COLORS["green"], command=lambda:self.load_level(1))
        level2_label = ButtonLabel((MONITO_SIZE[0] / 2, 550 * RESIZING[1]), assets.fonts["rubik40"], "Level 2", COLORS["blue"], COLORS["green"], command=lambda:self.load_level(2))
        level3_label = ButtonLabel((MONITO_SIZE[0] / 2, 650 * RESIZING[1]), assets.fonts["rubik40"], "Level 3", COLORS["blue"], COLORS["green"], command=lambda:self.load_level(3))
        quit_but = Button((MONITO_SIZE[0] / 2, 800 * RESIZING[1]), (250, 100), assets.fonts["rubik40"], "Main Menu", command=self.quit)
        self.UIManager.adds(quit_but, levels_label, level1_label, level2_label, level3_label)

    def load_level(self, lvl):
        if lvl == 1 or data.progress[f"level {lvl - 1}"]:
            self.main.load_menu("game", lvl)

    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.UIManager.clicked(self.mousePos)

    def update(self):
        self.UIManager.update(pygame.Vector2(pygame.mouse.get_pos()))

    def render(self):
        self.UIManager.render(self.window)
    
    def run(self):
        self.UIManager.objects = []
        for i in range(1, data.progress["nb_levels"]):
            button = self.UIManager.buttons[i + 2]
            if (not data.progress[f"level {i}"]):
                self.UIManager.add(Image((button.rect.x - 25, button.rect.centery), assets.ui["lock"]))
                button.hover_color = COLORS["red"]
            else:
                button.hover_color = COLORS["green"]
        super().run()


class MainMenu(Menu):

    def __init__(self):
        super().__init__(COLORS["grey"], FPS)

        self.UIManager = UIManager()

        title = Label((MONITO_SIZE[0] / 2, 100 * RESIZING[1]), assets.fonts["rubik80"], "PHILANTROPIST", COLORS["purple"])
        play_but = Button((MONITO_SIZE[0] / 2, 300 * RESIZING[1]), (275, 100), assets.fonts["rubik60"], "Play", command=lambda:self.load_menu("levels", 1))
        rules_but = ButtonLabel((MONITO_SIZE[0] / 2, 500 * RESIZING[1]), assets.fonts["rubik60"], "Rules", COLORS["cyan"], COLORS["purple"], lambda:self.load_menu("rules"))
        settings_but = ButtonLabel((MONITO_SIZE[0] / 2, 600 * RESIZING[1]), assets.fonts["rubik60"], "Settings", COLORS["cyan"], COLORS["purple"], lambda:self.load_menu("settings"))
        credits_but = ButtonLabel((MONITO_SIZE[0] / 2, 700 * RESIZING[1]), assets.fonts["rubik60"], "Credits", COLORS["cyan"], COLORS["purple"], lambda:self.load_menu("credits"))
        quit_but = ButtonLabel((MONITO_SIZE[0] / 2, 800 * RESIZING[1]), assets.fonts["rubik60"], "Quit", COLORS["cyan"], COLORS["purple"], command=Quit)

        self.UIManager.adds(title, play_but, rules_but, settings_but, credits_but, quit_but)


        self.menus = {
            "rules" : Rules(self, COLORS["white"], 90),
            "settings" : Settings(self, COLORS["black"], 90),
            "credits" : Credits(self, COLORS["black"], 90),
            "levels" : Levels(self, COLORS["white"], 90),
            "game" : GameManager(COLORS["blue"], 144)
        }
        self.currentMenu = ""

    def load_menu(self, menu, lvl=0):
        if self.currentMenu and self.menus[self.currentMenu].running:
            self.menus[self.currentMenu].quit()

        self.currentMenu = menu
        if menu != "game":

            self.menus[menu].run()
        else:
            self.menus[menu].run(lvl)

    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.UIManager.clicked(self.mousePos)

    def update(self):
        self.UIManager.update(self.mousePos)

    def render(self):
        self.window.blit(assets.sprites["backgroundfinal2"], (0, 0))
        self.UIManager.render(self.window)