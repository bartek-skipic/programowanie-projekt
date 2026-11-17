import pygame
import sys
import random
import pickle

from button import Button
from oval import Oval
from rectangle import Rectangle
from triangle import Triangle

def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

pygame.init()

size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Projekt")

figures = []
buttons = []

BACKGROUND_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR= (255, 255, 255)

font = pygame.font.SysFont('Arial', 16)
text = font.render('', True, BLACK_COLOR)

button1 = Button(0,0, WHITE_COLOR, BLACK_COLOR,'KWADRAT')
buttons.append(button1)
button2 = Button(100,0, WHITE_COLOR, BLACK_COLOR,'TROJKAT')
buttons.append(button2)
button3 = Button(200,0, WHITE_COLOR, BLACK_COLOR,'OKRAG')
buttons.append(button3)
button4 = Button(300,0, WHITE_COLOR, BLACK_COLOR,'SAVE')
buttons.append(button4)
button5 = Button(400,0, WHITE_COLOR, BLACK_COLOR,'LOAD')
buttons.append(button5)

isMoving = False
chosenfigure = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_clicked(event.pos) and button.title == "KWADRAT":
                    rect = Rectangle(400, 300, 100, 100, random_color())
                    figures.append(rect)
                elif button.is_clicked(event.pos) and button.title == "TROJKAT":
                    triangle = Triangle(400, 300, random_color())
                    figures.append(triangle)
                elif button.is_clicked(event.pos) and button.title == "OKRAG":
                    oval = Oval(400, 300, 100, random_color())
                    figures.append(oval)
                elif button.is_clicked(event.pos) and button.title == "SAVE":
                    with open("projekt.pkl", "wb") as file:
                        pickle.dump(figures, file)
                elif button.is_clicked(event.pos) and button.title == "LOAD":
                    with open("projekt.pkl", "rb") as file:
                        figures = pickle.load(file)

            for fig in figures:
                if fig.is_clicked(event.pos):
                    isMoving = True
                    chosenfigure = fig

        elif event.type == pygame.MOUSEBUTTONUP:
            chosenfigure = None
            isMoving = False
        elif event.type == pygame.MOUSEMOTION:
            if isMoving:
                x, y = event.pos
                chosenfigure.setPosition(x, y)


    screen.fill(BACKGROUND_COLOR)

    for fig in figures:
        fig.draw(screen)

    for button in buttons:
        button.draw(screen)

    text = font.render(f"Liczba figur: {len(figures)}", True, BLACK_COLOR)
    screen.blit(text, (10, 580))

    pygame.display.flip()