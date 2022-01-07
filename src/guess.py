class Guess:
    puzzle_string = str()
    square = str()
    guess = str()

    def __init__(self, puzzle_string :str, square :str, guess :str):
        self.puzzle_string = puzzle_string
        self.square = square
        self.guess = guess

    def __repr__(self):
        return f"{self.square} {self.guess}"
