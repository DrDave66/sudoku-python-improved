import time
import cProfile
import sys
from puzzles import Puzzles
from sudoku import Sudoku
from procStats import Stats



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

def solve_all_no_stats(filename: str) -> None:
    ps = Puzzles(filename)
    s = Sudoku()
    success = 0
    failed = 0
    n = ps.get_number_of_puzzles()
    i = 0
    solve_time = 0.0
    total_start = time.perf_counter()
    start = time.perf_counter()
    for i in range(n):
        s.set_puzzle(ps.get_puzzle(i))
        solve_start = time.perf_counter()
        s.solve_puzzle()
        solve_time += time.perf_counter() - solve_start
        if s.is_puzzle_solved():
            success += 1
        else:
            failed += 1
        if i % (n/50) == 0:
            print(i)
    percent = float(failed) / float(i+1) * 100.0
    print(f"Solved {success} of {i+1} puzzles, {failed} unsolved -> {percent:.3f}% in {time.perf_counter() - total_start:.3f} sec, {solve_time/ps.get_number_of_puzzles()*1000:.4f} msec per puzzle")


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


def quick_solve(s, p):
    solved = 0
    solve_time = 0
    total_start = time.perf_counter()
    for ii in range(p.get_number_of_puzzles()):
        s.set_puzzle(p.get_puzzle(ii))
        # s.print_puzzle_and_allowable_values()
        start = time.perf_counter()
        s.solve_ones()
        solve_time += time.perf_counter() - start
        if s.is_puzzle_solved():
            solved += 1

        if (ii + 1) % 10000 == 0:
            print(f"{ii + 1} - {solved}")
    total_time = time.perf_counter() - total_start
    print(
        f"Solved {solved} of {p.get_number_of_puzzles()} puzzles,  {total_time:.3f} sec total,"
        f" {solve_time / p.get_number_of_puzzles() * 1000:.4f} msec per puzzle")


if __name__ == "__main__":
    grid1 = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
    grid3 = "8.2.5.7.1..7.8246..1.9.....6....18325.......91843....6.....4.2..9561.3..3.8.9.6.7"
    need2 = ".687..9....4....71.3.8.9.5.3...8.1...4...5..7..73.4.926.2..1..5....2.6...59.3..28"
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
    profiling = False
    # if profiling:
    #     s = Sudoku()
    #     p = Puzzles(Puzzles.puzzle_10000)
    #     statsName = "test.stats"
    #     cProfile.run('quick_solve(s, p)', statsName)
    #     import pstats
    #     from pstats import SortKey
    #
    #     ps = pstats.Stats(statsName)
    #     ps.strip_dirs().sort_stats(SortKey.TIME).print_stats(20)
    # else:
    if len(sys.argv) >= 2:
        if len(sys.argv) == 3:
            statsName = sys.argv[2]
            cmd = "solve_all_no_stats('" + sys.argv[1] + "')"
            basename = sys.argv[1].split("/")[-1]
            print(f"Basename is {basename}")
            cProfile.run(cmd, statsName)
            import pstats
            from pstats import SortKey
            p = Stats(statsName)
            p.strip_dirs().sort_stats(SortKey.TIME).print_stats(20)
            p.strip_dirs().sort_stats(SortKey.TIME).dump_stats(statsName)
            print(f"Dumped stats to {statsName}")
        else:
            solve_all_no_stats(sys.argv[1])
    else:
        print("you must supply a puzzle file name. append stats filename to save stats")

        # ps = Puzzles("../sudoku-puzzles/Guesses.txt")
        # # ps = Puzzles(Puzzles.puzzle_10000)
        # s = Sudoku()
        # success = 0
        # failed = 0
        # solve_time = 0
        # guessed = 0
        # total_start = time.perf_counter()
        # for i in range(ps.get_number_of_puzzles()):
        #     s.set_puzzle(ps.get_puzzle(i))
        #     if i % 100 == 0:
        #         print(i)
        #     start = time.perf_counter()
        #     if s.solve_puzzle() is True:
        #         success += 1
        #     else:
        #         failed += 1
        #     solve_time += time.perf_counter() - start
        #     if s.number_of_guesses > 0:
        #         guessed += 1
        #     #     print(f"Guessed {i}")
        # percent = float(failed) / float(i + 1) * 100.0
        #
        # print(f"Solved {success} of {i + 1} puzzles, {failed} unsolved -> {percent:.3f}% in "
        #       f"{(time.perf_counter() - total_start):.3f} sec, "
        #       f"{solve_time / ps.get_number_of_puzzles() * 1000:.4f} msec per puzzle",
        #       f"{guessed} puzzles needed guesses")


