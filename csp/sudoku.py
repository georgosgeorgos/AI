import queue
import copy
import csv
import sys
from library_sudoku import *


def backtrack(sudoku, D, X, q, PATH, n_node):

    check = Check(sudoku, D, X)
    constraint = Constraint(sudoku, D, X)

    if check.checkGoal(sudoku):
        return sudoku, D, q, PATH, n_node

    if q.qsize() == 0:
        logic, D = constraint.AC3(D)
        sudoku = constraint.newState(sudoku, D)
        return sudoku, D, q, PATH, n_node

    var = q.get()[1]
    n_node += 1

    values = set(D[var])  # copy of the values set of variable into domain
    # values = values

    for value in values:
        if value in D[var]:

            D_copy, sudoku_copy = copy.deepcopy(D), copy.deepcopy(sudoku)
            check = Check(sudoku_copy, D_copy, X)

            if check.consistency(sudoku_copy, value, var):  # check consistency for this value
                # make a copy to check if the assigment is right or not
                D_copy[var] = set(value)
                constraint = Constraint(sudoku_copy, D_copy, X)
                logic, D_copy = constraint.MAC3(D_copy, var)  # inference part (try AC-3)
                sudoku_copy = constraint.newState(sudoku_copy, D_copy)
                if logic:
                    sudoku_copy, D_copy, q, PATH, n_node = backtrack(
                        sudoku_copy, D_copy, X, q, PATH, n_node
                    )  # DON'T ASSIGN TO sudoku, D because return False globally for every problem
                    if sudoku_copy != False:
                        return sudoku_copy, D_copy, q, PATH, n_node

    return False, D, q, PATH, n_node


def main(start, r):

    PATH = {}
    n_node = 0
    N = len(start)
    L = []

    for k in r:

        sudokuClass = Sudoku(start, k)
        sudoku, D, X = sudokuClass.create()

        q = queue.PriorityQueue()
        constraint = Constraint(sudoku, D, X)
        logic, D = constraint.AC3(D)
        sudoku = constraint.newState(sudoku, D)

        for key in D:

            PATH[key] = {}
            q.put((len(D[key]), key))  # data structure to deal with LRV

        sudoku, D, q, PATH, n_node = backtrack(sudoku, D, X, q, PATH, n_node)

    return sudoku


string = sys.argv

string = string[1]
k = 0
start = []
start.append([string])

sudoku = main(start, [k])

grid = Sudoku(start, k)
X = grid.createGrid()

string = grid.convert(sudoku)

with open("output.txt", "w", newline="") as fp:

    fp.write(string)
