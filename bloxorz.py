from sys import argv
from bloxorz_logic import bloxorz_bfs, bloxorz_ga
import time
import psutil
'''

'''
_, input, solver = argv

start_time = time.time()
mem_before = psutil.Process(os.getpid()).memory_info().rss

if solver == 'DFS':
    test = bloxorz_bfs('input{}.txt'.format(input))
    test.BFS_solver()
elif solver == 'GA':
    test = bloxorz_ga('input{}.txt'.format(input))
    test.GA_solver()  

end_time = time.time()
mem_after = psutil.Process(os.getpid()).memory_info().rss

print("Time elapsed: ", start_time - end_time, "seconds")
print("Memory usage: ", mem_after - mem_before, "MB")