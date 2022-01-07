from distutils import text_file

class Puzzles:
    _puzzles = list()
    puzzle_1m = "../sudoku-puzzles/1MP.txt"
    solution_1m = "../sudoku-puzzles/1MS.txt"
    puzzle_10m = "../sudoku-puzzles/10MP.txt"
    solution_10m = "../sudoku-puzzles/10MS.txt"
    puzzle_100 = "../sudoku-puzzles/100P.txt"
    solution_100 = "../sudoku-puzzles/100S.txt"
    puzzle_1000 = "../sudoku-puzzles/1000P.txt"
    solution_1000 = "../sudoku-puzzles/1000S.txt"
    puzzle_5000 = "../sudoku-puzzles/5000P.txt"
    solution_5000 = "../sudoku-puzzles/5000S.txt"
    puzzle_10000 = "../sudoku-puzzles/10000P.txt"
    solution_10000 = "../sudoku-puzzles/10000S.txt"
    puzzle_100000 = "/Users/dave/code/GitHub/sudoku-puzzles/sudoku-puzzles/100000P.txt"
    puzzle_easy50 = "../sudoku-puzzles/easy50.txt"
    puzzle_hardest = "../sudoku-puzzles/hardest.txt"
    puzzle_top95 = "../sudoku-puzzles/top95.txt"

    def __init__(self, filename=None):

        cols = "123456789"
        rows = "ABCDEFGHI"
        if filename is None:
            filename = self._100Failed1
        print(f"Loading file {filename}")
        self._squares = [a + b for a in rows for b in cols]
        pf = text_file.TextFile(filename)
        self._puzzles = pf.readlines()
        pf.close()

    def get_number_of_puzzles(self):
        return len(self._puzzles)

    def get_puzzle(self, num) -> str:
        if 0 <= num < self.get_number_of_puzzles():
            return self._puzzles[num]
        else:
            raise IndexError(f"max puzzle number is {len(self._puzzles) - 1} ")
