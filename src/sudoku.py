import time
import cProfile
import re
from puzzles import Puzzles
from puzzle import Puzzle


def solve_one_puzzle(filename, num=None) -> None:
    """
    solves one puzzle from a file. if no puzzle number is specified, a random one is chosen
    :param filename: puzzle filename to be opened
    :param [optional num: puzzle number
    :return: None
    """
    ps = Puzzles(filename)
    p = Puzzle()
    if num is None:
        import random
        random.seed()
        num = random.randrange(ps.get_number_of_puzzles())
    p.set_puzzle(ps.get_puzzle(num))
    p.print_puzzle()
    start = time.perf_counter()
    p.solve_puzzle()
    end = time.perf_counter()
    p.print_puzzle()
    solve_time = end - start
    solved = p.is_puzzle_solved()
    print(f"Puzzle {num}, Solved = {solved}, Time = {solve_time:.4f} ms")

def solve_puzzle_range(filename, puzzle_range=None):
    ps = Puzzles(filename)
    p = Puzzle()
    if puzzle_range is None:
        puzzle_range = range(ps.get_number_of_puzzles())
    start = time.perf_counter()
    solved = 0
    unsolved = 0
    end = 0.0
    for r in puzzle_range:
        p.set_puzzle(ps.get_puzzle(r))
        p.solve_puzzle()
        end = time.perf_counter()
        if p.is_puzzle_solved():
            solved += 1
        else:
            unsolved += 1
    solve_time = end - start
    average_time = float(solve_time) / float(len(puzzle_range))
    print(f"Solved = {solved}, Unsolved = {unsolved}, Time = {solve_time:.4f} ms, Average time {average_time:.4f} msec")

def solve_all_no_stats(filename: str) -> None:
    ps = Puzzles(filename)
    p = Puzzle()
    success = 0
    failed = 0
    start = time.perf_counter()
    n = ps.get_number_of_puzzles()
    i = 0
    for i in range(n):
        p.set_puzzle(ps.get_puzzle(i))
        p.solve_puzzle()

        if p.is_puzzle_solved():
            success += 1
        else:
            failed += 1
    percent = float(failed) / float(i+1) * 100.0
    solve_time = time.perf_counter() - start
    print(f"Solved {success} of {i+1} puzzles, {failed} unsolved -> {percent:.3f}% in {time.perf_counter()-start:.3f} sec, {solve_time/ps.get_number_of_puzzles()*1000:.4f} msec per puzzle")


def solve_all_with_stats(filename: str, save_failures:bool =False, usemod:int =0) -> None:
    """

    :param filename:
    :param save_failures:
    :param usemod:
    :return:
    """

    ps = Puzzles(filename)
    p = Puzzle()
    success = 0
    failed = 0
    n = ps.get_number_of_puzzles()
    if usemod == 0:
        mod = int(n/20)
    else:
        mod = usemod
    if mod == 0:
        mod = 1
    start = time.perf_counter()
    all_failed = list()
    min_time = 999999999.0
    max_time = 0.0
    sum_time = 0.0
    i = 0
    for i in range(n):
        p.set_puzzle(ps.get_puzzle(i))
        temp_start = time.perf_counter()
        p.solve_puzzle()
        temp_end = time.perf_counter()
        puzzle_time = temp_end - temp_start
        min_time = min(min_time, puzzle_time)
        max_time = max(max_time, puzzle_time)
        sum_time += puzzle_time
        if p.is_puzzle_solved():
            success += 1
        else:
            failed += 1
            all_failed.append(i)
        if (i+1) % mod == 0:
            percent = float(failed) / float(i+1) * 100.0
            print(f"Puzzle {i+1}")
            print(f"    Solved {success} of {i+1} puzzles, {failed} unsolved -> {percent:.3f}%")
            print(f"    Last puzzle time {(temp_end - temp_start)/float(i+1)*1000:.5f} msec")
            print(f"    Min time: {min_time*1000:.4f} msec, Max Time {max_time*1000:.4f}")
            print(f"    Time per puzzle {sum_time/float(i+1)*1000:.4f} msec")
    end = time.perf_counter()
    percent = float(failed) / float(i+1) * 100.0
    print(f"Solved {success} of {i+1} puzzles, {failed} unsolved -> {percent:.3f}%")
    print(f"Total time {end - start:.3f} sec")
    print(f"Min time: {min_time * 1000:.4f} msec, Max Time {max_time * 1000:.4f}")
    print(f"Time per puzzle {sum_time/float(n)*1000:0.6f} msec")
    if failed > 0 and save_failures is True:
        failed_filename = filename + "_Failed.txt"
        failed_file = open(failed_filename, 'wt')
        for i in all_failed:
            failed_file.write(f"{ps.get_puzzle(i)}\n")
        failed_file.close()
        print(f"Wrote {failed_filename} of failed puzzles")

