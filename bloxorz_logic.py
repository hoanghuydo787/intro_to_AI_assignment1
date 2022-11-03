import os
import copy

'''
hàng cột
map
x1 y1 x2 y2
các hàng tiếp theo thể hiện tọa độ các nút của cầu
'''
indir = "io_bloxorz/input"
outdir = "io_bloxorz/output"
# this class manage state of map
class bloxorz_state:
    def __init__(self, x1, y1, x2, y2, map, parent):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.map = copy.deepcopy(map)
        self.parent = parent
    
    def __str__(self):
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2
        res = "==================================\n"
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if ((i == y1 and j == x1) or (i == y2 and j == x2)):
                    res += 'X '
                elif self.map[i][j] == 0:
                    res += '  '
                else:
                    res += str(self.map[i][j]) + ' '
            res += '\n'
        return res

class bloxorz_manage:
    def __init__(self, input):
        self.row, self.col, map, x1, y1, x2, y2, self.buttons = self.read_input(input)
        self.init_state = bloxorz_state(x1, y1, x2, y2, map, None)

    def read_input(self, filename):
        with open(os.path.join(indir,filename), "r") as f:
            #read number of column and number of row
            row, col = [int(x) for x in next(f).split()]
            #read map
            map = []
            countLine = 0
            for line in f:
                map.append([int(x) for x in line.split()])
                countLine += 1
                if countLine == row:
                    break
            #read x1, y1, x2, y2
            x1, y1, x2, y2 = [int(x) for x in next(f).split()]
            #read button management
            # <x> <y> <type(0(openonly), 1(closeonly), 2(both))> <numOfPoint> [<xi> <yi>]
            button = []
            for line in f:
                button.append([int(x) for x in line.split()])
            
            return row, col, map, x1, y1, x2, y2, button

    def goal_state(self, state) -> bool:
        if state.x1 == state.x2 and state.y1 == state.y2:
            if state.map[state.y1][state.x1] == 2:
                return True 
        return False

    def check_valid_state(self, state) -> bool:
        x1, x2, y1, y2, map = state.x1, state.x2, state.y1, state.y2, state.map
        if min(x1, x2) >= 0 and min(y1, y2) >= 0 and max(x1, x2) < len(map[0]) and max(y1, y2) < len(map):
            if state.map[y1][x1] == 0 or state.map[y2][x2] == 0: 
                return False
            elif x1 == x2 and y1 == y2 and state.map[y1][x1] == 3: #check for red point
                return False
            return True
        return False

    def handle_button_O(self, state, buttonInfo):
        # handle for 3 case: button for only open, button for only close, button for both
        if buttonInfo[2] == 0: # button only open
            for i in range(0, buttonInfo[3]):
                state.map[buttonInfo[3+2*i+2]][buttonInfo[3+2*i+1]] = 1
        elif buttonInfo[2] == 1: # button only close
            for i in range(0, buttonInfo[3]):
                state.map[buttonInfo[3+2*i+2]][buttonInfo[3+2*i+1]] = 0
        else: #button for both
            for i in range(0, buttonInfo[3]):
                state.map[buttonInfo[3+2*i+2]][buttonInfo[3+2*i+1]] = abs(state.map[buttonInfo[3+2*i+2]][buttonInfo[3+2*i+1]] - 1)

    def handle_button_X(self, state, buttonInfo):
        # handle for 3 case: button for only open, button for only close, button for both
        if buttonInfo[2] == 0: # button only open
            for i in range(0, buttonInfo[3]):
                state.map[buttonInfo[3+2*i+2]][buttonInfo[3+2*i+1]] = 1
        elif buttonInfo[2] == 1: # button only close
            for i in range(0, buttonInfo[3]):
                state.map[buttonInfo[3+2*i+2]][buttonInfo[3+2*i+1]] = 0
        else: #button for both
            for i in range(0, buttonInfo[3]):
                state.map[buttonInfo[3+2*i+2]][buttonInfo[3+2*i+1]] = abs(state.map[buttonInfo[3+2*i+2]][buttonInfo[3+2*i+1]] - 1)

    def handle_button(self, state):
        x1, x2, y1, y2 = state.x1, state.x2, state.y1, state.y2 
        for i in self.buttons:
            if (i[0], i[1]) in [(x1, y1), (x2, y2)]:
                if (state.map[i[1]][i[0]] == 4): # 4 representation button O
                    self.handle_button_O(state, i)
                elif x1 == x2 and y1 == y2: # 5 representation for button X 
                    self.handle_button_X(state, i)

    def move_up(self, state):
        x1, x2, y1, y2 = state.x1, state.x2, state.y1, state.y2
        map = state.map
        if x1 == x2 and y1 == y2: # standing
            y1 -= 1
            y2 -= 2
        elif y1 == y2: # lying horizontal
            y1 -= 1
            y2 -= 1
        else: # lying vertical
            y1 = y2 = min(y1-1, y2-1)
        newState = bloxorz_state(x1, y1, x2, y2, map, state)
        if self.check_valid_state(newState):
            self.handle_button(newState)
            return newState
        return None

    def move_down(self, state):
        x1, x2, y1, y2 = state.x1, state.x2, state.y1, state.y2
        map = state.map
        if x1 == x2 and y1 == y2: # standing
            y1 += 1
            y2 += 2
        elif y1 == y2: # horizontal
            y1 += 1
            y2 += 1
        else: #vertical
            y1 = y2 = max(y1+1, y2+1)
        newState = bloxorz_state(x1, y1, x2, y2, map, state)
        if self.check_valid_state(newState):
            self.handle_button(newState)
            return newState
        return None

    def move_left(self, state):
        x1, x2, y1, y2 = state.x1, state.x2, state.y1, state.y2
        map = state.map
        if x1 == x2 and y1 == y2: # standing
            x1 -= 1
            x2 -= 2
        elif y1 == y2: # horizontal
            x1 = x2 = min(x1-1, x2-1)
        else: #vertical
            x1 -= 1
            x2 -= 1
        newState = bloxorz_state(x1, y1, x2, y2, map, state)
        if self.check_valid_state(newState):
            self.handle_button(newState)
            return newState
        return None

    def move_right(self, state):
        x1, x2, y1, y2 = state.x1, state.x2, state.y1, state.y2
        map = state.map
        if x1 == x2 and y1 == y2: # standing
            x1 += 1
            x2 += 2
        elif y1 == y2: # horizontal
            x1 = x2 = max(x1+1, x2+1)
        else: #vertical
            x1 += 1
            x2 += 1
        newState = bloxorz_state(x1, y1, x2, y2, map, state)
        if self.check_valid_state(newState):
            self.handle_button(newState)
            return newState
        return None

