import sys
import os
from dataclasses import dataclass
from functools import cmp_to_key
from enum import Enum
from typing import Dict
import pstats


class SortKey(str, Enum):
    CALLS = 'calls', 'ncalls'
    CUMULATIVE = 'cumulative', 'cumtime'
    FILENAME = 'filename', 'module'
    LINE = 'line'
    NAME = 'name'
    NFL = 'nfl'
    PCALLS = 'pcalls'
    STDNAME = 'stdname'
    TIME = 'time', 'tottime'

    def __new__(cls, *values):
        value = values[0]
        obj = str.__new__(cls, value)
        obj._value_ = value
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        return obj

@dataclass(unsafe_hash=True)
class FunctionProfile:
    ncalls: int
    tottime: float
    tottime_percent: float
    percall_tottime: float
    cumtime: float
    cumtime_percent: float
    percall_cumtime: float
    file_name: str
    line_number: int
    callers: []

@dataclass(unsafe_hash=True)
class StatsProfile:
    '''Class for keeping track of an item in inventory.'''
    total_tt: float
    total_calls: int
    func_profiles: Dict[str, FunctionProfile]

class MyStats:
    def __init__(self, *args, stream=None):
        super().__init__(*args, stream=stream)
        self.stream = stream or sys.stdout
        if not len(args):
            arg = None
        else:
            arg = args[0]
            args = args[1:]
        self.all_callees = None  # calc only if needed
        self.files = []
        self.fcn_list = None
        self.total_tt = 0
        self.total_calls = 0
        self.prim_calls = 0
        self.max_name_len = 0
        self.top_level = set()
        self.stats = {}
        self.sort_arg_dict = {}
        self.load_stats(arg)
        try:
            self.get_top_level_stats()
        except Exception:
            print("Invalid timing data %s" %
                  (self.files[-1] if self.files else ''), file=self.stream)
            raise
        self.add(*args)

    def get_stats_profile(self):
        """This method returns an instance of StatsProfile, which contains a mapping
        of function names to instances of FunctionProfile. Each FunctionProfile
        instance holds information related to the function's profile such as how
        long the function took to run, how many times it was called, etc...
        """
        func_list = self.fcn_list[:] if self.fcn_list else list(self.stats.keys())
        if not func_list:
            return StatsProfile(0, 0, {})

        total_tt = self.total_tt
        func_profiles = {}
        stats_profile = StatsProfile(total_tt, self.total_calls, func_profiles)

        for func in func_list:
            cc, nc, tt, ct, callers = self.stats[func]
            file_name, line_number, func_name = func
            ncalls = str(nc) if nc == cc else (str(nc) + '/' + str(cc))
            tottime = tt
            percall_tottime = -1 if nc == 0 else float(tt / nc)
            cumtime = float(ct)
            percall_cumtime = -1 if cc == 0 else float(ct / cc)
            func_profile = FunctionProfile(
                int(ncalls),
                tottime,  # time spent in this function alone
                tottime / total_tt, # % total time
                percall_tottime,
                cumtime,  # time spent in the function plus all functions that this function called,
                cumtime / total_tt, # % cumtime
                percall_cumtime,
                file_name,
                line_number,
                callers # list of callers
            )
            func_profiles[func_name] = func_profile

        return stats_profile

    def get_print_list(self, sel_list):
        width = self.max_name_len
        if self.fcn_list:
            stat_list = self.fcn_list[:]
            msg = "   Ordered by: " + self.sort_type + '\n'
        else:
            stat_list = list(self.stats.keys())
            msg = "   Random listing order was used\n"

        for selection in sel_list:
            stat_list, msg = self.eval_print_amount(selection, stat_list, msg)

        count = len(stat_list)

        if not stat_list:
            return 0, stat_list
        print(msg, file=self.stream)
        if count < len(self.stats):
            width = 0
            for func in stat_list:
                if  len(func_std_string(func)) > width:
                    width = len(func_std_string(func))
        return width+2, stat_list

    def print_stats(self, *amount):
        for filename in self.files:
            print(filename, file=self.stream)
        if self.files:
            print(file=self.stream)
        indent = ' ' * 8
        for func in self.top_level:
            print(indent, func_get_function_name(func), file=self.stream)

        print(indent, self.total_calls, "function calls", end=' ', file=self.stream)
        if self.total_calls != self.prim_calls:
            print("(%d primitive calls)" % self.prim_calls, end=' ', file=self.stream)
        print("in %.3f seconds" % self.total_tt, file=self.stream)
        print(file=self.stream)
        width, list = self.get_print_list(amount)
        if list:
            self.print_title()
            for func in list:
                self.print_line(func)
            print(file=self.stream)
            print(file=self.stream)
        return self

    def print_callees(self, *amount):
        width, list = self.get_print_list(amount)
        if list:
            self.calc_callees()

            self.print_call_heading(width, "called...")
            for func in list:
                if func in self.all_callees:
                    self.print_call_line(width, func, self.all_callees[func])
                else:
                    self.print_call_line(width, func, {})
            print(file=self.stream)
            print(file=self.stream)
        return self

    def print_callers(self, *amount):
        width, list = self.get_print_list(amount)
        if list:
            self.print_call_heading(width, "was called by...")
            for func in list:
                cc, nc, tt, ct, callers = self.stats[func]
                self.print_call_line(width, func, callers, "<-")
            print(file=self.stream)
            print(file=self.stream)
        return self

    def print_call_heading(self, name_size, column_title):
        print("Function ".ljust(name_size) + column_title, file=self.stream)
        # print sub-header only if we have new-style callers
        subheader = False
        for cc, nc, tt, ct, callers in self.stats.values():
            if callers:
                value = next(iter(callers.values()))
                subheader = isinstance(value, tuple)
                break
        if subheader:
            print(" "*name_size + "    ncalls  tottime  %tottime cumtime  %cumtime", file=self.stream)

    def print_call_line(self, name_size, source, call_dict, arrow="->"):
        print(func_std_string(source).ljust(name_size) + arrow, end=' ', file=self.stream)
        if not call_dict:
            print(file=self.stream)
            return
        clist = sorted(call_dict.keys())
        indent = ""
        for func in clist:
            name = func_std_string(func)
            value = call_dict[func]
            if isinstance(value, tuple):
                nc, cc, tt, ct = value
                if nc != cc:
                    substats = '%d/%d' % (nc, cc)
                else:
                    substats = '%d' % (nc,)
                substats = '%s %s %s %s %s  %s' % (substats.rjust(7+2*len(indent)),
                                                   f8(tt), f8(tt/self.total_tt*100.0),
                                                   f8(ct), f8(ct/self.total_tt*100.0), name)
                left_width = name_size + 1
            else:
                substats = '%s(%r) %s' % (name, value, f8(self.stats[func][3]))
                left_width = name_size + 3
            print(indent*left_width + substats, file=self.stream)
            indent = " "

    def print_title(self):
        print('   ncalls  tottime  %tottime percall  cumtime  %cumtime percall', end=' ', file=self.stream)
        print('filename:lineno(function)', file=self.stream)

    def print_line(self, func):  # hack: should print percentages
        cc, nc, tt, ct, callers = self.stats[func]
        c = str(nc)
        if nc != cc:
            c = c + '/' + str(cc)
        print(c.rjust(9), end=' ', file=self.stream)
        print(f8(tt), end=' ', file=self.stream)
        print(f8(tt / self.total_tt * 100.0), end=' ', file=self.stream)
        if nc == 0:
            print(' '*8, end=' ', file=self.stream)
        else:
            print(f8(tt/nc), end=' ', file=self.stream)
        print(f8(ct), end=' ', file=self.stream)
        print(f8(ct / self.total_tt * 100.0), end=' ', file=self.stream)
        if cc == 0:
            print(' '*8, end=' ', file=self.stream)
        else:
            print(f8(ct/cc), end=' ', file=self.stream)
        print(func_std_string(func), file=self.stream)


