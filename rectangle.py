import pygame

from geometricfigure import GeometricFigure


class Rectangle(GeometricFigure):

    def __init__(self, posx, posy, width, height, color):
        super().__init__(posx, posy, color)
        self.width = width
        self.height = height
        self.rectdraw = pygame.Rect(posx, posy, width, height)

    def setPosition(self, posx, posy):
        super().setPosition(posx, posy)
        self.rectdraw.x = posx
        self.rectdraw.y = posy

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rectdraw)

    def is_clicked(self, mouse_pos):
        return self.rectdraw.collidepoint(mouse_pos)