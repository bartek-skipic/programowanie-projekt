from functools import wraps
import pygame

def only_enabled(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.enabled:
            return False
        return method(self, *args, **kwargs)

    return wrapper

class Button:

    def __init__(self, posx, posy, color, textColor, title):
        self.enabled = True
        self.textColor = textColor
        self.color = color
        self.title = title
        self.posx, self.posy = posx, posy
        self.width = 100
        self.height = 50
        self.rectdraw = pygame.Rect(posx + 5, posy + 5, self.width - 10, self.height - 10)
        self.borderdraw = pygame.Rect(posx, posy, self.width, self.height)
        self.font = pygame.font.SysFont('Arial', 16)
        self.text = self.font.render(title, True, self.textColor)
        self.textWidth, self.textHeight = self.font.size(title)

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("enabled musi mieć wartość bool.")
        self._enabled = value

    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), self.borderdraw)
        pygame.draw.rect(screen, self.color, self.rectdraw)
        screen.blit(self.text, (self.posx + self.width/2 - self.textWidth/2, self.posy + self.height/2 - self.textHeight/2))

    @only_enabled
    def is_clicked(self, mouse_pos):
        return self.borderdraw.collidepoint(mouse_pos)
