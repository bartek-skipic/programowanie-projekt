Edytor figur w Pygame

Projekt na zaliczenie przedmiotu Zaawansowane techniki programowania w języku Python. Program pozwala dodawać kwadraty, trójkąty i koła, przesuwać je myszą oraz zapisywać i wczytywać rysunek. Potrafi też obliczyć, jaki procent okna zajmują figury.

Uruchomienie

Potrzebny jest Python 3.12 lub nowszy i biblioteka Pygame. Projekt był uruchamiany na Macu z Pythonem 3.12.

Przy pierwszym uruchomieniu wpisz w terminalu, w katalogu projektu:

    python3.12 -m venv .venv312
    source .venv312/bin/activate
    python -m pip install pygame
    python window.py

Przy kolejnych uruchomieniach wystarczą dwie ostatnie czynności:

    source .venv312/bin/activate
    python window.py

Można też wybrać nazwę zapisu i kolor figur:

    python window.py --project test-1 --color '#ff8800'

W tym przykładzie rysunek będzie zapisany w pliku test-1.pkl, a nowe figury będą pomarańczowe. Bez podania argumentów plik nazywa się projekt.pkl, a kolory figur są losowe.

Obsługa programu

Przyciski KWADRAT, TROJKAT i OKRAG dodają figury. Figurę można przesunąć, przytrzymując na niej przycisk myszy. Gdy figury się nakładają, wybierana jest ta dodana jako ostatnia.

SAVE zapisuje rysunek, a LOAD go wczytuje. Plik zapisu znajduje się w katalogu, z którego uruchomiono program. Zapis i odczyt działają w osobnym wątku. Komunikaty o zakończeniu operacji i błędach pojawiają się w terminalu.

Klawisz P uruchamia liczenie powierzchni zajętej przez figury. Wynik pojawia się w terminalu. Nakładające się fragmenty liczone są raz. Obliczenia wykonują dwa procesy, a okno czeka na wynik.

Na dole okna widać liczbę wszystkich figur i liczbę kół.

Wykorzystane zagadnienia

- Dekoratory funkcji - decorators.py, log_operation i measure(repeats). log_operation jest używany przy save_project i load_project w window.py.
- Dekorator metody - button.py, only_enabled przy Button.is_clicked. Korzysta z self.enabled.
- Property z setterem - button.py, Button.enabled. Setter sprawdza, czy przypisana wartość jest typu bool.
- Iterator - figure_iterator.py, FigureIterator z metodami __iter__ i __next__. Używany podczas rysowania figur.
- Generator - window.py, figures_at. Zwraca przez yield figury znajdujące się pod kursorem.
- Wyrażenie generujące - window.py, liczenie kół w zmiennej circle_count.
- Wyrażenia regularne - validation.py, parse_project_name i parse_color. Kolor jest rozbijany na nazwane grupy red, green i blue.
- Wątki - window.py, ThreadPoolExecutor do zapisu i odczytu. Queue przekazuje wyniki do głównej pętli. pending_io pozwala obsługiwać jedną operację plikową naraz.
- Procesy - figure_coverage.py, calculate_coverage i count_covered_pixels. ProcessPoolExecutor dzieli liczenie pikseli na dwa procesy.
- GIL - gil_benchmark.py, porównanie wykonania sekwencyjnego, wątków i procesów.

Dekoratory funkcji korzystają z functools.wraps. Przed oddaniem trzeba jeszcze sprawdzić użycie measure(repeats) oraz końcową wersję only_enabled i Button.enabled.

Wyniki pomiarów i wnioski

Benchmark uruchamia się poleceniem:

    python gil_benchmark.py

Skrypt sam generuje obraz 800 na 600 pikseli. Połowa pikseli jest zajęta, więc poprawny wynik to 240 000. Każdy wariant wykonuje te same obliczenia na tych samych danych. Podane czasy to mediany z pięciu prób. Uwzględniają również uruchomienie i zamknięcie puli wątków lub procesów.

- Sekwencyjnie - 21,33 ms, 240 000 zajętych pikseli.
- 2 wątki - 20,70 ms, 240 000 zajętych pikseli.
- 2 procesy - 58,11 ms, 240 000 zajętych pikseli.

Wszystkie trzy warianty policzyły 240 000 zajętych pikseli. Wykonanie sekwencyjne zajęło 21,33 ms, a dwa wątki 20,70 ms, więc różnica wyniosła tylko 0,63 ms. Na podstawie tak małej różnicy trudno mówić o przyspieszeniu dzięki wątkom. W CPythonie 3.12 GIL pozwala tylko jednemu wątkowi naraz wykonywać kod Pythona w danym procesie. Osobne procesy mogą liczyć równolegle, ale w tym teście zajęło im to 58,11 ms, czyli około 2,7 razy dłużej niż sekwencyjnie. Przy tak małym obrazie uruchomienie procesów i przesłanie danych prawdopodobnie zajęło więcej czasu, niż udało się zaoszczędzić na samych obliczeniach.

Problemy podczas pracy

Przy dodawaniu procesów kod uruchamiający aplikację został przeniesiony do main(). Na końcu pliku dodany został warunek if __name__ == "__main__". Dzięki temu proces roboczy może zaimportować moduł bez ponownego otwierania okna.

Zapis w tle wymagał kopii figur wykonanej przez deepcopy. Dzięki temu przesuwanie figur w oknie nie zmienia danych przekazanych do zapisu. Wynik operacji wraca przez Queue i jest odbierany w głównej pętli programu.

Przy obliczaniu powierzchni trzeba było uwzględnić nakładanie figur. Dlatego figury są rysowane na osobnej przezroczystej powierzchni, a program liczy zajęte piksele.

Sprawdzenie działania

Rysunek testowy można utworzyć w aplikacji, zapisać przez SAVE i ponownie wczytać przez LOAD. Pusty rysunek powinien dać wynik 0.00%. Jeden kwadrat 100 na 100 pikseli, mieszczący się w oknie, powinien dać 2.08%. Drugi kwadrat w tym samym miejscu powinien pozostawić ten wynik. Po rozsunięciu obu kwadratów wynik powinien wynieść 4.17%, jeśli oba mieszczą się w oknie.

Dane testowe do benchmarku są generowane przy każdym uruchomieniu skryptu.

Elementy dodatkowe

Projekt ma interfejs graficzny w Pygame, argumenty uruchomienia obsługiwane przez argparse i logowanie operacji przez logging.
