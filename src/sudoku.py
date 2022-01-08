from guess import Guess
import random
from constants import *
from io import StringIO
import sys



class Sudoku:
    puzzle = [ALLCLEAR for s1 in SQUARES]
    allowable_values = [ALLSET for s2 in SQUARES]
    guess_list = list()

    def __init__(self, puzz_text: str = None) -> None:
        """
        initializes class Puzzle
        :param puzz_text: (str) a puzzle string
        """
        self.clear_puzzle()
        print(self.get_puzzle_text())
        if puzz_text is not None:
            file_ok = True
            # check to make sure puzz is a correctly formated string
            # remove carriage returns
            puzz_text.replace("\n", "")
            # replace 0 with periods
            puzz_text.replace("0", ".")
            # verify length
            if len(puzz_text) < 81:
                file_ok = False
            if puzz_text.replace(".", "").isnumeric() is not True:
                file_ok = False
            if file_ok:
                self.set_puzzle(puzz_text)

    def set_puzzle(self, puz_text: str) -> None:
        if len(puz_text) >= 81:
            pass
        else:
            raise ValueError("String passed to set_puzzle must be 81 chars long")
        self.clear_puzzle()
        for s in SQUARES:
            if puz_text[s] == '.' or puz_text[s] == '0':
                self.puzzle[s] = ALLCLEAR
            else:
                self.set_value(s, BITMASK[int(puz_text[s]) - 1])

    def clear_puzzle(self):
        for s in SQUARES:
            self.puzzle[s] = ALLCLEAR
            self.allowable_values[s] = ALLSET

    def set_value(self, s: int, bm: int) -> bool:
        if self.allowable_values[s] & bm == 0:
            return False
        if bm == ALLCLEAR:
            self.puzzle[s] = ALLCLEAR
        else:
            self.puzzle[s] = bm
            self.allowable_values[s] = ALLCLEAR
        for p in PEERS[s]:
            self.allowable_values[p] &= ~bm
        return True

# ################################################################################
# utility functions
# ################################################################################

    @staticmethod
    def bitmask_to_string(bm: int) -> str:
        if bm == ALLCLEAR:
            return "."
        for i in range(9):
            if bm & BITMASK[i] != 0:
                return chr(ord('1') + i)

    def get_puzzle_text(self) -> str:
        return "".join(self.bitmask_to_string(self.puzzle[s]) for s in SQUARES)

    def get_number_of_open_squares(self):
        num = 0
        for s in SQUARES:
            if len(self.allowable_values[s] != ALLCLEAR):
                num += 1
        return num

    def bitmask_to_value(self,  num: int) -> str:
        retval = ""
        if num == BITMASK[9]:
            return "."
        elif num == ALLCLEAR:
            return " "
        if self.number_of_bits_set(num) == 1:
            for i in range(9):
                if num >> i & 1 != 0:
                    return f" {i+1}"
        else:
            for i in range(9):
                if num & BITMASK[i] != 0:
                    retval += f"{i+1}"
        return retval

    @staticmethod
    def number_of_bits_set(num: int) -> int:
        c = int()
        c = (num * 0x200040008001 & 0x111111111111111) % 0xf
        return c

        # result = 0
        # stop = (num != 0)
        # while stop:
        #     num &= num - 1
        #     result += 1
        #     stop = (num != 0)
        # return result