class TupleComp:
    """This class provides a generic function for comparing any two tuples.
    Each instance records a list of tuple-indices (from most significant
    to least significant), and sort direction (ascending or decending) for
    each tuple-index.  The compare functions can then be used as the function
    argument to the system sort() function when a list of tuples need to be
    sorted in the instances order."""

    def __init__(self, comp_select_list):
        self.comp_select_list = comp_select_list

    def compare (self, left, right):
        for index, direction in self.comp_select_list:
            l = left[index]
            r = right[index]
            if l < r:
                return -direction
            if l > r:
                return direction
        return 0

# **************************************************************************
# func_name is a triple (file:string, line:int, name:string)
def func_strip_path(func_name):
    filename, line, name = func_name
    return os.path.basename(filename), line, name

def func_get_function_name(func):
    return func[2]

def func_std_string(func_name):  # match what old profile produced
    if func_name[:2] == ('~', 0):
        # special case for built-in functions
        name = func_name[2]
        if name.startswith('<') and name.endswith('>'):
            return '{%s}' % name[1:-1]
        else:
            return name
    else:
        return "%s:%d(%s)" % func_name

def add_func_stats(target, source):
    """Add together all the stats for two profile entries."""
    cc, nc, tt, ct, callers = source
    t_cc, t_nc, t_tt, t_ct, t_callers = target
    return (cc+t_cc, nc+t_nc, tt+t_tt, ct+t_ct,
              add_callers(t_callers, callers))

def add_callers(target, source):
    """Combine two caller lists in a single list."""
    new_callers = {}
    for func, caller in target.items():
        new_callers[func] = caller
    for func, caller in source.items():
        if func in new_callers:
            if isinstance(caller, tuple):
                # format used by cProfile
                new_callers[func] = tuple(i + j for i, j in zip(caller, new_callers[func]))
            else:
                # format used by profile
                new_callers[func] += caller
        else:
            new_callers[func] = caller
    return new_callers

def count_calls(callers):
    """Sum the caller statistics to get total number of calls received."""
    nc = 0
    for calls in callers.values():
        nc += calls
    return nc

