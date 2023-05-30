import pygame


__all__ = ["Trap"]


class Trap(pygame.sprite.Sprite):

    def __init__(self, animation, pos, anim_speed, hitsize=(0,0), cooldown=0.2, tag="collectable"):
        super().__init__()
        # Physics
        self.animation = animation
        self.nb_anims = len(self.animation)
        self.frame = 0
        self.anim_speed = anim_speed
        self.sprite = animation[0]
        self.rect = animation[0].get_rect(center=pos)
        self.hitbox = animation[0].get_rect(center=pos)
        self.hitsize = hitsize
        self.set_hitbox()

        self.activated = False
        self.cooldown = cooldown
        self.last_activation = cooldown
        self.damage = 1

        self.tag = tag

    @classmethod
    def init(cls, manager):
        cls.entityManager = manager
    
    def set_hitbox(self):
        self.hitbox.width = self.rect.width - self.hitsize[0]
        self.hitbox.height = self.rect.height - self.hitsize[1]
        self.hitbox.center = self.rect.center

    def animate(self):
        self.frame += 1
        self.frame %= self.nb_anims * self.anim_speed
        self.sprite = self.animation[self.frame // self.anim_speed]
    
    def animation_finished(self):
        return self.frame // self.anim_speed == self.nb_anims - 1

    def update(self, deltaTime):
        self.last_activation += deltaTime
        self.activated = False
        if (self.last_activation >= self.cooldown):
            self.activated = True
            self.animate()
        if self.animation_finished():
            self.last_activation = 0
            self.animate()
        
        if self.activated: self.set_hitbox()
        else: self.hitbox.size = (0, 0)

    def render(self, surface, offset, screen):
        if self.rect.colliderect(screen):
            surface.blit(self.sprite, pygame.Vector2(self.rect.topleft) - offset)
 
    def render_debug(self, surface, offset):
        # HitBox
        hitbox = pygame.Rect(self.hitbox.x - offset.x, self.hitbox.y - offset.y, self.hitbox.w, self.hitbox.h)
        pygame.draw.rect(surface, (255,0,0), hitbox, 1)

    def destroy(self):
        self.kill()

    def on_collision(self):
        self.destroy()