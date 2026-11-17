import pygame

from geometricfigure import GeometricFigure

class Oval(GeometricFigure):

    def __init__(self, posx, posy, radius, color):
        super().__init__(posx, posy, color)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)


    def is_clicked(self, mouse_pos):
        mouse_vec = pygame.math.Vector2(mouse_pos)
        pos_vec = pygame.math.Vector2(self.posx, self.posy)
        distance = mouse_vec.distance_to(pos_vec)
        return distance <= self.radius