from time import sleep
from math import *
import sys
import tkinter as tk


class Node:
    i = j = -1
    Parent = (-1, -1)
    g = h = f = -1
    children = []
    blocked = False

    def __init__(self, position, parent = None):
        i = position[0]
        j = position[1]
        if parent is not None:
            self.Parent[0] = parent[0]
            self.Parent[1] = parent[1]
        self.children = []
        self.blocked = False


class Tree:
    Root = None
    CELL_DETAILS = []

    def isValid(self, i, j):
        if 0 <= i <= ROW-1:
            if 0 <= j <= COL-1:
                return True
            else:
                return False
        else:
            return False

    def isDestionation(self, i, j):
        if d_row == i and d_col == j:
            return True
        else:
            return False

    def isBlocked(self, i, j, matrix):
        if matrix[i][j] == 0:
            return True
        else:
            return False

    def Populate(self, matrix):
        self.Root = Node((s_row, s_col))
        self.Root.i = s_row
        self.Root.j = s_col
        self.Root.g = 0


        cellDetails = []
        for i in range(ROW):
            cellDetails.append([])
            for j in range(COL):
                cellDetails[i].append(Node((i, j)))

        for i in range(ROW):
            for j in range(COL):
                if matrix[i][j] == 0:
                    cellDetails[i][j].blocked = True
                else:
                    cellDetails[i][j].blocked = False

        for i in range(ROW):
            for j in range(COL):
                if not self.isBlocked(i, j, matrix):
                    cellDetails[i][j].i = i
                    cellDetails[i][j].j = j
                    position = (i, j)
                    r = position[0]
                    c = position[1]
                    count = 0
                    if self.isValid(r + 1, c) and not self.isBlocked(r + 1, c, matrix): # and (r + 1, c) not in closedList:
                        if (r + 1, c) not in cellDetails[r][c].children:
                            cellDetails[r][c].children.append((r + 1, c))
                            cellDetails[r + 1][c].Parent = (r, c)
                        count += 1
                    if self.isValid(r - 1, c) and not self.isBlocked(r - 1, c, matrix): # and (r - 1, c) not in closedList:
                        if (r - 1, c) not in cellDetails[r][c].children:
                            cellDetails[r][c].children.append((r - 1, c))
                            cellDetails[r - 1][c].Parent = (r, c)
                        count += 1
                    if self.isValid(r, c + 1) and not self.isBlocked(r, c + 1, matrix): # and (r, c + 1) not in closedList:
                        if (r, c + 1) not in cellDetails[r][c].children:
                            cellDetails[r][c].children.append((r, c + 1))
                            cellDetails[r][c + 1].Parent = (r, c)
                        count += 1
                    if self.isValid(r, c - 1) and not self.isBlocked(r, c - 1, matrix): # and (r, c - 1) not in closedList:
                        if (r, c - 1) not in cellDetails[r][c].children:
                            cellDetails[r][c].children.append((r, c - 1))
                            cellDetails[r][c - 1].Parent = (r, c)
                        count += 1
                else:
                    pass
        self.CELL_DETAILS = cellDetails
        return

    def display(self):
        for i in range(ROW):
            for j in range(COL):
                print("Current Node : " + str(i) + ", " + str(j))
                print("It's Parent : " + str(self.CELL_DETAILS[i][j].Parent[0]) + ", " + str(self.CELL_DETAILS[i][j].Parent[1]))
                print("G = " + str(self.CELL_DETAILS[i][j].g))
                print("H = " + str(self.CELL_DETAILS[i][j].h))
                print("F = " + str(self.CELL_DETAILS[i][j].f))
                print("Blocked: " + str(self.CELL_DETAILS[i][j].blocked))
                print("Children of : " + str(i) + ", " + str(j))
                print(self.CELL_DETAILS[i][j].children)
                print("********************************")

    def assignG(self):
        for i in range(ROW):
            for j in range(COL):
                if self.CELL_DETAILS[i][j].g == -1:
                    self.CELL_DETAILS[i][j].g = self.CELL_DETAILS[self.CELL_DETAILS[i][j].Parent[0]][self.CELL_DETAILS[i][j].Parent[1]].g + 1
                else:
                    pass

    def assignHF(self):
        for i in range(ROW):
            for j in range(COL):
                if self.CELL_DETAILS[i][j].blocked:
                    self.CELL_DETAILS[i][j].h = sys.float_info.max
                    self.CELL_DETAILS[i][j].f = self.CELL_DETAILS[i][j].g + self.CELL_DETAILS[i][j].h
                else:
                    if self.CELL_DETAILS[i][j].h == -1:
                        self.CELL_DETAILS[i][j].h = EuclideanDistance((i, j), (d_row, d_col))
                        self.CELL_DETAILS[i][j].f = self.CELL_DETAILS[i][j].g + self.CELL_DETAILS[i][j].h
                    else:
                        pass

    def findPath(self):
        global STATE
        frontier = []
        path = []
        for child in self.CELL_DETAILS[self.Root.i][self.Root.j].children:
            frontier.append(self.CELL_DETAILS[child[0]][child[1]])
        path.append((s_row, s_col))

        while True:
            if len(frontier) == 0:
                STATE = "NOT FOUND"
                print("Destination Not Found!")
                break

            selected = frontier[0]
            for obj in path:
                if self.CELL_DETAILS[obj[0]][obj[1]] in frontier:
                    frontier.remove(self.CELL_DETAILS[obj[0]][obj[1]])
            for x in frontier:
                if x.f < selected.f:
                    selected = x
            if selected in frontier:
                frontier.remove(selected)
            path.append((selected.i, selected.j))

            if self.isDestionation(selected.i, selected.j):
                STATE = "FOUND"
                print("Destination Found!")
                break
            for child in self.CELL_DETAILS[selected.i][selected.j].children:
                if (child[0], child[1]) not in path:
                    frontier.append(self.CELL_DETAILS[child[0]][child[1]])

        global PATH
        PATH = path

    def prune(self):
        global PATH

        root = self.CELL_DETAILS[PATH[len(PATH)-1][0]][PATH[len(PATH)-1][1]]
        parent = root
        index = len(PATH) - 2
        path = []
        while index >= 0:
            node = self.CELL_DETAILS[PATH[index][0]][PATH[index][1]]
            if (node.i, node.j) in parent.children:
                path.append((node.i, node.j))
                parent = node
            index -= 1
        PATH = path


