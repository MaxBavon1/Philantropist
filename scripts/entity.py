import pygame
import math

__all__ = ["StaticEntity", "Entity"]

""" All Games Objects are considered as entities, static entities are entities that do not 
have animations, whearas entity are animated
Therefore StaticEntity and Entity defines the behaviour of all objects in the game, 
since the player, the ennemies, the bullets and the collectables all inherit from the entity class"""


class StaticEntity(pygame.sprite.Sprite):

    entityManager = None

    def __init__(self, sprite, pos, hitsize=(0,0), speed=1, vel=0, health=1, damage=1, tag="Entity"):
        super().__init__()
        # Physics
        self.position = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(vel)
        self.rect = sprite.get_rect(center=self.position)
        self.hitbox = sprite.get_rect(center=self.position)
        self.hitsize = pygame.Vector2(hitsize)
        self.set_size(self.rect.size)
        self.sprite = sprite
        self.speed = speed
        self.grounded = False
        # Attributes
        self.maxHealth = health
        self.health = self.maxHealth
        self.damage = damage
        self.tag = tag

    @classmethod
    def init(cls, manager):
        cls.entityManager = manager
    
    def set_left(self, x):
        self.hitbox.left = x
        self.position.x = self.hitbox.centerx
        self.rect.centerx = self.hitbox.centerx

    def set_right(self, x):
        self.hitbox.right = x
        self.position.x = self.hitbox.centerx
        self.rect.centerx = self.hitbox.centerx

    def set_top(self, y):
        self.hitbox.top = y
        self.position.y = self.hitbox.centery
        self.rect.centery = self.hitbox.centery

    def set_bottom(self, y):
        self.hitbox.bottom = y
        self.position.y = self.hitbox.centery
        self.rect.centery = self.hitbox.centery
    
    def set_pos(self, pos):
        self.position.x, self.position.y = pos[0], pos[1]
        self.hitbox.center = pos
        self.rect.center = pos
    
    def set_size(self, size):
        self.hitbox.size = size[0] - self.hitsize.x, size[1] - self.hitsize[1]
        self.rect.size = size
        self.hitbox.center = self.position
        self.rect.center = self.position
    
    def health_update(self):
        if self.health <= 0:
            self.destroy()

    def horizontal_collision(self, level):
        # ---- Horizontal Collisions ----
        if self.hitbox.left < level.border.left: # Border Left
            self.hitbox.left = level.border.left
            self.position.x = self.hitbox.centerx
        if self.hitbox.right > level.border.right: # Border Right
            self.hitbox.right = level.border.right
            self.position.x = self.hitbox.centerx

        for tile in level.collide(self): # TileMap
            if self.velocity.x > 0:
                self.hitbox.right = tile.left
                self.position.x = self.hitbox.centerx
            elif self.velocity.x < 0:
                self.hitbox.left = tile.right
                self.position.x = self.hitbox.centerx

    def vertical_collision(self, level):
        # ---- Vertical Collisions ----
        if self.hitbox.top < level.border.top: # Border Top
            self.hitbox.top = level.border.top
            self.position.y = self.hitbox.centery
            self.velocity.y = 0
        if self.hitbox.bottom > level.border.bottom: # Border Bottom
            self.hitbox.bottom = level.border.bottom
            self.position.y = self.hitbox.centery
            self.velocity.y = 0
            self.grounded = True

        for tile in level.collide(self): # TileMap
            if self.velocity.y > 0:
                self.hitbox.bottom = tile.top
                self.position.y = self.hitbox.centery
                self.velocity.y = 0
                self.grounded = True
            elif self.velocity.y < 0:
                self.hitbox.top = tile.bottom
                self.position.y = self.hitbox.centery
                self.velocity.y = 0 

    def update(self, deltaTime, gravityScale):
        self.health_update()
        # ---- Map Collisions
        # X Axis
        level = self.entityManager.game.level
        self.position.x += self.velocity.x * deltaTime
        self.hitbox.centerx = self.position.x
        self.horizontal_collision(level)
        # Y Axis
        self.velocity.y += gravityScale * deltaTime
        self.position.y += self.velocity.y * deltaTime
        self.hitbox.centery = math.ceil(self.position.y)
        self.vertical_collision(level)

        self.rect.center = self.position

        if (self.grounded and self.velocity.y != 0):
            self.grounded = False

    def render(self, surface, offset, screen):
        if self.rect.colliderect(screen):
            surface.blit(self.sprite, pygame.Vector2(self.rect.topleft) - offset)
 
    def render_debug(self, surface, offset):
        # HitBox
        hitbox = pygame.Rect(self.hitbox.x - offset.x, self.hitbox.y - offset.y, self.hitbox.w, self.hitbox.h)
        if self.grounded: pygame.draw.rect(surface, (0,255,0), hitbox, 1)
        else: pygame.draw.rect(surface, (255,0,0), hitbox, 1)

        pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(self.rect.x - offset.x, self.rect.y - offset.y, self.rect.w, self.rect.h), 1)
        # Position
        pygame.draw.circle(surface, (0, 0, 0), self.position - offset, 2)
        # Velocity
        movement = self.velocity * 0.2
        pygame.draw.aaline(surface, (0,0,255), self.position - offset, self.position + movement - offset, 2)

    def destroy(self):
        self.kill()
        self.on_death()

    def on_collision(self, entity):
        pass

    def on_death(self):
        pass


class Entity(StaticEntity):
     
    def __init__(self, animations, pos, hitsize=(0,0), speed=1, vel=0, health=1, damage=1, anim_speed=1, tag="Entity"):
        self.animations = animations
        self.current_anim = list(animations.keys())[0]
        self.frame = 0
        self.anim_speed = anim_speed
        self.direction = "right"
        super().__init__(animations[self.current_anim][0], pos, hitsize, speed, vel, health, damage, tag)

    def set_animation_rect(self, animation, sprite):
        pass

    def play(self, animation):
        if self.current_anim != animation:
            self.frame = 0
            self.current_anim = animation
            self.set_animation_rect(animation, self.animations[self.current_anim][0])

    def animate(self):
        self.frame += 1
        self.frame %= len(self.animations[self.current_anim]) * self.anim_speed
        self.sprite = self.animations[self.current_anim][self.frame // self.anim_speed]

    def update(self, deltaTime, gravityScale):
        super().update(deltaTime, gravityScale)
        self.animate()