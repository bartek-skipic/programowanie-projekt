import argparse
import re

PROJECT_NAME = re.compile(r"[A-Za-z0-9_-]{1,40}")
HEX_COLOR = re.compile(
    r"#(?P<red>[0-9a-f]{2})(?P<green>[0-9a-f]{2})(?P<blue>[0-9a-f]{2})",
    re.IGNORECASE,
)


def parse_project_name(value: str) -> str:
    if PROJECT_NAME.fullmatch(value) is None:
        raise argparse.ArgumentTypeError(
            "Nazwa projektu musi mieć 1–40 znaków: litery A–Z, cyfry, _ lub -."
        )
    return value


def parse_color(value: str) -> tuple[int, int, int]:
    match = HEX_COLOR.fullmatch(value)
    if match is None:
        raise argparse.ArgumentTypeError("Podaj kolor w formacie #RRGGBB.")

    return (
        int(match["red"], 16),
        int(match["green"], 16),
        int(match["blue"], 16),
    )