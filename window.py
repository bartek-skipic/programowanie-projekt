import argparse
from validation import parse_color, parse_project_name
import pygame
import sys
import random
import pickle

import logging
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path
from queue import Empty, Queue

from decorators import log_operation

from figure_iterator import FigureIterator
from button import Button
from oval import Oval
from rectangle import Rectangle
from triangle import Triangle

def random_color():
    if args.color is not None:
        return args.color
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

parser = argparse.ArgumentParser()
parser.add_argument("--project", type=parse_project_name, default="projekt")
parser.add_argument("--color", type=parse_color)
args = parser.parse_args()

project_file = f"{args.project}.pkl"

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

@log_operation
def save_project(filename, saved_figures):
    path = Path(filename)
    temporary = path.with_suffix(".pkl.tmp")
    try:
        with temporary.open("wb") as file:
            pickle.dump(saved_figures, file)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


@log_operation
def load_project(filename):
    with open(filename, "rb") as file:
        return pickle.load(file)


logging.basicConfig(level=logging.INFO)
io_pool = ThreadPoolExecutor(max_workers=1)
io_results = Queue()
pending_io = None

def figures_at(figures, position):
    for fig in reversed(figures):
        if fig.is_clicked(position):
            yield fig

while True:
    try:
        completed = io_results.get_nowait()
    except Empty:
        pass
    else:
        try:
            result = completed.result()
            if pending_io == "load":
                figures = result
                chosenfigure = None
                isMoving = False
                print(f"Wczytano {project_file}")
            else:
                print(f"Zapisano {project_file}")
        except (OSError, EOFError, pickle.PickleError) as error:
            print(f"Błąd operacji na pliku: {error}")
        finally:
            pending_io = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            io_pool.shutdown(wait=True)
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
                   if pending_io is None:
                        pending_io = "save"
                        snapshot = deepcopy(figures)
                        future = io_pool.submit(save_project, project_file, snapshot)
                        future.add_done_callback(io_results.put)
                elif button.is_clicked(event.pos) and button.title == "LOAD":
                    if pending_io is None:
                        pending_io = "load"
                        future = io_pool.submit(load_project, project_file)
                        future.add_done_callback(io_results.put)

            for fig in figures:
                if fig.is_clicked(event.pos):
                    chosenfigure = next(figures_at(figures, event.pos), None)
                    isMoving = chosenfigure is not None

        elif event.type == pygame.MOUSEBUTTONUP:
            chosenfigure = None
            isMoving = False
        elif event.type == pygame.MOUSEMOTION:
            if isMoving:
                x, y = event.pos
                chosenfigure.setPosition(x, y)


    screen.fill(BACKGROUND_COLOR)

    for fig in FigureIterator(figures):
        fig.draw(screen)

    for button in buttons:
        button.draw(screen)

    circle_count = sum(1 for fig in figures if isinstance(fig, Oval))
    text = font.render(
    f"Liczba figur: {len(figures)} | Koła: {circle_count}",
    True,
    BLACK_COLOR,
)
    screen.blit(text, (10, 580))

    pygame.display.flip()