def f8(x):
    return f"{x:8.3f}" # "%8.3f" % x

if __name__ == '__main__':
    import cmd

    class MyProfileBrowser(cmd.Cmd):
        def __init__(self, profile=None):
            cmd.Cmd.__init__(self)
            self.prompt = " % "
            self.stats = None
            self.stream = sys.stdout
            if profile is not None:
                self.do_read(profile)

        def generic(self, fn, line):
            args = line.split()
            processed = []
            for term in args:
                try:
                    processed.append(int(term))
                    continue
                except ValueError:
                    pass
                try:
                    frac = float(term)
                    if frac > 1 or frac < 0:
                        print("Fraction argument must be in [0, 1]", file=self.stream)
                        continue
                    processed.append(frac)
                    continue
                except ValueError:
                    pass
                processed.append(term)
            if self.stats:
                getattr(self.stats, fn)(*processed)
            else:
                print("No statistics object is loaded.", file=self.stream)
            return 0

        def generic_help(self):
            print("Arguments may be:", file=self.stream)
            print("* An integer maximum number of entries to print.", file=self.stream)
            print("* A decimal fractional number between 0 and 1, controlling", file=self.stream)
            print("  what fraction of selected entries to print.", file=self.stream)
            print("* A regular expression; only entries with function names", file=self.stream)
            print("  that match it are printed.", file=self.stream)

        def do_add(self, line):
            if self.stats:
                try:
                    self.stats.add(line)
                except OSError as e:
                    print("Failed to load statistics for %s: %s" % (line, e), file=self.stream)
            else:
                print("No statistics object is loaded.", file=self.stream)
            return 0

        def help_add(self):
            print("Add profile info from given file to current statistics object.", file=self.stream)

        def do_callees(self, line):
            return self.generic('print_callees', line)

        def help_callees(self):
            print("Print callees statistics from the current stat object.", file=self.stream)
            self.generic_help()

        def do_callers(self, line):
            return self.generic('print_callers', line)

        def help_callers(self):
            print("Print callers statistics from the current stat object.", file=self.stream)
            self.generic_help()

        def do_EOF(self, line):
            print("", file=self.stream)
            return 1

        def help_EOF(self):
            print("Leave the profile browser.", file=self.stream)

        def do_quit(self, line):
            return 1

        def help_quit(self):
            print("Leave the profile browser.", file=self.stream)

        def do_read(self, line):
            if line:
                try:
                    self.stats = MyStats(line)
                except OSError as err:
                    print(err.args[1], file=self.stream)
                    return
                except Exception as err:
                    print(err.__class__.__name__ + ':', err, file=self.stream)
                    return
                self.prompt = line + "% "
            elif len(self.prompt) > 2:
                line = self.prompt[:-2]
                self.do_read(line)
            else:
                print("No statistics object is current -- cannot reload.", file=self.stream)
            return 0

        def help_read(self):
            print("Read in profile data from a specified file.", file=self.stream)
            print("Without argument, reload the current file.", file=self.stream)

        def do_reverse(self, line):
            if self.stats:
                self.stats.reverse_order()
            else:
                print("No statistics object is loaded.", file=self.stream)
            return 0

        def help_reverse(self):
            print("Reverse the sort order of the profiling report.", file=self.stream)

        def do_sort(self, line):
            if not self.stats:
                print("No statistics object is loaded.", file=self.stream)
                return
            abbrevs = self.stats.get_sort_arg_defs()
            if line and all((x in abbrevs) for x in line.split()):
                self.stats.sort_stats(*line.split())
            else:
                print("Valid sort keys (unique prefixes are accepted):", file=self.stream)
                for (key, value) in MyStats.sort_arg_dict_default.items():
                    print("%s -- %s" % (key, value[1]), file=self.stream)
            return 0

        def help_sort(self):
            print("Sort profile data according to specified keys.", file=self.stream)
            print("(Typing `sort' without arguments lists valid keys.)", file=self.stream)

        def complete_sort(self, text, *args):
            return [a for a in MyStats.sort_arg_dict_default if a.startswith(text)]

        def do_stats(self, line):
            return self.generic('print_stats', line)

        def help_stats(self):
            print("Print statistics from the current stat object.", file=self.stream)
            self.generic_help()

        def do_strip(self, line):
            if self.stats:
                self.stats.strip_dirs()
            else:
                print("No statistics object is loaded.", file=self.stream)

        def help_strip(self):
            print("Strip leading path information from filenames in the report.", file=self.stream)

        def help_help(self):
            print("Show help for a given command.", file=self.stream)

        def postcmd(self, stop, line):
            if stop:
                return stop
            return None

    if len(sys.argv) > 1:
        initprofile = sys.argv[1]
    else:
        initprofile = None
    try:
        browser = MyProfileBrowser(initprofile)
        for profile in sys.argv[2:]:
            browser.do_add(profile)
        print("Welcome to the profile statistics browser.", file=browser.stream)
        browser.cmdloop()
        print("Goodbye.", file=browser.stream)
    except KeyboardInterrupt:
        pass

# That's all, folks.
