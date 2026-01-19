HOST = '127.0.0.1'
PORT = 5555

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650
GRID_SIZE = 10
CELL_SIZE = 55
MARGIN = 4


WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREEN = (144, 238, 144)
GREEN_DARK = (34, 139, 34)
RED = (255, 182, 193)
BLUE = (173, 216, 230)
GREY = (220, 220, 220)
DARK_GREY = (80, 80, 80)


BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)

LEVELS = [
    {
        "name": "Poziom 1",
        "grid": [
    ['.', '.', '.', '.', 'K', '.', 'L', '.', '.', '.'],
    ['.', '.', '.', '.', 'O', 'B', 'O', 'L', '.', '.'],
    ['.', '.', '.', 'U', 'R', 'O', 'D', 'A', '.', '.'],
    ['.', '.', '.', '.', 'T', 'R', 'Y', 'K', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', 'K', '.', 'D', '.', '.', '.', '.'],
    ['.', '.', '.', 'O', 'P', 'A', 'D', '.', '.', '.'],
    ['.', '.', 'I', 'M', 'A', 'G', 'O', '.', '.', '.'],
    ['.', '.', '.', 'A', 'R', 'A', 'K', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
],
        "clues": [
            "Poziomo:",
            "- 1/2 denara",
            "- piękno, krasa",
            "- baran rozpłodowy",
            "- deszcz lub śnieg",
            "- dorosły owad",
            "- towar z wadą"
            "",
            "Pionowo:",
            "- ukośnik",
            "- tenisowa arena",
            "- w izbie Lordów",
            "- w ręku dentysty",
            "- krótki sztylet",
            "- zimny deser",
            "- basen portowy",
            "- do pieczęci"

        ]
    },
    {
        "name": "Poziom 2: Sieci",
        "grid": [
    ['.', 'N', '.', 'O', '.', '.', '.', '.', '.', '.'],
    ['.', 'E', '.', 'K', '.', '.', '.', '.', '.', '.'],
    ['U', 'R', 'A', 'N', '.', '.', '.', '.', '.', '.'],
    ['.', 'W', 'L', 'O', 'S', 'I', 'E', '.', '.', '.'],
    ['.', '.', '.', '.', 'T', '.', '.', '.', '.', '.'],
    ['N', 'A', 'N', 'D', 'U', '.', '.', 'R', '.', '.'],
    ['.', 'L', '.', 'Z', 'L', 'O', 'T', 'Y', '.', '.'],
    ['.', 'B', 'O', 'B', 'A', 'S', '.', 'S', '.', '.'],
    ['L', 'U', 'K', 'A', '.', 'E', '.', 'I', '.', '.'],
    ['.', 'M', 'O', 'N', 'I', 'T', '.', 'K', '.', '.']
],
        "clues": [
            "Poziomo:",
            "- obok neptuna",
            "- z niego smyczek",
            "- podobny do strusia",
            "- 100 groszy",
            "- małe dziecko",
            "- puste miejsce",
            "- wzywa do zapłaty",
            "",
            "Pionowo:",
            "- żyłka liścia",
            "- w nim rodzinne zdjęcia",
            "- z tęczówką",
            "- z szybą",
            "- pękate naczynie",
            "- na szyi księdza",
            "- kłuje na łące",
            "- drobna kasza"
        ]
    }
]