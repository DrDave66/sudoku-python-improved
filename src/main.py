import time
import cProfile
import re
from puzzles import Puzzles
from sudoku import Sudoku
from constants import *


# def solve_one_puzzle(filename, num=None) -> None:
#     """
#     solves one puzzle from a file. if no puzzle number is specified, a random one is chosen
#     :param filename: puzzle filename to be opened
#     :param [optional num: puzzle number
#     :return: None
#     """
#     ps = Puzzles(filename)
#     p = Puzzle()
#     if num is None:
#         import random
#         random.seed()
#         num = random.randrange(ps.get_number_of_puzzles())
#     p.set_puzzle(ps.get_puzzle(num))
#     p.print_puzzle()
#     start = time.perf_counter()
#     p.solve_puzzle()
#     end = time.perf_counter()
#     p.print_puzzle()
#     solve_time = end - start
#     solved = p.is_puzzle_solved()
#     print(f"Puzzle {num}, Solved = {solved}, Time = {solve_time:.4f} ms")

# def solve_puzzle_range(filename, puzzle_range=None):
#     ps = Puzzles(filename)
#     p = Puzzle()
#     if puzzle_range is None:
#         puzzle_range = range(ps.get_number_of_puzzles())
#     start = time.perf_counter()
#     solved = 0
#     unsolved = 0
#     end = 0.0
#     for r in puzzle_range:
#         p.set_puzzle(ps.get_pulist()zzle(r))
#         p.solve_puzzle()
#         end = time.perf_counter()
#         if p.is_puzzle_solved():puzzle
#             solved += 1
#         else:
#             unsolved += 1
#     solve_time = end - start
#     average_time = float(solve_time) / float(len(puzzle_range))
#     print(f"Solved = {solved}, Unsolved = {unsolved}, Time = {solve_time:.4f} ms, Average time {average_time:.4f} msec")

# def solve_all_no_stats(filename: str) -> None:
#     ps = Puzzles(filename)
#     p = Puzzle()
#     success = 0
#     failed = 0
#     start = time.perf_counter(list())
#     n = ps.get_number_of_puzzles()
#     i = 0
#     for i in range(n):
#         p.set_puzzle(ps.get_puzzle(i))
#         p.solve_puzzle()

#         if p.is_puzzle_solved():
#             success += 1
#         else:
#             failed += 1
#     percent = float(failed) / float(i+1) * 100.0
#     solve_time = time.perf_counter() - start
#     print(f"Solved {success} of {i+1} puzzles, {failed} unsolved -> {percent:.3f}% in {time.perf_counter()-start:.3f} sec, {solve_time/ps.get_number_of_puzzles()*1000:.4f} msec per puzzle")


# def solve_all_with_stats(filename: str, save_failures:bool =False, usemod:int =0) -> None:
#     """

#     :param filename:
#     :param save_failures:
#     :param usemod:
#     :return:
#     """

#     ps = Puzzles(filename)
#     p = Puzzle()
#     success = 0
#     failed = 0
#     n = ps.get_number_of_puzzles()
#     if usemod == 0:
#         mod = int(n/20)
#     else:
#         mod = usemod
#     if mod == 0:
#         mod = 1
#     start = time.perf_counter()
#     all_failed = list()
#     min_time = 999999999.0
#     max_time = 0.0
#     sum_time = 0.0
#     i = 0
#     for i in range(n):
#         p.set_puzzle(ps.get_puzzle(i))
#         temp_start = time.perf_counter()
#         p.solve_puzzle()
#         temp_end = time.perf_counter()
#         puzzle_time = temp_end - temp_start
#         min_time = min(min_time, puzzle_time)
#         max_time = max(max_time, puzzle_time)
#         sum_time += puzzle_time
#         if p.is_puzzle_solved():
#             success += 1
#         else:
#             failed += 1
#             all_failed.append(i)
#         if (i+1) % mod == 0:
#             percent = float(failed) / float(i+1) * 100.0
#             print(f"Puzzle {i+1}")
#             print(f"    Solved {success} of {i+1} puzzles, {failed} unsolved -> {percent:.3f}%")
#             print(f"    Last puzzle time {(temp_end - temp_start)/float(i+1)*1000:.5f} msec")
#             print(f"    Min time: {min_time*1000:.4f} msec, Max Time {max_time*1000:.4f}")
#             print(f"    Time per puzzle {sum_time/float(i+1)*1000:.4f} msec")
#     end = time.perf_counter()
#     percent = float(failed) / float(i+1) * 100.0
#     print(f"Solved {success} of {i+1} puzzles, {failed} unsolved -> {percent:.3f}%")
#     print(f"Total time {end - start:.3f} sec")
#     print(f"Min time: {min_time * 1000:.4f} msec, Max Time {max_time * 1000:.4f}")
#     print(f"Time per puzzle {sum_time/float(n)*1000:0.6f} msec")
#     if failed > 0 and save_failures is True:
#         failed_filename = filename + "_Failed.txt"
#         failed_file = open(failed_filename, 'wt')
#         for i in all_failed:
#             failed_file.write(f"{ps.get_puzzle(i)}\n")
#         failed_file.close()
#         print(f"Wrote {failed_filename} of failed puzzles")

