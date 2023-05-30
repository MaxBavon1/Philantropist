from .assets import *
from .entity import *
from .player import *
from .bullet import *
from .ennemies import *
from .collectables import *


class EntityGroup(pygame.sprite.Group):

    def __init__(self, entityManager):
        super().__init__()
        self.entityManager = entityManager

    def render(self, surface, camera):
        for entity in self:
            entity.render(surface, camera.offset, camera.rect)
            if self.entityManager.game.debugMode:
                entity.render_debug(surface, camera.offset)


class EntityManager:

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.assets = game.assets.sprites
        self.data = game.data.entities
        self.types = {
            "zombie": Zombie
        }
        StaticEntity.init(self)
        Ennemy.init(self.data, self.assets)
        self.player = Player(self.assets["player_anim"], (0, 0), hitsize=(15, 0), tag="player")
        self.ennemies = EntityGroup(self)
        self.bullets = EntityGroup(self)

    def spawn_ennemy(self, entityType, *args, **kwargs):
        entity = self.types[entityType](self.player, *args, **kwargs)
        self.ennemies.add(entity)

    def create_bullet(self, pos, vel):
        bullet = Bullet(self.assets["bullet"], pos, hitsize=(5,5), vel=vel, tag="bullet")
        self.bullets.add(bullet)

    @property
    def size(self):
        return 1 + len(self.ennemies) + len(self.bullets)

    def load_entities(self, entity_tilemap):
        for y in range(len(entity_tilemap)):
            for x in range(len(entity_tilemap[0])):
                ID = int(entity_tilemap[y][x])
                if ID != -1:
                    tile_pos = pygame.Vector2(x * TILE_SIZE, y * TILE_SIZE)
                    if ID == 16: # Player
                        self.player.position = pygame.Vector2(tile_pos)
                    elif ID == 19: # Zombie
                        self.spawn_ennemy("zombie", tile_pos)

    def load_level(self, entity_tilemap, objects_tilemap):
        self.ennemies.empty()
        self.bullets.empty()
        self.load_entities(entity_tilemap)      
        self.player.velocity = pygame.Vector2(0)
        self.player.coins = 0
        self.player.health = self.player.maxHealth

    def update(self, deltaTime, gravityScale):
        self.bullets.update(deltaTime, gravityScale)
        self.ennemies.update(deltaTime, gravityScale)
        self.player.update(deltaTime, gravityScale)

        self.handle_collisions()

    def render(self, surface, camera):
        self.player.render(surface, camera)
        if self.game.debugMode:
            self.player.render_debug(surface, camera.offset)
        self.ennemies.render(surface, camera)
        self.bullets.render(surface, camera)

    def handle_collisions(self):
        for bullet, ennemies in pygame.sprite.groupcollide(self.bullets, self.ennemies, False, False).items():
            bullet.destroy()
            for ennemy in ennemies:
                ennemy.take_damage(bullet.damage)

        #self.player.health -= len(pygame.sprite.spritecollide(self.player, self.ennemies, False))