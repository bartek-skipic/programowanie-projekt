class GeometricFigure:

    def __init__(self, posx, posy, color):
        self.posx = posx
        self.posy = posy
        self.color = color

    def setPosition(self, posx, posy):
        self.posx = posx
        self.posy = posy

    def draw(self, screen):
        pass

    def is_clicked(self, mouse_pos):
        return False

