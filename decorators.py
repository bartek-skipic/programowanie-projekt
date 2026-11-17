import logging
from functools import wraps
from statistics import median
from time import perf_counter


def log_operation(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        logging.info("Start: %s", function.__name__)
        result = function(*args, **kwargs)
        logging.info("Koniec: %s", function.__name__)
        return result

    return wrapper


def measure(repeats: int):
    if repeats < 1:
        raise ValueError("Liczba powtórzeń musi być dodatnia.")

    def decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            times = []
            for _ in range(repeats):
                start = perf_counter()
                result = function(*args, **kwargs)
                times.append(perf_counter() - start)

            return result, median(times)

        return wrapper

    return decorate