class bloxorz_bfs(bloxorz_manage):
    def __init__(self, input):
        bloxorz_manage.__init__(self, input)
        self.isVisited = []
        self.input = input

    def check_for_visited(self, state):
        for i in self.isVisited:
            if state.x1 == i.x1 and state.y1 == i.y1 and state.x2 == i.x2 and \
                state.y2 == i.y2 and state.map == i.map:
                return False
        return True

    def get_all_next_state(self, state):
        up, down, left, right = self.move_up(state), self.move_down(state), self.move_left(state), self.move_right(state)
        res = []
        if (up != None and self.check_for_visited(up)):
            res.append(up)
            self.isVisited.append(up)
        if (down != None and self.check_for_visited(down)):
            res.append(down)
            self.isVisited.append(down)
        if (left != None and self.check_for_visited(left)):
            res.append(left)
            self.isVisited.append(left)
        if (right != None and self.check_for_visited(right)):
            res.append(right)
            self.isVisited.append(right)
        return res

    def BFS(self):
        stack = [self.init_state]
        self.isVisited.append(self.init_state)
        while stack:
            cur = stack.pop()
            if self.goal_state(cur):
                # print result
                with open(os.path.join(outdir,self.input.replace("input", "output")), "w") as f:
                    states = []
                    while cur:
                        states.append(cur)
                        cur = cur.parent
                    states.reverse()
                    for i in range(len(states)):
                        f.write("Step " + str(i) + "\n")
                        f.write(str(states[i]))
            else:
                move = self.get_all_next_state(cur)
                for i in move:
                    stack.append(i)

class bloxorz_ga(bloxorz_manage):
    def __init__(self, input):
        bloxorz_manage.__init__(self, input)
        self.input = input
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if map[i][j] == 2:
                    self.x_goal, self.y_goal = i, j
        self.dna_length = len(self.map) * len(self.map[0])

    def distance_to_goal(self):
        # euclidean distance
        x1, x2, y1, y2 = state.x1, state.x2, state.y1, state.y2
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        return sqrt((x - self.x_goal) ** 2 + (y - self.y_goal) ** 2)
    
    def fitness_score(self):
        return 1 / distance_to_goal()

    def generate_dna_sequence(self):
        # dna sequence length is 2x total size of the map
        # if dna sequence leads to goal in any of its chromosome, stop the algorithm
        # chromosome of dna has 4 values(1,2,3,4), associate with 4 moves(up, down, left, right), respectively
