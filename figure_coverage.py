from concurrent.futures import ProcessPoolExecutor


def count_covered_pixels(pixels: bytes) -> int:
    """Policz piksele z niezerową przezroczystością w danych RGBA."""
    return sum(pixels[index] > 0 for index in range(3, len(pixels), 4))


def calculate_coverage(pixels: bytes, width: int, height: int) -> float:
    """Zwróć procent powierzchni zajętej przez figury."""
    middle = (height // 2) * width * 4
    parts = (pixels[:middle], pixels[middle:])

    with ProcessPoolExecutor(max_workers=2) as executor:
        covered = sum(executor.map(count_covered_pixels, parts))

    return 100 * covered / (width * height)