from .entity import *
import pygame

class Bullet(StaticEntity):
    
    lifeSpan = 15
    bulletForce = 1200
    bounce = (0.75, 0.65)
    bulletDamage = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity *= self.bulletForce
        self.spawnTime = 0
        self.rebounce = self.lifeSpan
        self.damage = self.bulletDamage

    def bounce_off(self, axis=1):
        self.rebounce -= 1
        self.velocity.x *= axis * self.bounce[0]
        self.velocity.y *= -axis * self.bounce[1]

    def horizontal_collision(self, level):
        if self.hitbox.left < level.border.left: # Border Left
            self.hitbox.left = level.border.left
            self.position.x = self.hitbox.centerx
            self.bounce_off(-1)
        if self.hitbox.right > level.border.right: # Border Right
            self.hitbox.right = level.border.right
            self.position.x = self.hitbox.centerx
            self.bounce_off(-1)

        for tile in level.collide(self): # TileMap
            if self.velocity.x > 0 and self.hitbox.left < tile.left:
                self.hitbox.right = tile.left
                self.position.x = self.hitbox.centerx
                self.bounce_off(-1)
            elif self.velocity.x < 0 and self.hitbox.right > tile.right:
                self.hitbox.left = tile.right
                self.position.x = self.hitbox.centerx
                self.bounce_off(-1)
 
    def vertical_collision(self, level):
         # ---- Vertical Collisions ----
        if self.hitbox.top < level.border.top: # Border Top
            self.hitbox.top = level.border.top
            self.position.y = self.hitbox.centery
            self.bounce_off(1)
        if self.hitbox.bottom > level.border.bottom: # Border Bottom
            self.hitbox.bottom = level.border.bottom
            self.position.y = self.hitbox.centery
            self.bounce_off(1)

        for tile in level.collide(self): # TileMap
            if self.velocity.y > 0 and self.hitbox.top < tile.top:
                self.hitbox.bottom = tile.top
                self.position.y = self.hitbox.centery
                self.bounce_off(1)
            elif self.velocity.y < 0 and self.hitbox.bottom > tile.bottom:
                self.hitbox.top = tile.bottom
                self.position.y = self.hitbox.centery
                self.bounce_off(1)

    def update(self, deltaTime, gravityScale):
        self.spawnTime += deltaTime
        if self.spawnTime > self.lifeSpan or self.rebounce <= 0:
            self.destroy()

        #X Axis
        level = self.entityManager.game.level
        self.position.x += self.velocity.x * deltaTime
        self.hitbox.centerx = self.position.x
        self.horizontal_collision(level)
        # Y Axis
        self.velocity.y += gravityScale * deltaTime
        self.position.y += self.velocity.y * deltaTime
        self.hitbox.centery = self.position.y
        self.vertical_collision(level)

        self.rect.center = self.position

    def on_collision(self, entity):
        if entity.tag == "slime":
            self.alive = False
