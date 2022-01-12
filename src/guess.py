import copy


class Guess:
    puzzle = [0] * 81
    allowable_values = [0] * 81
    square = int()
    guess = int()

    def __init__(self, puzzle: list, allowable_values: list, square: int, guess: int):
        # self.puzzle = copy.deepcopy(puzzle)
        self.puzzle = puzzle[:]
        self.allowable_values = allowable_values[:]
        # self.allowable_values = copy.deepcopy(allowable_values)
        # for i in range(81):
        #     self.puzzle[i] = puzzle[i]
        #     self.allowable_values[i] = allowable_values[i]

        self.square = square
        self.guess = guess

    def __repr__(self):
        return f"{self.square_to_text(self.square)} {self.guess_to_text(self.guess)}"

    @staticmethod
    def square_to_text(sq: int) -> str:
        c = int(sq % 9)
        r = int(sq / 9)
        return chr(ord("A") + r) + chr(ord("1") + c)

    @staticmethod
    def guess_to_text(g: int) -> str:
        for i in range(9):
            if (g >> i) & 1 != 0:
                return str(i)
        return " "