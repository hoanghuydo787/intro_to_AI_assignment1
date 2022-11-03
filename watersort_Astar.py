import os
from watersort_logic import watersort_Astar
import time 
import psutil

outdir = "io_watersort/output"

start_time = time.time()
mem_before = psutil.Process(os.getpid()).memory_info().rss

#Choose the input file
test = watersort_Astar("input1.txt")

mem_after = psutil.Process(os.getpid()).memory_info().rss

test.display_res()

end_time = time.time()

with open(os.path.join(outdir,test.outfile), "a") as f:
    f.write('\n--------\nTime of algorithm is {} seconds'.format(end_time-start_time))
    f.write('\nMemory usage is {:,} bytes'.format(mem_after - mem_before))
