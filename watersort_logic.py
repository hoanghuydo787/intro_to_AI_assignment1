import os
import copy

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
class watersort_dfs:
    def __init__(self,filename):
        self.filename = filename
        self.init_state = State()
        with open(os.path.join(indir,filename), "r") as f:
            self.numTubes, self.numColors = [int(x) for x in next(f).split()] # read first line
            self.colors = set()
            for line in f: # read rest of lines
                tube = [x for x in line.split()]
                self.colors.add(x for x in tube)
                self.init_state.addTube(tube)
            while len(self.init_state.mat) < self.numTubes:
                self.init_state.addTube([])
    def display_res(self):
        steps = self.dfs()
        with open(os.path.join(outdir,self.filename.replace("input", "output")), "w") as f:
            for i in range(len(steps)):
                s = steps[i].display_state()
                if s == "":
                    f.write("CANNOT SOLVE")
                    return
                f.write("Step " + str(i) + "\n")
                f.write(steps[i].display_state())
            f.write("DONE")
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
