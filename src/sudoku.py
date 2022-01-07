from guess import Guess
import random
from constants import *


class Sudoku:
    puzzle = [allClear for s in squares]
    allowable_values = [allSet for s in squares]

    digits = "123456789"
    rows = "ABCDEFGHI"
    cols = "123456789"
    guess_list = list()

    def __init__(self, puzz_text: str = None) -> None:
        """
        initializes class Puzzle
        :param puzz_text: (str) a puzzle string
        """

        self.clear_puzzle()
        if puzz_text is not None:
            file_ok = True
            # check to make sure puzz is a correctly formated string
            # remove carriage returns
            puzz_text.replace("\n", "")
            # replace 0 with periods
            puzz_text.replace("0", ".")
            # verify length
            if len(puzz_text) != 81:
                file_ok = False
            if puzz_text.replace(".", "").isnumeric() is not True:
                file_ok = False
            if file_ok:
                self.set_puzzle(puzz_text)

#     @staticmethod
#     def _cross(a, b) -> list:
#         """
#         computes a vector cross product of each element in iterables A and B.
#         For example, if you pass in _cross("123","ABC"), the return list will be:
#             _cross("123","ABC") - ['1A', '1B', '1C', '2A', '2B', '2C', '3A', '3B', '3C']
#             _cross("1234","ABC")) - ['1A', '1B', '1C', '2A', '2B', '2C', '3A', '3B', '3C', '4A', '4B', '4C']
#         :param a: first iterable
#         :param b: second iterable
#         :return: a list containing the cross product of A and B
#         """
#         return [aa+bb for aa in a for bb in b]

#     def set_puzzle(self, puz_text: str) -> None:
#         if len(puz_text) == 81:
#             self.puzzle = dict(zip(self.squares, puz_text))
#             for s in self.squares:
#                 self.allowable_values[s] = self.digits
#         else:
#             raise ValueError("String passed to set_puzzle must be 81 chars long")
#         for s in self.squares:
#             if self.puzzle[s] == ".":
#                 self.puzzle[s] = "."
#             else:
#                 self.set_value(s, self.puzzle[s])

#     def clear_puzzle(self):
#         for u in self.units:
#             self.puzzle[u] = '.'
#             self.allowable_values[u] = self.digits

#     def get_puzzle_text(self) -> str:
#         return "".join(self.puzzle[u] for u in self.squares)

#     def get_allowable_values_text(self) -> str:
#         retval = ""
#         for u in self.squares:
#             retval = retval + self.allowable_values[u]
#             if u != "I9":
#                 retval += "|"
#         return retval

#     def get_packed_puzzle(self) -> str:
#         return self.get_puzzle_text() + "_" + self.get_allowable_values_text()

#     def unpack_puzzle(self, text):
#         puz_allow = text.split("_")
#         self.puzzle = dict(zip(self.squares, puz_allow[0]))
#         allow = puz_allow[1].split("|")
#         self.allowable_values = dict(zip(self.squares, allow))


# ################################################################################
# # puzzle printing functions
# ################################################################################

#     def pretty_print(self, what, title=None):
#         """prints a formatted representation of a puzzle
#         """
#         header = "     1   2   3    4   5   6    7   8   9"
#         top = "  ========================================="
#         row_sep = "  || --------- || --------- || --------- ||"
#         col_sep = "||"
#         num_sep = "|"
#         row_num = -1
#         col_num = -1
#         print()
#         if title is not None:
#             print(title)
#         print(header)
#         print(top)
#         for r in self.rows:
#             print(f'{r} {col_sep}', end="")
#             for c in self.cols:
#                 index = r + c
#                 if what[index] == 0:
#                     print("  ", end="")
#                 else:
#                     print(f" {what[index]}", end="")
#                 if (col_num - 1) % 3 == 0:
#                     print(f" {col_sep}", end="")
#                 else:
#                     print(f" {num_sep}", end="")
#                 col_num += 1
#             row_num += 1
#             print()
#             if row_num == 8:
#                 print(top)
#             elif (row_num + 1) % 3 == 0:
#                 print(row_sep)

#     def print_allowable_values(self):
#         """prints a formatted representation of a puzzle
#         """
#         what = self.allowable_values
#         header = "          1           2         3             4           5           6             7           8          9"
#         top = "  ================================================================================================================="
#         row_sep = "  || --------------------------------- || --------------------------------- || --------------------------------- ||"
#         col_sep = "||"
#         num_sep = "|"
#         row_num = -1
#         col_num = -1
#         print("------ Allowable Values ------")
#         print(header)
#         print(top)
#         for r in self.rows:
#             print(f'{r} {col_sep}', end="")
#             for c in self.cols:
#                 index = r+c
#                 if len(what[index]) == 1:
#                     print("          ", end="")
#                 else:
#                     print(f" {what[index]:9}", end="")
#                 if (col_num-1) % 3 == 0:
#                     print(f" {col_sep}", end="")
#                 else:
#                     print(f" {num_sep}", end="")
#                 col_num += 1
#             row_num += 1
#             print()
#             if row_num == 8:
#                 print(top)
#             elif (row_num + 1) % 3 == 0:
#                 print(row_sep)
#         print()

#     def print_number_of_available_values(self):
#         nv = dict()
#         for r in self.rows:
#             for c in self.cols:
#                 index = r+c
#                 nv[index] = len(self.allowable_values[index])
#         self.pretty_print(nv, "------ Number of Allowable Values ------")

