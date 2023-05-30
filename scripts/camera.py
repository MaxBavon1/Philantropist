import pygame

class Camera:

    def __init__(self, game):
        self.game = game
        self.target = pygame.Vector2(0)
        self.position = pygame.Vector2(0)
        self.offset = pygame.Vector2(0)
        self.center = pygame.Vector2(game.WIDTH/2, game.HEIGHT/2)
        self.rect = pygame.Rect(self.position, (game.WIDTH, game.HEIGHT))
        self.smoothSpeed = 2.5
    
    def screen_to_world_point(self, point):
        return point + self.offset

    def follow(self, entity):
        self.target = entity.position
        self.position = pygame.Vector2(self.target)

    def update(self, deltaTime):
        self.position = self.position.lerp(self.target, self.smoothSpeed * deltaTime)
        self.rect.center = self.position
        self.offset = self.position - self.center
    
    def render_debug(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), self.center, 0)