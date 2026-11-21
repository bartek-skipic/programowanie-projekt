import argparse
import logging
import pickle
import random
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path
from queue import Empty, Queue

from collections.abc import Iterator
from geometricfigure import GeometricFigure

import pygame

from button import Button
from decorators import log_operation
from figure_coverage import calculate_coverage
from figure_iterator import FigureIterator
from oval import Oval
from rectangle import Rectangle
from triangle import Triangle
from validation import parse_color, parse_project_name


BACKGROUND_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)


def random_color() -> tuple[int, int, int]:
    """Wylosuj kolor RGB."""
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


@log_operation
def save_project(
    filename: str,
    saved_figures: list[GeometricFigure],
) -> None:
    """Zapisz figury przez plik tymczasowy."""
    path = Path(filename)
    temporary = path.with_suffix(".pkl.tmp")
    try:
        with temporary.open("wb") as file:
            pickle.dump(saved_figures, file)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


@log_operation
def load_project(filename: str) -> list[GeometricFigure]:
    """Wczytaj figury z pliku projektu."""
    with open(filename, "rb") as file:
        return pickle.load(file)


def figures_at(
    figures: list[GeometricFigure],
    position: tuple[int, int],
) -> Iterator[GeometricFigure]:
    """Zwracaj figury pod kursorem od ostatnio narysowanej."""
    for fig in reversed(figures):
        if fig.is_clicked(position):
            yield fig


def main() -> None:
    """Uruchom okno aplikacji i obsługę zdarzeń."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=parse_project_name, default="projekt")
    parser.add_argument("--color", type=parse_color)
    args = parser.parse_args()

    project_file = f"{args.project}.pkl"
    logging.basicConfig(level=logging.INFO)

    pygame.init()
    try:
        size = (800, 600)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Projekt")
        font = pygame.font.SysFont("Arial", 16)

        figures = []
        buttons = [
            Button(0, 0, WHITE_COLOR, BLACK_COLOR, "KWADRAT"),
            Button(100, 0, WHITE_COLOR, BLACK_COLOR, "TROJKAT"),
            Button(200, 0, WHITE_COLOR, BLACK_COLOR, "OKRAG"),
            Button(300, 0, WHITE_COLOR, BLACK_COLOR, "SAVE"),
            Button(400, 0, WHITE_COLOR, BLACK_COLOR, "LOAD"),
        ]

        chosenfigure = None
        io_results = Queue()
        pending_io = None

        with ThreadPoolExecutor(max_workers=1) as io_pool:
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
                            print(f"Wczytano {project_file}")
                        else:
                            print(f"Zapisano {project_file}")
                    except (OSError, EOFError, pickle.PickleError) as error:
                        print(f"Błąd operacji na pliku: {error}")
                    finally:
                        pending_io = None

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for button in buttons:
                            if not button.is_clicked(event.pos):
                                continue

                            if button.title in ("KWADRAT", "TROJKAT", "OKRAG"):
                                color = args.color if args.color is not None else random_color()

                                if button.title == "KWADRAT":
                                    figures.append(Rectangle(400, 300, 100, 100, color))
                                elif button.title == "TROJKAT":
                                    figures.append(Triangle(400, 300, color))
                                else:
                                    figures.append(Oval(400, 300, 100, color))

                            elif button.title == "SAVE" and pending_io is None:
                                snapshot = deepcopy(figures)
                                pending_io = "save"
                                future = io_pool.submit(save_project, project_file, snapshot)
                                future.add_done_callback(io_results.put)

                            elif button.title == "LOAD" and pending_io is None:
                                pending_io = "load"
                                future = io_pool.submit(load_project, project_file)
                                future.add_done_callback(io_results.put)

                        chosenfigure = next(figures_at(figures, event.pos), None)

                    elif event.type == pygame.MOUSEBUTTONUP:
                        chosenfigure = None

                    elif event.type == pygame.MOUSEMOTION:
                        if chosenfigure is not None:
                            chosenfigure.setPosition(*event.pos)

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        width, height = screen.get_size()
                        drawing = pygame.Surface((width, height), pygame.SRCALPHA)

                        for fig in FigureIterator(figures):
                            fig.draw(drawing)

                        pixels = pygame.image.tobytes(drawing, "RGBA")
                        coverage = calculate_coverage(pixels, width, height)
                        print(f"Figury zajmują {coverage:.2f}% powierzchni")

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
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()