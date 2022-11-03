import os
from watersort_logic import watersort_Astar, watersort_dfs
import time
import sys
import psutil

outdir = "io_watersort/output"
filename = sys.argv[1]
algorithm = sys.argv[2]

start_time = time.time()
mem_before = psutil.Process(os.getpid()).memory_info().rss

if algorithm == "dfs":
    test = watersort_dfs(filename)
else:
    test = watersort_Astar(filename)

mem_after = psutil.Process(os.getpid()).memory_info().rss
end_time = time.time()

test.display_res()

with open(os.path.join(outdir,test.outfile), "a") as f:
    f.write('\n--------\nTime of algorithm is {} seconds'.format(end_time-start_time))
    f.write('\nMemory usage is {:,} bytes'.format(mem_after - mem_before))
