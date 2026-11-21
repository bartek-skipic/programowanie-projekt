from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from decorators import measure
from figure_coverage import count_covered_pixels


@measure(repeats=5)
def count_sequentially(parts: tuple[bytes, ...]) -> int:
    """Policz zajęte piksele sekwencyjnie."""
    return sum(count_covered_pixels(part) for part in parts)


@measure(repeats=5)
def count_with_threads(parts: tuple[bytes, ...]) -> int:
    """Policz zajęte piksele przy użyciu dwóch wątków."""
    with ThreadPoolExecutor(max_workers=2) as executor:
        return sum(executor.map(count_covered_pixels, parts))


@measure(repeats=5)
def count_with_processes(parts: tuple[bytes, ...]) -> int:
    """Policz zajęte piksele przy użyciu dwóch procesów."""
    with ProcessPoolExecutor(max_workers=2) as executor:
        return sum(executor.map(count_covered_pixels, parts))


def main() -> None:
    """Porównaj czas wykonania tych samych obliczeń."""
    width, height = 800, 600

    pixel_pair = bytes((255, 128, 0, 255, 0, 0, 0, 0))
    pixels = pixel_pair * (width * height // 2)

    middle = (height // 2) * width * 4
    parts = (pixels[:middle], pixels[middle:])
    expected = width * height // 2

    methods = (
        ("Sekwencyjnie", count_sequentially),
        ("2 wątki", count_with_threads),
        ("2 procesy", count_with_processes),
    )

    print(f"Obraz {width} × {height} | Oczekiwany wynik: {expected} pikseli")

    for name, count in methods:
        result, elapsed = count(parts)

        if result != expected:
            raise RuntimeError(
                f"{name}: oczekiwano {expected}, wyszło {result}"
            )

        print(f"{name:14} {elapsed * 1000:8.2f} ms | {result} pikseli")


if __name__ == "__main__":
    main()