def EuclideanDistance(a, b):
    x1 = a[0]
    y1 = a[1]
    x2 = b[0]
    y2 = b[1]
    return sqrt(((x2-x1)*(x2-x1)) + ((y2-y1)*(y2-y1)))

PATH = []

ROW = 40
COL = 40

MAP = []

s_row = 0
s_col = 0
d_row = 0
d_col = 0

STATE = "START"


def convertMAP():
    conMAP = []
    for i in range(ROW):
        conMAP.append([])
    for i in range(ROW):
        for j in range(COL):
            if MAP[i][j] == 'r' or MAP[i][j] == 'i' or MAP[i][j]=='d':
                conMAP[i].append(1)
            else:
                conMAP[i].append(0)
    return conMAP


def walk(x1, y1, x2, y2):
    c.create_rectangle(y1, x1, y2, x2, fill="yellow")


def animatePath():
    global PATH

    for i in range(len(PATH)):
        x1 = PATH[i][0] * 10
        y1 = PATH[i][1] * 10
        x2 = x1+10
        y2 = y1+10

        if i != 0 and i!=len(PATH)-1:
            walk(x1, y1, x2, y2)

    PATH = []


def SearchPath():
    global STATE
    STATE = "SEARCH"
    map = convertMAP()

    tree = Tree()
    tree.Populate(map)
    tree.assignG()
    tree.assignHF()
    tree.findPath()

    tree.prune()
    if STATE == "FOUND":
        pass
        animatePath()


def CreateObstacles():
    global STATE
    STATE = "CreateObstacles"


