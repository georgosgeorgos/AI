import time
import resource
import math


class Stack:  # LIFO
    def __init__(self):
        self.items = []
        self.set_items = set()

    def empty(self):
        return self.items == []

    def put(self, item):
        self.items.append(item)
        self.set_items.add(str(item))

    def get(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def list_format(self):
        return self.items

    def set_format(self):
        return self.set_items

    def set_remove(self, elements, NODES):
        for element in elements:
            self.set_items.remove(element)
            del NODES[element]
        return NODES


class State:
    def __init__(self, state):

        self.state = state[:]
        self.goal = [i for i in range(0, len(self.state))]
        self.path = []

    def getSize(self):
        return len(self.state)

    def getState(self):
        return self.state

    def getGoal(self):
        return self.goal

    def checkState(self):
        return self.state == self.goal

    def writePath(self, string):

        for s in string:

            if s == "U":
                self.path.append("Up")

            elif s == "D":
                self.path.append("Down")

            elif s == "L":
                self.path.append("Left")

            elif s == "R":
                self.path.append("Right")

        return self.path


class Board:

    """
    this class controls the moves on the board at a low-level
    """

    def __init__(self, state):

        self.state = state[:]
        self.n = int(math.sqrt(len(self.state)))

    def getSizeBoard(self):
        return self.n

    # this four methods return the different possible new configurations starting in a generic point

    def up(self, index):

        stateC = self.state[:]
        stateC[index], stateC[index - self.n] = stateC[index - self.n], stateC[index]
        return stateC

    def down(self, index):

        stateC = self.state[:]
        stateC[index], stateC[index + self.n] = stateC[index + self.n], stateC[index]
        return stateC

    def left(self, index):

        stateC = self.state[:]
        stateC[index], stateC[index - 1] = stateC[index - 1], stateC[index]
        return stateC

    def right(self, index):

        stateC = self.state[:]
        stateC[index], stateC[index + 1] = stateC[index + 1], stateC[index]
        return stateC

    # these add the new state to the frontier

    def getUp(self, index, frontier, explored):

        u = self.up(index)
        if str(u) in explored:
            return frontier, -1
        frontier.put(u)
        return frontier, u

    def getDown(self, index, frontier, explored):

        d = self.down(index)
        if str(d) in explored:
            return frontier, -1
        frontier.put(d)
        return frontier, d

    def getLeft(self, index, frontier, explored):

        l = self.left(index)
        if str(l) in explored:
            return frontier, -1
        frontier.put(l)
        return frontier, l

    def getRight(self, index, frontier, explored):

        r = self.right(index)
        if str(r) in explored:
            return frontier, -1
        frontier.put(r)
        return frontier, r


class Neighbours(Board):
    def __init__(self, state):

        self.state = state[:]
        self.n = int(math.sqrt(len(self.state)))
        self.node_list = []

    def getIndex(self):
        for index in range(len(self.state)):
            if self.state[index] == 0:
                return index

    def computeChildren(self, elements, index, frontier, explored):

        for element in elements:
            if element == "U":
                frontier, u = self.getUp(index, frontier, explored)
                if u != -1:
                    self.node_list.append([u, "U"])
            elif element == "D":
                frontier, d = self.getDown(index, frontier, explored)
                if d != -1:
                    self.node_list.append([d, "D"])
            elif element == "L":
                frontier, l = self.getLeft(index, frontier, explored)
                if l != -1:
                    self.node_list.append([l, "L"])
            elif element == "R":
                frontier, r = self.getRight(index, frontier, explored)
                if r != -1:
                    self.node_list.append([r, "R"])
        return frontier

    def neighboursDFS(self, frontier, explored):

        index = self.getIndex()

        if index == 0:
            frontier = self.computeChildren(["R", "D"], index, frontier, explored)

        elif index == (self.n - 1):
            frontier = self.computeChildren(["L", "D"], index, frontier, explored)

        elif index == self.n * (self.n - 1):
            frontier = self.computeChildren(["R", "U"], index, frontier, explored)

        elif index == (self.n * self.n - 1):
            frontier = self.computeChildren(["L", "U"], index, frontier, explored)

        elif index in range(1, self.n - 1):
            frontier = self.computeChildren(["R", "L", "D"], index, frontier, explored)

        elif index in range((self.n * (self.n - 1)) + 1, (self.n * self.n) - 1):
            frontier = self.computeChildren(["R", "L", "U"], index, frontier, explored)

        elif index % self.n == 0:
            frontier = self.computeChildren(["R", "D", "U"], index, frontier, explored)

        elif index % self.n == self.n - 1:
            frontier = self.computeChildren(["L", "D", "U"], index, frontier, explored)

        else:
            frontier = self.computeChildren(["R", "L", "D", "U"], index, frontier, explored)

        return frontier

    def getNodeList(self):
        return self.node_list


def extractTotalPath(state, NODES, f):

    state = state[:]
    path_tot = NODES[state][f["move"]]
    parent_move = -1
    while parent_move != "":

        parent = NODES[state][f["parent"]]
        parent_move = NODES[parent][f["move"]]

        path_tot = parent_move + path_tot
        state = parent

    return path_tot


def out(
    path_to_goal,
    cost_of_path,
    nodes_expanded,
    fringe_size,
    max_fringe_size,
    search_depth,
    max_search_depth,
    running_time,
    max_ram_usage,
):

    with open("output.txt", "w") as fp:

        fp.write("path_to_goal: " + str(path_to_goal) + "\n")
        fp.write("cost_of_path: " + str(cost_of_path) + "\n")
        fp.write("nodes_expanded: " + str(nodes_expanded) + "\n")
        fp.write("fringe_size: " + str(fringe_size) + "\n")
        fp.write("max_fringe_size: " + str(max_fringe_size) + "\n")
        fp.write("search_depth: " + str(search_depth) + "\n")
        fp.write("max_search_depth: " + str(max_search_depth) + "\n")
        fp.write("running_time: " + str(running_time) + "\n")
        fp.write("max_ram_usage: " + str(max_ram_usage) + "\n")

    return None


def dfs(initial_state):

    s = time.time()
    frontier = Stack()
    frontier.put(initial_state)
    nodes_expanded = 0
    max_fringe_size = 0
    max_search_depth = 0
    path_level = 0
    f = {"path": "0", "depth": "1", "move": "2", "parent": "3"}
    value = False
    NODES = {str(initial_state): {f["path"]: "", f["depth"]: path_level, f["move"]: "", f["parent"]: ""}}

    while frontier.empty() == False:

        state = frontier.get()
        status = State(state)
        neig = Neighbours(state)

        if status.checkState():

            fringe_size = frontier.size()
            path_to_goal = extractTotalPath(str(state), NODES, f)
            path_to_goal = status.writePath(path_to_goal)
            cost_of_path = len(path_to_goal)
            search_depth = NODES[str(state)][f["depth"]]
            e = time.time()
            running_time = e - s
            max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)

            return (
                path_to_goal,
                cost_of_path,
                nodes_expanded,
                fringe_size,
                max_fringe_size,
                search_depth,
                max_search_depth,
                running_time,
                max_ram_usage,
            )

        else:

            explored_frontier = frontier.set_format()  # explored + frontier
            frontier = neig.neighboursDFS(frontier, explored_frontier)  # select neighbours
            nodes_expanded += 1

            nodes = neig.getNodeList()

            if value:
                parent = NODES[str(state)][f["parent"]]
                path_level = NODES[parent][f["depth"]] + 1
                value = False

            NODES[str(state)]["depth"] = path_level
            path_level = path_level + 1

            for node in nodes:
                if str(node[0]) not in NODES:
                    NODES[str(node[0])] = {
                        f["path"]: "",
                        f["depth"]: path_level,
                        f["move"]: node[1],
                        f["parent"]: str(state),
                    }

            if nodes != []:
                node = nodes[-1]
                NODES[str(node[0])][f["path"]] = NODES[str(state)][f["path"]] + node[1]

                if path_level > max_search_depth:
                    max_search_depth = path_level

                if frontier.size() > max_fringe_size:
                    max_fringe_size = frontier.size()

            if nodes == []:
                value = True

    return None
