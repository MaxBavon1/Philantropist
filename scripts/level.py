import pygame
import csv
import os

from .assets import *
from .collectables import *
from .traps import *


class TrapsGroup(pygame.sprite.Group):

    def __init__(self, level):
        super().__init__()
        self.level = level

    def render(self, surface, camera):
        for entity in self:
            entity.render(surface, camera.offset, camera.rect)
            if self.level.game.debugMode:
                entity.render_debug(surface, camera.offset)


class CollectablesGroup(pygame.sprite.Group):

    def __init__(self, level):
        super().__init__()
        self.level = level

    def render(self, surface, camera):
        for entity in self:
            entity.render(surface, camera.offset, camera.rect)
            if self.level.game.debugMode:
                entity.render_debug(surface, camera.offset)


class Level:

    levels = {1 : "forest", 2 : "snow", 3 : "lava"}

    def __init__(self, game):
        self.game = game
        self.data = self.game.data.levels
        self.assets = game.assets.sprites
        self.tiles = game.assets.tiles

        self.tilemap = []
        self.layers = {}
        self.tilesets = {}
        self.traps = TrapsGroup(self)
        self.collectables = CollectablesGroup(self)
        
        self.parallalax_factor = 0.2
        self.background = None

        self.level = 0
        self.name = ""
        self.width = 0
        self.height = 0
        self.border = pygame.Rect(0, 0, 0, 0)

    def load_tilemaps(self, lvl):
        self.layers = {}
        path = f"data/level{lvl}/"
        for tilemap in os.listdir(path):
            name = tilemap.replace(".csv", "")
            name = name[7:] # Remove the "leveln_"
            name = name.lower()
            if name == "collisions":
                self.tilemap = list(csv.reader(open(path + tilemap)))
            else:
                self.layers[name] = list(csv.reader(open(path + tilemap)))

    def load_tilesets(self):
        self.tilesets = {}
        self.tilesets["collisions"] = self.tiles[self.name]
        for name in self.layers:
            self.tilesets[name] = self.tiles[name]

    def load_traps(self):
        self.traps.empty()
        traps_tilemap = self.layers["traps"]
        for y in range(len(traps_tilemap)):
            for x in range(len(traps_tilemap[0])):
                ID = int(traps_tilemap[y][x])
                if ID != -1:
                    tile_pos = pygame.Vector2(x * TILE_SIZE, y * TILE_SIZE)
                    tile_pos.x += TILE_SIZE // 2
                    tile_pos.y += TILE_SIZE // 2
                    if ID == 10: # Spikes
                        spike = Trap(self.assets["spike_anim"], tile_pos, 15, (5, 5), tag="spike")
                        self.traps.add(spike)

    def load_objects(self):
        self.collectables.empty()
        objects_tilemap = self.layers["objects"]
        for y in range(len(objects_tilemap)):
            for x in range(len(objects_tilemap[0])):
                ID = int(objects_tilemap[y][x])
                if ID != -1:
                    tile_pos = pygame.Vector2(x * TILE_SIZE, y * TILE_SIZE)
                    tile_pos.x += TILE_SIZE // 2
                    tile_pos.y += TILE_SIZE // 2
                    if ID == 0: # Coin
                        coin = Collectable(self.assets["coin_spin_anim"], tile_pos, 10, (25, 25), tag="coin")
                        self.collectables.add(coin)
                    if ID == 1: # Hearth
                        hearth = Collectable(self.assets["hearth_anim"], tile_pos, 20, (25, 25), tag="hearth")
                        self.collectables.add(hearth)
                    if ID == 6: # End Flag
                        flag = Collectable(self.assets["flag_anim"], (tile_pos.x + TILE_SIZE//2, tile_pos.y + TILE_SIZE//2), 20, (50, 50), tag="flag")
                        self.collectables.add(flag)

    def load_level(self, lvl):
        self.level = lvl
        self.name = self.levels[lvl]
        self.load_tilemaps(lvl)
        self.load_tilesets()
        self.load_traps()
        self.load_objects()
        self.background = self.assets[self.data[f"level{self.level}"]["background"]]

        self.width = len(self.tilemap[0])
        self.height = len(self.tilemap)
        self.border = pygame.Rect(0, 0, self.width * TILE_SIZE, self.height * TILE_SIZE)

    def level_complete(self):
        self.game.data.progress[f"level {self.level}"] = True
        self.game.data.save_progress()
        self.game.winMenu.run()
    
    def find_level_end(self) -> pygame.Rect:
        for y in range(self.height):
            for x in range(self.width):
                ID = int(self.layers["objects"][y][x])
                if ID == 6: # End Flag
                    return pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE * 2, TILE_SIZE * 2)
    
    def collide(self, entity, range_=2) -> list:
        tileX = int(entity.hitbox.x // TILE_SIZE)
        tileY = int(entity.hitbox.y // TILE_SIZE)
        tiles = []
        detection_range = range_
        for y in range(tileY - detection_range, tileY + detection_range + 1):
            for x in range(tileX - detection_range, tileX + detection_range + 1):
                if (x >= 0 and x < self.width) and (y >= 0 and y < self.height):
                    ID = int(self.tilemap[y][x])
                    if ID != -1 and ID < 100 and ID not in self.data[f"level{self.level}"]["collisions"]:
                        tile = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if entity.hitbox.colliderect(tile):
                            tiles.append(tile)
        return tiles

    def handle_collisions(self, player):
        for trap in self.traps:
            if trap.hitbox.colliderect(player.hitbox):
                player.take_damage(trap.damage)

        for collectable in self.collectables:
            if collectable.hitbox.colliderect(player.hitbox):
                if collectable.tag == "coin":
                    player.coins += 1
                elif collectable.tag == "hearth":
                    player.health += 2
                elif collectable.tag == "flag":
                    self.level_complete()
                collectable.on_collision()

    def render_tilemap(self, surface, camera, tilemap, tileset):
        offset, screen = camera.offset, camera.rect
        for y in range(self.height):
            for x in range(self.width):
                ID = int(tilemap[y][x])
                if ID != -1:
                    tile_pos = pygame.Vector2(x * TILE_SIZE, y * TILE_SIZE)
                    if screen.colliderect(pygame.Rect(tile_pos, (TILE_SIZE, TILE_SIZE))):
                        try:
                            tile = tileset[ID]
                            surface.blit(tile, tile_pos - offset)
                        except IndexError:
                            print("Invalid Tile !")
    
    def render_fast(self, surface, camera):
        pass

    def render_debug(self, surface, offset):
        for y in range(self.height):
            for x in range(self.width):
                ID = int(self.tilemap[y][x])
                if ID > 10:
                    pygame.draw.rect(surface, (0,255,0), (x * TILE_SIZE - offset.x, y * TILE_SIZE - offset.y, TILE_SIZE, TILE_SIZE), 1)
        
        border = pygame.Rect(self.border.x - offset.x, self.border.y - offset.y, self.border.w, self.border.h)
        pygame.draw.rect(surface, (255,0,0), border, 2)

    def render(self, surface, camera):
        """ Render all level layers and main collision tilemap in order (to create depth) """
        surface.blit(self.background, (-camera.position.x * self.parallalax_factor, -camera.position.y * self.parallalax_factor - 50))
        self.traps.render(surface, camera)
        self.render_tilemap(surface, camera, self.tilemap, self.tilesets["collisions"])
        self.collectables.render(surface, camera)

        if self.game.debugMode:
            self.render_debug(surface, camera.offset)
        
    def update(self, deltaTime):
        self.traps.update(deltaTime)
        self.collectables.update()