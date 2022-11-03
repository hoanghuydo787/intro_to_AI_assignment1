import os
import copy
from queue import PriorityQueue
from itertools import count

MAX_ELEMENTS = 4

indir = "io_watersort/input"
outdir = "io_watersort/output"

class State:
    def __init__(self, state= None):
        if state == None:
            self.mat = []
        else:
            self.mat = copy.deepcopy(state.mat)
    def addTube(self, Tube):
        self.mat.append(Tube)
    def getTypeOfTube(self, index_Tube) -> int:
        n = len(self.mat[index_Tube])
        if n == 0:
            return -1 #empty tube
        for i in range(n - 1):
            if self.mat[index_Tube][i] != self.mat[index_Tube][i+1]:
                return 2 #tube has more than one color
        if n == MAX_ELEMENTS:
            return 1 #tube has one color and full (goal tube)
        return 0 #tube has one color and is not full
    def getSizeOfTube(self, index_Tube):
        return len(self.mat[index_Tube])
    def getTopSizeOfTube(self, index_Tube)-> int:
        count = 1
        for i in range(len(self.mat[index_Tube]) - 2, -1, -1):
            if self.mat[index_Tube][i] == self.mat[index_Tube][i+1]:
                count += 1
            else:
                break
        return count
    def move(self, index_tube1, index_tube2, amount): #pour amount water from tube1 to tube2
        for i in range(amount):
            temp = self.mat[index_tube1].pop()
            self.mat[index_tube2].append(temp)
    def next_state(self, numTubes):
        result = []
        tube_type = [self.getTypeOfTube(i) for i in range(numTubes)]
        for i in range(numTubes-1):
            if (tube_type[i] == 1):
                continue
            for j in range(i + 1,numTubes,1):
                if (tube_type[j] == 1):
                    continue
                if (tube_type[i] + tube_type[j] == 2) or (tube_type[i] + tube_type[j] == 0): # 0 + 0, 2 + 0, 0 + 2: has tube type 0
                    if self.mat[j][-1] != self.mat[i][-1]: # tops of 2 tubes have different colors
                        continue
                    temp = State(self)
                    if tube_type[j] == 0: # 0 + 0, 2 + 0
                        temp.move(i, j, self.getTopSizeOfTube(i))
                        if tube_type[i] == 2 and (self.getSizeOfTube(i) + self.getSizeOfTube(j) <= 4):
                            temp2 = State(self)
                            temp2.move(j, i, temp2.getTopSizeOfTube(j))
                            result.insert(0, temp2)
                    else: # 0 + 2
                        temp.move(j, i, temp.getTopSizeOfTube(j))
                        if self.getSizeOfTube(i) + self.getSizeOfTube(j) <= 4:
                            temp2 = State(self)
                            temp2.move(i, j, temp2.getTopSizeOfTube(i))
                            result.insert(0, temp2)
                    result.append(temp)
                elif (tube_type[i] + tube_type[j] == 1): # 2 + (-1), (-1) + 2: empty tube and tube that has >=2 colors
                    temp = State(self)
                    if tube_type[j] == -1: # 2 + (-1)
                        temp.move(i, j, temp.getTopSizeOfTube(i))
                    else: # (-1) + 2
                        temp.move(j, i, temp.getTopSizeOfTube(j))
                    result.insert(0, temp)
                elif (tube_type[i] + tube_type[j] == 4): # 2 + 2: both 2 tubes which have >=2 colors
                    if self.mat[j][-1] != self.mat[i][-1]: # tops of 2 tubes have different colors
                        continue
                    amount_top_i = self.getTopSizeOfTube(i)
                    amount_top_j = self.getTopSizeOfTube(j)
                    if (self.getSizeOfTube(i) + amount_top_j <= 4): #pour $amount_top_j water from j to i
                        temp = State(self)
                        temp.move(j, i, amount_top_j)
                        result.insert(0, temp)
                    if (self.getSizeOfTube(j) + amount_top_i <= 4): #pour $amount_top_i water from i to j
                        temp = State(self)
                        temp.move(i, j, amount_top_i)
                        result.insert(0, temp)
        return result
    def goal_state(self) -> bool:
        for tube in range(len(self.mat)):
            type_tube = self.getTypeOfTube(tube)
            if (type_tube == 2) or (type_tube == 0):
                return False
        return True
    def getMoves(self, prev_state):
        s = ""
        src, des = 0, 0
        for i in range(len(self.mat)):
            if self.mat[i] != prev_state.mat[i]:
                if (len(self.mat[i]) < len(prev_state.mat[i])):
                    src = i
                else:
                    des = i
            else:
                continue
        s = "Pour from Tube " + str(src+1) + " to Tube " + str(des+1)
        return s
    def display_state(self):
        s = "---------\n"
        n = len(self.mat)
        if n == 0:
            return ""
        for i in range(n):
            s += "Tube " + str(i+1) + ":"
            for element in self.mat[i]:
                s += element + " "
            s += "\n"
        s += '=======================\n'
        return s