# old sudoku
# Solved 1000000 of 1000000 puzzles, 0 unsolved -> 0.000% in 1069.381 sec, 1.0694 msec per puzzle
# Solved 204989 of 204989 puzzles, 0 unsolved -> 0.000% in 2330.239 sec, 11.3676 msec per puzzle
# "improved" sudoku
# Solved 1000000 of 1000000 puzzles, 0 unsolved -> 0.000% in 619.789 sec, 0.6198 msec per puzzle
#
# # start = time.perf_counter()
# # solve_all_threads(Puzzles.puzzle_100000)
# # print(f"done {time.perf_counter() - start:.4} seconds")

#   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#  8100000   45.112    0.000   45.112    0.000 sudoku.py:53(set_value)
# 49312233   18.161    0.000   18.161    0.000 sudoku.py:103(number_of_bits_set)
#   608793   17.674    0.000   35.835    0.000 sudoku.py:224(<listcomp>)
#   200027    9.119    0.000    9.119    0.000 sudoku.py:247(is_puzzle_solved)
#   100000    4.134    0.000   25.471    0.000 sudoku.py:36(set_puzzle)
#   100000    3.586    0.000   70.332    0.001 sudoku.py:218(solve_ones)
#   100000    2.162    0.000    2.162    0.000 sudoku.py:48(clear_puzzle)
#        1    0.378    0.378  100.716  100.716 main.py:186(quick_solve)
#   808796    0.222    0.000    0.222    0.000 {built-in method builtins.len}
#   100000    0.076    0.000    0.136    0.000 puzzles.py:37(get_puzzle)
#   200002    0.049    0.000    0.049    0.000 {built-in method time.perf_counter}
#   100003    0.044    0.000    0.060    0.000 puzzles.py:34(get_number_of_puzzles)
#       11    0.000    0.000    0.000    0.000 {built-in method builtins.print}
#        1    0.000    0.000  100.716  100.716 {built-in method builtins.exec}
#        1    0.000    0.000  100.716  100.716 <string>:1(<module>)
#        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

# bit hack to count bits
#   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#  8100000   41.724    0.000   41.724    0.000 sudoku.py:53(set_value)
#   608793   19.712    0.000   37.271    0.000 sudoku.py:228(<listcomp>)
# 49312233   17.558    0.000   17.558    0.000 sudoku.py:103(number_of_bits_set)
#   200027    9.139    0.000    9.139    0.000 sudoku.py:251(is_puzzle_solved)
#   100000    4.039    0.000   23.649    0.000 sudoku.py:36(set_puzzle)
#   100000    3.440    0.000   69.537    0.001 sudoku.py:222(solve_ones)
#   100000    2.043    0.000    2.043    0.000 sudoku.py:48(clear_puzzle)
#        1    0.365    0.365   98.367   98.367 main.py:186(quick_solve)
#   808796    0.176    0.000    0.176    0.000 {built-in method builtins.len}
#   100000    0.076    0.000    0.180    0.000 puzzles.py:37(get_puzzle)
#   200002    0.052    0.000    0.052    0.000 {built-in method time.perf_counter}
#   100003    0.043    0.000    0.104    0.000 puzzles.py:34(get_number_of_puzzles)
#       11    0.000    0.000    0.000    0.000 {built-in method builtins.print}
#        1    0.000    0.000   98.367   98.367 {built-in method builtins.exec}
#        1    0.000    0.000   98.367   98.367 <string>:1(<module>)
#        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

#10k removed big loop comprehension
# Solved 10000 of 10000 puzzles,  7.509 sec total, 0.4997 msec per puzzle
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#    810000    3.756    0.000    3.756    0.000 sudoku.py:53(set_value)
#     10000    1.252    0.000    4.987    0.000 sudoku.py:222(solve_ones)
#   3476034    1.156    0.000    1.156    0.000 sudoku.py:103(number_of_bits_set)
#     20003    0.790    0.000    0.790    0.000 sudoku.py:251(is_puzzle_solved)
#     10000    0.343    0.000    2.085    0.000 sudoku.py:36(set_puzzle)
#     10000    0.165    0.000    0.165    0.000 sudoku.py:48(clear_puzzle)
#         1    0.028    0.028    7.509    7.509 main.py:186(quick_solve)
#     10000    0.007    0.000    0.013    0.000 puzzles.py:37(get_puzzle)
#     20002    0.005    0.000    0.005    0.000 {built-in method time.perf_counter}
#     10003    0.004    0.000    0.006    0.000 puzzles.py:34(get_number_of_puzzles)
#     20003    0.003    0.000    0.003    0.000 {built-in method builtins.len}
#         1    0.000    0.000    7.509    7.509 {built-in method builtins.exec}
#         2    0.000    0.000    0.000    0.000 {built-in method builtins.print}
#         1    0.000    0.000    7.509    7.509 <string>:1(<module>)
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