def operate(event):
    # for x
    xrounded = round(event.x, -1)
    if abs((xrounded - 10) - event.x) < abs((xrounded + 10) - event.x):
        xrounded2 = xrounded - 10
    else:
        xrounded2 = xrounded + 10
    if xrounded > xrounded2:
        x1 = xrounded2
        x2 = xrounded
    else:
        x1 = xrounded
        x2 = xrounded2

    # for y
    yrounded = round(event.y, -1)
    if abs((yrounded - 10) - event.y) < abs((yrounded + 10) - event.y):
        yrounded2 = yrounded - 10
    else:
        yrounded2 = yrounded + 10
    if yrounded > yrounded2:
        y1 = yrounded2
        y2 = yrounded
    else:
        y1 = yrounded
        y2 = yrounded2
    global STATE

    if MAP[int(y1/10)][int(x1/10)] == 'r' and STATE == "CreateObstacles":
        c.create_rectangle(x1, y1, x2, y2, fill="black")
        st = ""
        for i in range(len(MAP[int(y1 / 10)])):
            if i != int(x1/10):
                st += MAP[int(y1 / 10)][i]
            else:
                st += 'w'
        MAP[int(y1 / 10)] = st

    elif MAP[int(y1/10)][int(x1/10)] == 'r' and STATE == "INIT":
        c.create_rectangle(x1, y1, x2, y2, fill="blue")
        st = ""
        for i in range(len(MAP[int(y1 / 10)])):
            if i != int(x1 / 10):
                st += MAP[int(y1 / 10)][i]
            else:
                st += 'i'
        MAP[int(y1 / 10)] = st
        global s_row, s_col
        s_row = int(y1 / 10)
        s_col = int(x1/10)
        STATE = "START"
    elif MAP[int(y1/10)][int(x1/10)] == 'r' and STATE == "DEST":
        c.create_rectangle(x1, y1, x2, y2, fill="red")
        st = ""
        for i in range(len(MAP[int(y1 / 10)])):
            if i != int(x1 / 10):
                st += MAP[int(y1 / 10)][i]
            else:
                st += 'd'
        MAP[int(y1 / 10)] = st
        global d_row, d_col
        d_row = int(y1 / 10)
        d_col = int(x1 / 10)
        STATE = "START"


def create_grid(event=None):
    w = c.winfo_width()
    h = c.winfo_height()
    c.delete('grid_line')

    for i in range(0, w, 10):
        c.create_line([(i, 0), (i, h)], tag='grid_line')

    for i in range(0, h, 10):
        c.create_line([(0, i), (w, i)], tag='grid_line')


def create_map(event=None):
    global MAP
    MAP = []
    file = open("MAP")
    xbox = 0
    ybox = 0
    for row in file:
        MAP.append(row)
        ybox += 1
        for char in row:
            xbox += 1
            x1 = (xbox*10) - 10
            x2 = (xbox*10)
            y1 = (ybox*10) - 10
            y2 = (ybox*10)
            if char == 'w':
                c.create_rectangle(x1, y1, x2, y2, fill="black")
            elif char == 'r':
                c.create_rectangle(x1, y1, x2, y2, fill="gray")
            elif char == '-':
                c.create_rectangle(x1, y1, x2, y2, fill="green")
        xbox = 0
    STATE = "START"


def INITButton():
    global STATE
    STATE = "INIT"


def DESTButton():
    global STATE
    STATE = "DEST"


if __name__ == '__main__':
    root = tk.Tk()
    root.title("A* Search Algorithm")
    c = tk.Canvas(root, height=400, width=400, bg='white')
    c.pack(fill=tk.BOTH, expand=True)
    c.bind('<Configure>', create_grid)
    c.bind('<Configure>', create_map)
    c.bind("<Button 1>", operate)

    Reset = tk.Button(root, text="Reset", command=create_map)
    Reset.pack(side=tk.RIGHT)

    CreateObstacles = tk.Button(root, text="Create Obstacles", command=CreateObstacles)
    CreateObstacles.pack(side=tk.LEFT)

    SearchPath = tk.Button(root, text="Search Path", command=SearchPath)
    SearchPath.pack(side=tk.LEFT)

    INITButton = tk.Button(root, text="Initial Place", command=INITButton)
    INITButton.pack(side=tk.LEFT)

    DESTButton = tk.Button(root, text="Destination Place", command=DESTButton)
    DESTButton.pack(side=tk.LEFT)
    root.mainloop()