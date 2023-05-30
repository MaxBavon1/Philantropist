import pygame


__all__ = ["Collectable"]


class Collectable(pygame.sprite.Sprite):

    def __init__(self, animation, pos, anim_speed, hitsize=(0,0), tag="collectable"):
        super().__init__()
        # Physics
        self.animation = animation
        self.frame = 0
        self.anim_speed = anim_speed
        self.sprite = animation[0]
        self.rect = animation[0].get_rect(center=pos)
        self.hitbox = animation[0].get_rect(center=pos)
        self.hitbox.width -= hitsize[0]
        self.hitbox.height -= hitsize[1]
        self.hitbox.center = self.rect.center

        self.tag = tag

    @classmethod
    def init(cls, manager):
        cls.entityManager = manager

    def animate(self):
        self.frame += 1
        self.frame %= len(self.animation) * self.anim_speed
        self.sprite = self.animation[self.frame // self.anim_speed]

    def update(self):
        self.animate()

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