import pygame

from .entity import *


__all__ = ["Ennemy", "Zombie"]


""" We didn't have anough time to implement all types of ennemies but since there are modular
it would take a minimum amount of time, it just requires to change up the sprites and the behaviour
of the ennemy AI """


class Ennemy(Entity):

    data = None
    assets = None

    def __init__(self, ennemyType, target, pos):
        data = self.data[ennemyType]
        super().__init__(self.assets[ennemyType + "_anim"], pos, (15,0), data["speed"], (0,0), data["health"], data["damage"], data["anim_speed"], ennemyType)
        self.target = target
        self.jumpForce = data["jumpForce"]

        self.hit = False
        self.move_cooldown = 0.6
        self.hit_cooldown = 0.6
        self.last_hit = self.hit_cooldown

    @classmethod
    def init(cls, data, assets):
        cls.data = data
        cls.assets = assets

    def jump(self):
        self.velocity.y -= self.jumpForce

    def animate(self):
        if not self.hit:
            if self.direction == "right":
                self.play("run_right")
            else:
                self.play("run_left")

        super().animate()

    def set_animation_rect(self, animation, sprite):
        left, right, top, bottom = self.hitbox.left, self.hitbox.right, self.hitbox.top, self.hitbox.bottom # Saves old position
        self.set_size(sprite.get_size()) # Then resize the sprite to fit new animation

        # Finally reset the position before the sprite switch
        if self.direction == right: self.set_right(right)
        else: self.set_left(left)
        if self.velocity.y > 0: self.set_top(top)
        else: self.set_bottom(bottom)

    def update(self, deltaTime, gravityScale):
        self.hit = not self.last_hit >= self.move_cooldown
        self.last_hit += deltaTime

        self.velocity.x = 0
        if not self.hit:
            mouvement = (self.target.position - self.position).normalize()
            self.velocity.x = mouvement.x * self.speed
            if mouvement.y < 0 and self.grounded:
                self.jump()

            if self.velocity.x > 0:
                self.direction = "right"
            else:
                self.direction = "left"
        
        super().update(deltaTime, gravityScale)

    def take_damage(self, damage):
        if self.last_hit >= self.hit_cooldown:
            self.last_hit = 0
            self.health -= damage
            if self.direction == "right": self.play("hit_right")
            else: self.play("hit_left")


class Zombie(Ennemy):

    def __init__(self, target, pos):
        super().__init__("zombie", target, pos)