def solve_text_puzzle(puzzle):
    p = Puzzle(puzzle)
    start = time.perf_counter()
    p.solve_puzzle()
    end = time.perf_counter()
    solve_time = end - start
    solved = p.is_puzzle_solved()
    print(f"Puzzle, Solved = {solved}, Time = {solve_time:.4f} ms")
    p.print_puzzle()

def solve_text_puzzle_no_output(puzzle) -> bool:
    p = Puzzle(puzzle)
    p.solve_puzzle()
    return p.solve_puzzle()

import concurrent.futures

def solve_all_threads(filename: str) -> None:
    ps = Puzzles(filename)
    p = Puzzle()
    success = 0
    failed = 0
    start = time.perf_counter()
    n = ps.get_number_of_puzzles()
    i = 0
    #with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        future_sudoku = {executor.submit(solve_text_puzzle_no_output,ps.get_puzzle(i)) : i for i in range(ps.get_number_of_puzzles())}
        for future in concurrent.futures.as_completed(future_sudoku):
            result = future_sudoku[future]
            try:
                result = future.result()
            except Exception as exc:
                print('generated an exception:')
            else:
                if result is True:
                    success += 1
                else:
                    failed += 1

    percent = float(failed) / float(n) * 100.0
    solve_time = time.perf_counter() - start
    print(f"Solved {success} of {n} puzzles, {failed} unsolved -> {percent:.3f}% in {time.perf_counter()-start:.3f} sec, {solve_time/ps.get_number_of_puzzles()*1000:.4f} msec per puzzle")

if __name__ == "__main__":
    # start = time.perf_counter()
    # solve_all_threads(Puzzles.puzzle_100000)
    # print(f"done {time.perf_counter() - start:.4} seconds")
    ps = Puzzles(Puzzles.puzzle_10000)
    p = Puzzle()
    success = 0
    failed = 0
    start = time.perf_counter()
    for i in range(ps.get_number_of_puzzles()):
        p.set_puzzle(ps.get_puzzle(i))
        if p.solve_puzzle() is True:
            success += 1
        else:
            failed += 1
    percent = float(failed) / float(i + 1) * 100.0
    solve_time = time.perf_counter() - start
    print(
        f"Solved {success} of {i + 1} puzzles, {failed} unsolved -> {percent:.3f}% in {time.perf_counter() - start:.3f} sec, {solve_time / ps.get_number_of_puzzles() * 1000:.4f} msec per puzzle")

    # solve_all_no_stats(Puzzles.1000)
    # save_stats = False
    # statsName = 'back to jetbrains python 310.stats'

    # if save_stats is True:
    #     cProfile.run('solve_all_no_stats(Puzzles.puzzle_10000)',statsName)
    #     import pstats
    #     from pstats import SortKey
    #     p = pstats.Stats(statsName)
    #     p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(15)
    # else:
    #     import pstats
    #     from pstats import SortKey
    #     p = pstats.Stats(statsName)
    #     p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(15)

