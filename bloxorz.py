from sys import argv
from bloxorz_logic import bloxorz_bfs, bloxorz_ga
'''

'''
_, input, solver = argv

if solver == 'DFS':
    test = bloxorz_bfs('input{}.txt'.format(input))
    test.BFS_solver()
elif solver == 'GA':
    test = bloxorz_ga('input{}.txt'.format(input))
    test.GA_solver()  

