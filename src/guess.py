class Guess:
    puzzle_state = list()
    square = int()
    guess = int()

    def __init__(self, puzzle_state :list, square :int, guess :int):
        self.puzzle_state = puzzle_state
        self.square = square
        self.guess = guess

    def __repr__(self):
        return f"{self.square} {self.guess}"