#     def print_puzzle(self, title=None):
#         self.pretty_print(self.puzzle, title)

#     def get_number_of_open_squares(self):
#         num = 0
#         for u in self.units:
#             if len(self.allowable_values[u]) > 0:
#                 num += 1
#         return num

# ################################################################################
# # puzzle solving functions
# ################################################################################

#     def remove_guess(self, square: str, value: str):
#         self.allowable_values[square] = self.allowable_values[square].replace(value, "")

#     def guesses_remain(self) -> bool:
#         for s in self.squares:
#             if len(set(self.digits) - set(self.allowable_values[s])) < 9:
#                 return True
#         return False

#     def set_value(self, square, value) -> bool:
#         if self.allowable_values[square].find(value) == -1:
#             return False
#             # raise ValueError(f"You tried to set {value} into square {square}. Not in allowable values")
#         self.allowable_values[square] = ""
#         self.puzzle[square] = str(value)
#         for s in self.peers[square]:
#             self.allowable_values[s] = self.allowable_values[s].replace(value, "")
#         return True

#     def solve_ones(self):
#         set_some = True
#         while set_some:
#             set_some = False
#             with_one = [s for s in self.allowable_values if len(self.allowable_values[s]) == 1]
#             if len(with_one) > 0:
#                 for s in with_one:
#                     if self.allowable_values[s] != "":
#                         self.set_value(s, self.allowable_values[s])
#                         set_some = True
#                 # self.solve_ones()
#             # look in each unit and see if any value appears only one time
#             # create a list of all allowable values in a unit (rol, col, square)
#             for ul in self.unitlist:
#                 all_allowable = "".join(self.allowable_values[u] for u in ul)
#                 for d in self.digits:
#                     if all_allowable.count(d) == 1:
#                         for u in ul:
#                             if self.allowable_values[u].count(d) == 1:
#                                 self.set_value(u, d)
#                                 set_some = True

#     def is_puzzle_solved(self) -> bool:
#         # def unitsolved(unit): return set(self.puzzle[s] for s in unit) == set(self.digits)
#         # return all(unitsolved(unit) for unit in self.unitlist)
#         # A puzzle is solved if each unit is a permutation of the digits 1 to 9.
#         sd = set(self.digits)
#         if set(self.puzzle[u] for ul in self.unitlist for u in ul) != sd:
#             return False
#         return True
#         # for each unit in a unit list, make a set and compare to all digits
#         # and do that for each unitlist
#         # return all(set(self.puzzle[u] for u in ul) == set(self.digits) for ul in self.unitlist)

#     def get_guess(self):
#         min_number = min(len(self.allowable_values[s]) for s in self.squares if len(self.allowable_values[s]) > 0)
#         subset = [s for s in self.squares if len(self.allowable_values[s]) == min_number]
#         square = self.get_one_of(subset)
#         guess = self.get_one_of(self.allowable_values[square])
#         return guess, square

#     def pop_guess(self):
#         # pop off last guess
#         lg = self.guess_list.pop()
#         # replace teh puzzle from before the last guess
#         self.unpack_puzzle(lg.puzzle_string)
#         # remove the last guess from list of available guesses
#         self.remove_guess(lg.square, lg.guess)

#     def start_guessing(self):
#         # max_depth = 0
#         # dead_ends = 0
#         self.guess_list = []
#         while not self.is_puzzle_solved():
#             while self.guesses_remain():
#                 num, square = self.get_guess()
#                 guess = self.get_one_of(self.allowable_values[square])
#                 d = Guess(self.get_packed_puzzle(), square, guess)
#                 self.guess_list.append(d)
#                 self.set_value(square, guess)
#                 self.solve_ones()
#                 # max_depth = max(max_depth,len(self.guess_list))
#                 if not self.is_puzzle_solved() and not self.guesses_remain():
#                     self.pop_guess()
#             if not self.is_puzzle_solved():
#                 # dead_ends += 1
#                 # print("dead end")
#                 # if we get here, we ran out of guesses.  so.....
#                 # pop an extra guess off of the stack and continue
#                 self.pop_guess()

#     @staticmethod
#     def get_one_of(seq):
#         return random.choice(seq)

#     @staticmethod
#     def shuffled(seq):
#         # Return a randomly shuffled copy of the input sequence.
#         seq = list(seq)
#         random.shuffle(seq)
#         return seq

#     def solve_puzzle(self) -> bool:

#         self.solve_ones()
#         if self.is_puzzle_solved():
#             return True
#         else:
#             self.start_guessing()
#             return self.is_puzzle_solved()

#     def random_puzzle(self, n=17):
#         # self.allowable = dict((s, self.digits) for s in self.squares)
#         self.clear_puzzle()
#         for s in self.shuffled(self.squares):
#             if not self.set_value(s,  random.choice(self.allowable_values[s])):
#                 break
#             ds = [self.puzzle[s] for s in self.squares if len(self.allowable_values[s]) == 0]
#             if len(ds) >= n and len(set(ds)) >= 8:
#                 return ''.join(self.puzzle[s] if len(self.allowable_values[s]) == 0 else '.' for s in self.squares)
#         return self.random_puzzle(n)  # Give up and make a new puzzle
