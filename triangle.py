import pygame

from geometricfigure import GeometricFigure

class Triangle(GeometricFigure):

    def __init__(self, posx, posy, color):
        super().__init__(posx, posy, color)
        self.vertices = [(posx, posy), (posx - 100, posy - 150), (posx + 100, posy - 150)]

    def setPosition(self, posx, posy):
        super().setPosition(posx, posy)
        self.vertices[0] = (posx, posy)
        self.vertices[1] = (posx - 100, posy - 150)
        self.vertices[2] = (posx + 100, posy - 150)

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.vertices)

    def is_clicked(self, mouse_pos):
        x, y = mouse_pos
        x1, y1 = self.vertices[0]
        x2, y2 = self.vertices[1]
        x3, y3 = self.vertices[2]

        denominator = ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))

        a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
        b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
        c = 1 - a - b

        return a >= 0 and b >= 0 and c >= 0