# ################################################################################
# # puzzle printing functions
# ################################################################################

    def pretty_print(self, what, title=None):
        """prints a formatted representation of a puzzle
        """
        header = "     1   2   3    4   5   6    7   8   9"
        top = "  ========================================="
        row_sep = "  || --------- || --------- || --------- ||"
        col_sep = "||"
        num_sep = "|"
        row_num = -1
        col_num = -1
        if title is not None:
            print(title)
        print(header)
        print(top)
        for r in range(9):
            print(f'{chr(ord("A") + r)} {col_sep}', end="")
            for c in range(9):
                index = r*9 + c
                if what[index] == ALLCLEAR:
                    print(" .", end="")
                else:
                    print(f"{self.bitmask_to_value(what[index])}", end="")
                if (col_num - 1) % 3 == 0:
                    print(f" {col_sep}", end="")
                else:
                    print(f" {num_sep}", end="")
                col_num += 1
            row_num += 1
            print()
            if row_num == 8:
                print(top)
            elif (row_num + 1) % 3 == 0:
                print(row_sep)

    def print_allowable_values(self, title: str):
        """prints a formatted representation of a puzzle
        """
        what = self.allowable_values
        header = "          1           2         3             4           5           6             7           8          9"
        top = "  ================================================================================================================="
        row_sep = "  || --------------------------------- || --------------------------------- || --------------------------------- ||"
        col_sep = "||"
        num_sep = "|"
        row_num = -1
        col_num = -1
        if title is not None:
            print(title)
        print(header)
        print(top)
        for r in range(9):
            print(f'{chr(ord("A") + r)} {col_sep}', end="")
            for c in range(9):
                index = r*9 + c
                if what[index] == ALLCLEAR:
                    print("          ", end="")
                else:
                    print(f" {self.bitmask_to_value(what[index]):9}", end="")
                if (col_num-1) % 3 == 0:
                    print(f" {col_sep}", end="")
                else:
                    print(f" {num_sep}", end="")
                col_num += 1
            row_num += 1
            print()
            if row_num == 8:
                print(top)
            elif (row_num + 1) % 3 == 0:
                print(row_sep)
        print()

    # def print_number_of_available_values(self):
    #     nv = [BITMASK[self.number_of_bits_set(self.allowable_values[s])-2 ] for s in SQUARES]
    #     self.pretty_print(nv, "------ Number of Allowable Values ------")

    def print_puzzle(self, title: str = None):
        self.pretty_print(self.puzzle, title)

    def print_puzzle_and_allowable_values(self, title: str = None):
        puzzle_out = StringIO()
        values_out = StringIO()
        # Replace default stdout (terminal) with our stream
        sys.stdout = puzzle_out
        self.print_puzzle(title)
        sys.stdout = values_out
        self.print_allowable_values(title)
        sys.stdout = sys.__stdout__
        pout = puzzle_out.getvalue()
        vout = values_out.getvalue()
        pout_lines = pout.split("\n")
        vout_lines = vout.split("\n")
        for l in range(len(pout_lines)):
            print(pout_lines[l] + "   " + vout_lines[l])




# ################################################################################
# # puzzle solving functions
# ################################################################################

    def solve_ones(self):
        set_some = True
        while set_some:
            while set_some:
                # self.print_puzzle_and_allowable_values()
                set_some = False
                with_one = [s for s in SQUARES if self.number_of_bits_set(self.allowable_values[s]) == 1]
                if len(with_one) > 0:
                    for s in with_one:
                        if self.allowable_values[s] != "":
                            self.set_value(s, self.allowable_values[s])
                            set_some = True
            # look in each unit and see if any value appears only one time
            # create a list of all allowable values in a unit (rol, col, square)
            if self.is_puzzle_solved():
                return
#            self.print_puzzle_and_allowable_values()
            for ul in UNITLIST:
                for b in BITS:
                    bit_count = 0
                    for s in ul:
                        if self.allowable_values[s] & BITMASK[b] != 0:
                            bit_count += 1
                    if bit_count == 1:
                        for s in ul:
                            if self.allowable_values[s] & BITMASK[b] != 0:
                                self.set_value(s, BITMASK[b])
                                set_some = True

    def is_puzzle_solved(self) -> bool:
        # def unitsolved(unit): return set(self.puzzle[s] for s in unit) == set(self.digits)
        # return all(unitsolved(unit) for unit in self.unitlist)
        # A puzzle is solved if each unit is a permutation of the digits 1 to 9.

        for u in UNITLIST:
            oreo = 0
            for s in u:
                oreo |= self.puzzle[s]
            if oreo != ALLSET:
                return False
        return True

        # for each unit in a unit list, make a set and compare to all digits
        # and do that for each unitlist
        # return all(set(self.puzzle[u] for u in ul) == set(self.digits) for ul in self.unitlist)

#     def remove_guess(self, square: str, value: str):
#         self.allowable_values[square] = self.allowable_values[square].replace(value, "")

#     def guesses_remain(self) -> bool:
#         for s in self.squares:
#             if len(set(self.digits) - set(self.allowable_values[s])) < 9:
#                 return True
#         return False


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
