from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from statistics import median
from time import perf_counter

from figure_coverage import count_covered_pixels


def count_sequentially(parts):
    return sum(count_covered_pixels(part) for part in parts)


def count_with_threads(parts):
    with ThreadPoolExecutor(max_workers=2) as executor:
        return sum(executor.map(count_covered_pixels, parts))


def count_with_processes(parts):
    with ProcessPoolExecutor(max_workers=2) as executor:
        return sum(executor.map(count_covered_pixels, parts))


def main():
    width, height = 800, 600

    # Jeden piksel nieprzezroczysty i jeden przezroczysty, na zmianę.
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
        times = []

        for _ in range(5):
            start = perf_counter()
            result = count(parts)
            times.append(perf_counter() - start)

            if result != expected:
                raise RuntimeError(f"{name}: oczekiwano {expected}, wyszło {result}")

        print(f"{name:14} {median(times) * 1000:8.2f} ms | {result} pikseli")


if __name__ == "__main__":
    main()