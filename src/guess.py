import copy


class Guess:
    puzzle_state = list()
    square = int()
    guess = int()

    def __init__(self, puzzle: list, allowable_values: list, square: int, guess: int):
        self.puzzle = copy.deepcopy(puzzle)
        self.allowable_values = copy.deepcopy(allowable_values)
        self.square = square
        self.guess = guess

    def __repr__(self):
        return f"{self.square_to_text(self.square)} {self.guess}"

    @staticmethod
    def square_to_text(sq: int) -> str:
        c = int(sq % 9)
        r = int(sq / 9)
        return chr(ord("A") + r) + chr(ord("1") + c)
