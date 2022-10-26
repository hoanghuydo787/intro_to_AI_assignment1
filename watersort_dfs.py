import os
from watersort import *

outdir = "io_watersort/output"

def dfs(start):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if goal_state(vertex):
            return path

        for next_element in next_state(vertex):
            stack.append((next_element, path + [next_element]))

if __name__ == "__main__":
    state = []
    filename = "input1.txt"
    read_input(filename, state)
    res = dfs(state)
    with open(os.path.join(outdir,filename.replace("input", "output")), "w") as f:
        for i in range(len(res)):
            f.write("Step " + str(i) + "\n")
            f.write(display_state(res[i]))