# pycharm python 3.10
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000   26.555   26.555 {built-in method builtins.exec}
#         1    0.000    0.000   26.555   26.555 <string>:1(<module>)
#         1    0.033    0.033   26.555   26.555 sudoku.py:52(solve_all_no_stats)
#     10000    0.019    0.000   18.822    0.002 puzzle.py:294(solve_puzzle)
#     10000    4.270    0.000   17.721    0.002 puzzle.py:212(solve_ones)
#    810000   10.249    0.000   13.014    0.000 puzzle.py:202(set_value)
#     10000    0.700    0.000    6.579    0.001 puzzle.py:58(set_puzzle)
#    643437    1.423    0.000    3.053    0.000 {method 'join' of 'str' objects}
#   9040356    2.490    0.000    2.490    0.000 {method 'count' of 'str' objects}
#  16200000    2.476    0.000    2.476    0.000 {method 'replace' of 'str' objects}
#     20000    0.860    0.000    2.126    0.000 puzzle.py:234(is_puzzle_solved)
#   6434370    1.630    0.000    1.630    0.000 puzzle.py:226(<genexpr>)
#   4880000    1.266    0.000    1.266    0.000 puzzle.py:239(<genexpr>)
#     23831    0.573    0.000    0.767    0.000 puzzle.py:216(<listcomp>)
#    820000    0.292    0.000    0.292    0.000 {method 'find' of 'str' objects}
# # improved is_puzzle_solved474
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000   28.635   28.635 {built-in method builtins.exec}
#         1    0.000    0.000   28.635   28.635 <string>:1(<module>)
#         1    0.035    0.035   28.634   28.634 sudoku.py:52(solve_all_no_stats)
#     10000    0.021    0.000   20.245    0.002 puzzle.py:291(solve_puzzle)
#     10000    4.712    0.000   19.043    0.002 puzzle.py:210(solve_ones)
#    810000   10.577    0.000   13.687    0.000 puzzle.py:200(set_value)
#     10000    0.754    0.000    6.915    0.001 puzzle.py:58(set_puzzle)
#    643437    1.657    0.000    3.468    0.000 {method 'join' of 'str' objects}
#  16200000    2.785    0.000    2.785    0.000 {method 'replace' of 'str' objects}
#   9040356    2.505    0.000    2.505    0.000 {method 'count' of 'str' objects}
#     20000    1.056    0.000    2.419    0.000 puzzle.py:232(is_puzzle_solved)
#   6434370    1.811    0.000    1.811    0.000 puzzle.py:224(<genexpr>)
#   4880000    1.363    0.000    1.363    0.000 puzzle.py:237(<genexpr>)
#     23831    0.605    0.000    0.827    0.000 puzzle.py:214(<listcomp>)
#    820000    0.343    0.000    0.343    0.000 {method 'find' of 'str' objects}

# baseline
 #   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
 #        1    0.000    0.000   28.472   28.472 {built-in method builtins.exec}
 #        1    0.000    0.000   28.471   28.471 <string>:1(<module>)
 #        1    0.039    0.039   28.471   28.471 sudoku.py:52(solve_all_no_stats)
 #    10000    0.022    0.000   19.849    0.002 puzzle.py:291(solve_puzzle)
 #    10000    4.157    0.000   18.121    0.002 puzzle.py:210(solve_ones)
 #   810000   10.251    0.000   13.444    0.000 puzzle.py:200(set_value)
 #    10000    0.655    0.000    6.681    0.001 puzzle.py:58(set_puzzle)
 #    20000    0.021    0.000    3.358    0.000 puzzle.py:232(is_puzzle_solved)
 #    20000    0.096    0.000    3.337    0.000 {built-in method builtins.all}
 #   560000    1.878    0.000    3.241    0.000 puzzle.py:242(<genexpr>)
 #   643437    1.470    0.000    3.193    0.000 {method 'join' of 'str' objects}
 # 16200000    2.830    0.000    2.830    0.000 {method 'replace' of 'str' objects}
 #  9040356    2.587    0.000    2.587    0.000 {method 'count' of 'str' objects}
 #  6434370    1.723    0.000    1.723    0.000 puzzle.py:224(<genexpr>)
 #    23831    0.549    0.000    0.759    0.000 puzzle.py:214(<listcomp>)


# Solved 100000 of 100000 puzzles, 0 unsolved -> 0.000%
# Total time 146.760 sec
# Min time: 0.7340 msec, Max Time 55.7176
# Time per puzzle 0.990170 msec
