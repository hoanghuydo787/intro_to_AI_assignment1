import os

MAX_ELEMENTS = 4
numTubes = 2 #number of tubes
numColors = 1 #number of colors
colors = []
indir = "io_watersort/input"

def getTypeOfTube(tube) -> int:
    n = len(tube)
    if n == 0:
        return -1 #empty tube
    for i in range(n - 1):
        if tube[i] != tube[i+1]:
            return 2 #tube has more than one color
    if n == MAX_ELEMENTS:
        return 1 #tube has one color and full (goal tube)
    return 0 #tube has one color and is not full
    
def goal_state(state) -> bool:
    for tube in state:
        if (getTypeOfTube(tube) == 2) or (getTypeOfTube(tube) == 0):
            return False
    return True
def read_input(filename, state):
    with open(os.path.join(indir,filename), "r") as f:
        global numTubes, numColors
        numTubes, numColors = [int(x) for x in next(f).split()] # read first line
        for line in f: # read rest of lines
            state.append([x for x in line.split()])
        while len(state) < numTubes:
            state.append([])
def size_top(tube)-> int:
    count = 1
    for i in range(len(tube) - 2, -1, -1):
        if tube[i] == tube[i+1]:
            count += 1
        else:
            break
    return count
def move(tube1, tube2, amount): #pour amount water from tube1 to tube2
    for i in range(amount):
        temp = tube1.pop()
        tube2.append(temp)

def next_state(current_state):
    result = []
    tube_type = [getTypeOfTube(tube) for tube in current_state]
    for i in range(numTubes-1):
        if (tube_type[i] == 1):
            continue
        for j in range(i + 1,numTubes,1):
            if (tube_type[j] == 1):
                continue
            if (tube_type[i] + tube_type[j] == 2) or (tube_type[i] + tube_type[j] == 0): # 0 + 0, 2 + 0, 0 + 2: has tube type 0
                if current_state[j][-1] != current_state[i][-1]: # tops of 2 tubes have different colors
                    continue
                temp = [row[:] for row in current_state]
                if tube_type[j] == 0: # 0 + 0, 2 + 0
                    move(temp[i], temp[j], size_top(temp[i]))
                    if tube_type[i] == 2 and (len(current_state[i]) + len(current_state[j]) <= 4):
                        temp2 = [row[:] for row in current_state]
                        move(temp2[j], temp2[i], len(temp2[j]))
                        result.insert(0, temp2)
                else: # 0 + 2
                    move(temp[j], temp[i], size_top(temp[j]))
                    if len(current_state[i]) + len(current_state[j]) <= 4:
                        temp2 = [row[:] for row in current_state]
                        move(temp2[i], temp2[j], len(temp2[i]))
                        result.insert(0, temp2)
                result.append(temp)
            elif (tube_type[i] + tube_type[j] == 1): # 2 + (-1), (-1) + 2: empty tube and tube that has >=2 colors
                temp = [row[:] for row in current_state]
                if tube_type[j] == -1: # 2 + (-1)
                    move(temp[i], temp[j], size_top(temp[i]))
                else: # (-1) + 2
                    move(temp[j], temp[i], size_top(temp[j]))
                result.insert(0, temp)
            elif (tube_type[i] + tube_type[j] == 4): # 2 + 2: both 2 tubes which have >=2 colors
                if current_state[j][-1] != current_state[i][-1]: # tops of 2 tubes have different colors
                    continue
                amount_top_i = size_top(current_state[i])
                amount_top_j = size_top(current_state[j])
                if (len(current_state[i]) + amount_top_j <= 4): #pour $amount_top_j water from j to i
                    temp = [row[:] for row in current_state]
                    move(temp[j], temp[i], amount_top_j)
                    result.insert(0, temp)
                if (len(current_state[j]) + amount_top_i <= 4): #pour $amount_top_i water from i to j
                    temp = [row[:] for row in current_state]
                    move(temp[i], temp[j], amount_top_i)
                    result.insert(0, temp)
    return result
def display_state(state):
    s = "---------\n"
    for i in range(numTubes):
        s += "Tube " + str(i+1) + ":"
        for element in state[i]:
            s += element + " "
        s += "\n"
    s += '=======================\n'
    return s
