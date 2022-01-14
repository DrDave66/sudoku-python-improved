import sys
import io
import pstats
from pstats import SortKey


class Functions:
    ncalls = int()
    tottime = float()
    tottime_percall = float()
    cumtime = float()
    cumtime_percall = float()
    filename = str()
    line = int()
    function = str()
    splitstr = list()

    def __init__(self, string: str):
        splitstr = string.split()
        ncalls = int(splitstr[0])
        tottime = float(splitstr[1])
        tottime_percall = tottime / ncalls
        cumtime = float(splitstr[3])
        cumtime_percall = cumtime / ncalls
        filename = splitstr[5].split(":")[0]
        line = splitstr[5].split(":")[1].split("(")[0]
        function = splitstr[5].split(":")[1].split("(")[1].split(")")[0]

    def __repr__(self):
        print(f"ncalls        {self.ncalls}")
        print(f"tottime       {self.tottime}")
        print(f"tottime_percall   {self.tottime_percall}")
        print(f"cumtime           {self.cumtime}")
        print(f"cumtime_percall   {self.cumtime_percall}")
        print(f"filename          {self.filename}")




if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("You must include a stats file name on the command line")
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    ps = pstats.Stats(sys.argv[1])
    ps.strip_dirs().sort_stats(SortKey.TIME).print_stats()

    sys.stdout = old_stdout
    print("done with capture")
    print("captured:")
    s = new_stdout.getvalue()
    ss = s.splitlines()
    print(ss)
    for i in range(len(ss)):
        print(ss[i])
    funcs = Functions(ss[7])