# def solve_text_puzzle(puzzle):
#     p = Puzzle(puzzle)
#     start = time.perf_counter()
#     p.solve_puzzle()
#     end = time.perf_counter()
#     solve_time = end - start
#     solved = p.is_puzzle_solved()
#     print(f"Puzzle, Solved = {solved}, Time = {solve_time:.4f} ms")
#     p.print_puzzle()

# def solve_text_puzzle_no_output(puzzle) -> bool:
#     p = Puzzle(puzzle)
#     p.solve_puzzle()
#     return p.solve_puzzle()

# import concurrent.futures

# def solve_all_threads(filename: str) -> None:
#     ps = Puzzles(filename)
#     p = Puzzle()
#     success = 0
#     failed = 0
#     start = time.perf_counter()
#     n = ps.get_number_of_puzzles()
#     i = 0
#     #with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
#     with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
#         future_sudoku = {executor.submit(solve_text_puzzle_no_output,ps.get_puzzle(i)) : i for i in range(ps.get_number_of_puzzles())}
#         for future in concurrent.futures.as_completed(future_sudoku):
#             result = future_sudoku[future]
#             try:
#                 result = future.result()
#             except Exception as exc:
#                 print('generated an exception:')
#             else:
#                 if result is True:
#                     success += 1
#                 else:
#                     failed += 1

#     percent = float(failed) / float(n) * 100.0
#     solve_time = time.perf_counter() - start
#     print(f"Solved {success} of {n} puzzles, {failed} unsolved -> {percent:.3f}% in {time.perf_counter()-start:.3f} sec, {solve_time/ps.get_number_of_puzzles()*1000:.4f} msec per puzzle")


def square_to_text(sq: int) -> str:
    c = int(sq % 9)
    r = int(sq / 9)
    return chr(ord("A") + r) + chr(ord("1") + c)

if __name__ == "__main__":
    grid1 = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
    grid3 = "8.2.5.7.1..7.8246..1.9.....6....18325.......91843....6.....4.2..9561.3..3.8.9.6.7"
    # not solved with ones / peers
    need_guess = ".61.2.....4.6.59..392...5.882...9..74....3......48...3..7..21...1..7....98..146.2"
    easy505 = "1..92....524.1...........7..5...81.2.........4.27...9..6...........3.945....71..6"
    grid2 = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
    hard1 = ".....6....59.....82....8....45........3........6..3.54...325..6.................."
    easy506 = ".43.8.25.6.............1.949....4.7....6.8....1.2....382.5.............5.34.9.71."
    blank = "................................................................................."
    # solved
    solved1 = "431829765276513984598467312389251647642378591157946238964785123723194856815632479"
    solved2 = "687942351591376284342158769465239178138567942279814635853791426924683517716425893"
    solved3 = "523846917961537428487219653154693782632478195798152346879324561316985274245761839"
    s = Sudoku()
    s.set_puzzle(grid1)
    print(s.get_puzzle_text())
    # # start = time.perf_counter()
    # # solve_all_threads(Puzzles.puzzle_100000)
    # # print(f"done {time.perf_counter() - start:.4} seconds")
    # ps = Puzzles(Puzzles.puzzle_1m)
    # p = Puzzle()
    # success = 0
    # failed = 0
    # start = time.perf_counter()
    # for i in range(ps.get_number_of_puzzles()):
    #     p.set_puzzle(ps.get_puzzle(i))
    #     if i%1000 == 0:
    #         print(i)
    #     if p.solve_puzzle() is True:
    #         success += 1
    #     else:
    #         failed += 1
    # percent = float(failed) / float(i + 1) * 100.0
    # solve_time = time.perf_counter() - start
    # print(
    #     f"Solved {success} of {i + 1} puzzles, {failed} unsolved -> {percent:.3f}% in {time.perf_counter() - start:.3f} sec, {solve_time / ps.get_number_of_puzzles() * 1000:.4f} msec per puzzle")
