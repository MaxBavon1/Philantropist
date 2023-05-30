from pygame.locals import *
import pygame


__all__ = ["UIManager", "Image", "Label", "Button", "ButtonImg", "ButtonLabel"]


class UIManager:

    __slots__ = ["buttons", "objects"]

    def __init__(self):
        self.buttons = []
        self.objects = []

    def add(self, obj):
        if (isinstance(obj, Image) or isinstance(obj, Label)):
            self.objects.append(obj)
        else:
            self.buttons.append(obj)

    def adds(self, *objs):
        for obj in objs:
            if (isinstance(obj, Image) or isinstance(obj, Label)):
                self.objects.append(obj)
            else:
                self.buttons.append(obj)

    def clicked(self, mousePos):
        for obj in self.buttons:
            obj.clicked(mousePos)

    def update(self, mousePos):
        for obj in self.buttons:
            obj.update(mousePos)
    
    def render(self, surface):
        for obj in self.buttons:
            obj.render(surface)
        for obj in self.objects:
            obj.render(surface)


class Image:

    __slots__ = ["position", "image"]

    def __init__(self, pos, img) -> None:
        self.position = pos
        self.image = img

    def render(self, surface):
        surface.blit(self.image, (self.position[0] - self.image.get_width() / 2, self.position[1] - self.image.get_height() / 2))


class Label:

    __slots__ = ["position", "font", "text", "text_color"]

    def __init__(self, pos, font, txt="", txt_color=(255,255,220)) -> None:
        self.position = pos
        self.font = font
        self.text = txt
        self.text_color = txt_color

    def render(self, surface):
        surf = self.font.render(self.text, 1, self. text_color)
        width, height = self.font.size(self.text)
        surface.blit(surf, (self.position[0] - (width / 2), self.position[1] - (height / 2)))


class Button:

    __slots__ = ["font", "text", "rect", "background", "hover_color", "text_color", "hover_scale", "hover", "command"]

    def __init__(self, pos, size, font, txt="", bg=(0,0,0,180), txt_color=(255,255,220), hover_col=(0, 0, 0, 255), hover_scale=1.1, command=lambda:0):
        self.font = font
        self.text = txt
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = pos
        self.background = bg
        self.text_color = txt_color
        self.hover_color = hover_col
        self.hover_scale = hover_scale
        self.hover = False
        self.command = command
    
    def collide(self, mousePos):
        return self.rect.collidepoint(mousePos.x, mousePos.y)

    def clicked(self, mousePos):
        if (self.hover):
            self.command()

    def update(self, mousePos):
        self.hover = self.collide(mousePos)

    def render(self, surface):
        if self.hover:
            surf = pygame.Surface(self.rect.size)
            surf.fill(self.hover_color)
            width, height = self.font.size(self.text)
            txt_surf = self.font.render(self.text, 1, self.text_color)
            surf.blit(txt_surf, (surf.get_width() / 2 - width / 2, surf.get_height() / 2 - height / 2))
            surf.set_alpha(self.hover_color[3])

            surface.blit(surf, self.rect.topleft)
        else:
            surf = pygame.Surface(self.rect.size)
            surf.fill(self.background)
            width, height = self.font.size(self.text)
            txt_surf = self.font.render(self.text, 1, self.text_color)
            surf.blit(txt_surf, (surf.get_width() / 2 - width / 2, surf.get_height() / 2 - height / 2))
            surf.set_alpha(self.background[3])

            surface.blit(surf, self.rect.topleft)


class ButtonImg:

    __slots__ = ["image", "rect", "hover_color", "hover_scale", "hover", "command"]

    def __init__(self, pos, img, hover_col=(200, 200, 200), hover_scale=1.1, command=lambda:0):
        self.image = img
        self.rect = img.get_rect(center=pos)
        self.hover_color = hover_col
        self.hover_scale = hover_scale
        self.hover = False
        self.command = command
    
    def collide(self, mousePos):
        return self.rect.collidepoint(mousePos.x, mousePos.y)

    def clicked(self, mousePos):
        if (self.hover):
            self.command()

    def update(self, mousePos):
        self.hover = self.collide(mousePos)

    def render(self, surface):
        if self.hover:
            surf = self.image.copy()
            hover_surf = pygame.Surface(surf.get_size())
            hover_surf.set_alpha(100)
            hover_surf.fill(self.hover_color)
            surf.blit(hover_surf, (0, 0))
            surf = pygame.transform.scale_by(surf, self.hover_scale)
            surface.blit(surf, (self.rect.centerx - surf.get_width() / 2, self.rect.centery - surf.get_height() / 2))
        else:
            surface.blit(self.image, self.rect.topleft)



class ButtonLabel:
    
    __slots__ = ["text", "font", "rect", "text_color", "hover_color", "hover_scale", "hover", "command"]

    def __init__(self, pos, font, txt="", txt_color=(255,255,255), hover_color=(0,0,0), command=lambda:0):
        self.text = txt
        self.font = font
        self.rect = pygame.Rect((0, 0, 0, 0))
        self.rect.size = self.font.size(txt)[0], self.font.size(txt)[1]
        self.rect.center = pos
        self.text_color = txt_color
        self.hover_color = hover_color
        self.hover = False
        self.command = command

    def collide(self, mousePos):
        return self.rect.collidepoint(mousePos.x, mousePos.y)

    def clicked(self, mousePos):
        if (self.hover):
            self.command()

    def update(self, mousePos):
        self.hover = self.collide(mousePos)

    def render(self, surface):
        if self.hover:
            surf = self.font.render(self.text, 1, self.hover_color)
        else:
            surf = self.font.render(self.text, 1, self.text_color)
        
        surface.blit(surf, self.rect.topleft)