class watersort_manage():
    def __init__(self,filename):
        self.filename = filename
        self.init_state = State()
        with open(os.path.join(indir,filename), "r") as f:
            self.numTubes, self.numColors = [int(x) for x in next(f).split()] # read first line
            self.colors = set()
            for line in f: # read rest of lines
                tube = [x for x in line.split()]
                for x in tube:
                    self.colors.add(x)
                self.init_state.addTube(tube)
            while len(self.init_state.mat) < self.numTubes:
                self.init_state.addTube([])
        self.steps = []
        self.outfile = self.filename.replace('input', 'output')
    def display_res(self):
        with open(os.path.join(outdir,self.outfile), "w") as f:
            for i in range(len(self.steps)):
                s = self.steps[i].display_state()
                if s == "":
                    f.write("CANNOT SOLVE")
                    return
                if i != 0:
                    f.write("Step " + str(i) + ": " + self.steps[i].getMoves(self.steps[i-1]) + "\n")
                else:
                    f.write("Initial State\n")
                f.write(self.steps[i].display_state())
            f.write("DONE")

class watersort_dfs(watersort_manage):
    def __init__(self,filename):
        watersort_manage.__init__(self,filename)
        self.steps = self.dfs()
        self.outfile = self.outfile.replace('.txt', '_dfs.txt')
    def dfs(self):
        stack = [(self.init_state, [self.init_state])]
        while stack:
            (vertex, path) = stack.pop()
            if vertex.goal_state():
                return path

            for next_element in vertex.next_state(self.numTubes):
                stack.append((next_element, path + [next_element]))
        path.append(State())
        return path
class watersort_Astar(watersort_manage):
    def __init__(self,filename):
        watersort_manage.__init__(self,filename)
        self.steps = self.Astar()
        self.outfile = self.outfile.replace('.txt', '_Astar.txt')
    def heuristic_function(self, state):
        scores = 0
        bottomColors = dict()
        for color in self.colors:
            bottomColors[color] = 0
        for i in range(self.numTubes):
            for j in range(len(state.mat[i])):
                if j == 0:
                    bottomColors[state.mat[i][j]] += 1
                else:
                    if state.mat[i][j] != state.mat[i][j-1]:
                        scores += 1
        for color in bottomColors.keys():
            if bottomColors[color] != 0:
                scores += (bottomColors[color]-1)
            else:
                continue
        return scores
    def Astar(self):
        unique = count()
        open_list = PriorityQueue()
        open_list.put((0 + self.heuristic_function(self.init_state), next(unique), [self.init_state, 0]))
        parent = dict()
        parent[self.init_state] = None
        while open_list.empty() == False:
            (f, unique_num ,state_and_g) = open_list.get()
            g_next = state_and_g[1] + 1
            if state_and_g[0].goal_state():
                path = [state_and_g[0]]
                parent_node = parent[state_and_g[0]]
                while parent_node != None:
                    path.append(parent_node)
                    parent_node = parent[parent_node] 
                path.reverse()
                return path
    
            for next_state in state_and_g[0].next_state(self.numTubes):
                check_node_queue = False
                index = 0
                for node in open_list.queue:
                    if next_state.mat == node[2][0].mat:
                        check_node_queue = True
                        break
                    index += 1
                f = g_next + self.heuristic_function(next_state)
                if check_node_queue == False:
                    open_list.put((f, next(unique), [next_state, g_next]))
                    parent[next_state] = state_and_g[0]
                elif open_list.queue[index][0] > f:
                    temp = PriorityQueue()
                    for node in open_list.queue:
                        if node[2][0].mat == next_state.mat:
                            temp.put((f, next(unique), [next_state, g_next]))
                        else:
                            temp.put(node)
                    open_list.queue =  temp
                    parent[next_state] = state_and_g[0]
        path = [State()]
        return path
