import pygame
import os

__all__ = ["Assets", "TILE_SIZE", "PIXEL_RATIO", "COLORS"]

""" Loads all the images, animations, sprites, tilesets etc... Basicaly all pixel art from
the game are loaded with the Assets class, it uses a recursive function to browse throw the assets folder
and load the game assets """

PATH = os.getcwd()
PIXEL_RATIO = 3
PIXEL_UNIT = 16
TILE_SIZE = PIXEL_RATIO * PIXEL_UNIT
# Colors
COLORS = {
    "white" : (255,255,255),
    "black" : (0,0,0),
    "grey" : (135,135,135),
    "blue" : (57,140,204),
    "green" : (64,222,87),
    "red" : (255,0,0),
    "purple" : (171,32,253),
    "brown" : (118,54,46),
    "cyan" : (49,175,212),
    "pink" : (226,40,220)
}


class Assets:

    __slots__ = ["sprites", "tiles", "ui", "fonts"]

    def __init__(self):
        """ Loads all the assets needed to run the game, including all directories
        and files using a recursive method """
        self.sprites = self.load_sprites()
        self.tiles = self.load_tiles()
        self.ui = self.load_ui()
        self.fonts = self.load_fonts()

    def load_image(self, path, size=PIXEL_RATIO, alpha=True):
        surf = pygame.image.load(path)
        surf = pygame.transform.scale(surf, (surf.get_width() * size, surf.get_height() * size))
        surf = surf.convert_alpha() if alpha else surf.convert()
        return surf

    def load_animation(self, path, size=PIXEL_RATIO, alpha=True):
        sheet = self.load_image(path, size, alpha)
        frames = int(path[-5])
        sprite_size = sheet.get_width() // frames
        animation = []
        for x in range(frames):
            animation.append(sheet.subsurface((x * sprite_size, 0, sprite_size, sheet.get_height())))
        return animation

    def load_dir_animations(self, path):
        animations = {}
        for filename in os.listdir(path):
            name = filename[:-5]
            animations[name.replace("_anim", "")] = self.load_animation(os.path.join(path, filename))
        return animations

    def custom_load_sprites(self, path, sprites):
        for directory in os.listdir(path):
            new_path = os.path.join(path + directory)
            if os.path.isdir(new_path): # Load next directory
                if "anim" in directory:
                    sprites[directory] = self.load_dir_animations(os.path.join(new_path))
                else:
                    self.custom_load_sprites(new_path + '/', sprites)
            else: # Load file
                filename = directory[:-4]
                if "anim" in filename:
                    sprites[filename[:-1]] = self.load_animation(new_path)
                else:
                    if "background" in new_path:
                        sprites[filename] = self.load_image(new_path, 1, False)
                    else:
                        sprites[filename] = self.load_image(new_path)
        return sprites

    def load_sprites(self):
        sprites = {}
        path = os.path.join(PATH, "assets/images/")
        self.custom_load_sprites(path, sprites)
        return sprites

    def load_tileset(self, path):
        tiles = self.load_image(path)
        width = tiles.get_width()
        height = tiles.get_height()
        tileset = []
        for y in range(0, height, TILE_SIZE):
            for x in range(0, width, TILE_SIZE):
                tileset.append(tiles.subsurface(x, y, TILE_SIZE, TILE_SIZE))
        return tileset

    def load_tiles(self):
        tiles = {}
        path = os.path.join(PATH, "assets/tiles/")
        for (root, dirs, files) in os.walk(path, topdown=True):
            for file_ in files:
                filename = file_[:-4]
                tiles[filename] = self.load_tileset(root + '/' + file_)
        return tiles

    def load_ui(self):
        ui = {}
        path = os.path.join(PATH, "assets/ui")
        for (root, dirs, files) in os.walk(path, topdown=True):
            for file_ in files:
                ui[file_[:-4]] = self.load_image(root + '/' + file_)
        return ui
    
    def load_fonts(self):
        fonts = {}
        path = os.path.join(PATH, "assets/fonts/")
        for (root, dirs, files) in os.walk(path, topdown=True):
            for file_ in files:
                fonts[file_[:-4]] = pygame.font.Font(os.path.join(path, file_), int(file_[-6:-4])) # font_nameXX -> XX Represent the size of the font
        return fonts
