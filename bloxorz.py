import os
from sys import argv
from bloxorz_logic import bloxorz_dfs, bloxorz_ga
import time
import psutil
'''

'''
_, input, solver = argv

start_time = time.time()
mem_before = psutil.Process(os.getpid()).memory_info().rss

if solver == 'DFS':
    test = bloxorz_dfs('input{}.txt'.format(input))
    test.DFS_solver()
elif solver == 'GA':
    test = bloxorz_ga('input{}.txt'.format(input))
    test.GA_solver()  

end_time = time.time()
mem_after = psutil.Process(os.getpid()).memory_info().rss

print("Time elapsed: ", end_time - start_time, "seconds")
print("Memory usage: ", (mem_after - mem_before) / (1024 * 1024), "MBs")