from .entity import *
from .bullet import *

import pygame


class Player(Entity):
    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.anim_speed = 8
        self.jumpForce = 600
        self.speed = 250
        self.maxHealth = 10
        self.health = self.maxHealth
        self.flyingSpeed = 2500
        self.play("walk_right")

        self.hit = False
        self.move_cooldown = 0.35
        self.hit_cooldown = 1.2
        self.last_hit = self.hit_cooldown
        
        self.hearth_ui = self.entityManager.game.assets.ui["hearth"]
        self.coin_ui = self.entityManager.game.assets.ui["coin"]
        self.coins = 4
    
    def animate(self):
        if not self.hit:
            if self.direction == "right":
                if self.velocity.y == 0:
                    self.play("idle_right") if self.velocity.x == 0 else self.play("walk_right")
                else:
                    self.play("fall_right") if self.velocity.y > 0 else self.play("jump_right")
            else:
                if self.velocity.y == 0:
                    self.play("idle_left") if self.velocity.x == 0 else self.play("walk_left")
                else:
                    self.play("fall_left") if self.velocity.y > 0 else self.play("jump_left")

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

        keyboard = pygame.key.get_pressed()
        self.velocity.x = 0
        if not self.hit and keyboard[pygame.K_d] or keyboard[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.direction = "right"
        if not self.hit and keyboard[pygame.K_q] or keyboard[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.direction = "left"

        if keyboard[pygame.K_TAB]:
            self.shoot()
        if keyboard[pygame.K_LSHIFT]:
            self.velocity.y -= self.flyingSpeed * deltaTime

        super().update(deltaTime, gravityScale)
    
        # Collectables Collisions
        self.entityManager.game.level.handle_collisions(self)

    def jump(self):
        self.velocity.y -= self.jumpForce
    
    def shoot(self):
        cursor = self.entityManager.game.camera.screen_to_world_point(pygame.mouse.get_pos())
        direction = (pygame.Vector2(cursor) - self.position)
        self.entityManager.create_bullet(self.position, direction.normalize())

    def render(self, surface, camera):
        super().render(surface, camera.offset, camera.rect)

        # ---- UI ----
        hearth_width, hearth_height = self.hearth_ui.get_size()
        for n in range(self.health // 2): # Hearts
            surface.blit(self.hearth_ui, (hearth_width * n, 0))

        surface.blit(self.coin_ui, (0, hearth_height))
        self.entityManager.game.render_text(str(self.coins), (self.coin_ui.get_width(), hearth_height), "rubik40")
    
    def take_damage(self, damage):
        if self.last_hit >= self.hit_cooldown:
            self.last_hit = 0
            self.health -= damage
            if self.direction == "right": self.play("hit_right")
            else: self.play("hit_left")

    def on_death(self):
        self.entityManager.game.deathMenu.run()