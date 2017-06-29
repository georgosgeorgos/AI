import queue
import copy
import csv

class Sudoku:
    
    def __init__(self,start,k=0):
        
        self.start = start
        self.col = [str(i) for i in range(1,10)]
        self.row = list("ABCDEFGHI")
        self.k = k
        self.X = []
        self.S = []

    def createGrid(self):
        for i in self.row:
            temp = []
            for j in self.col:
                temp.append(i+j)
            self.X.append(temp)
        return self.X

    def initialState(self):
        index = 0
        for i in range(len(self.X)):
            temp = []
            for j in range(len(self.X[i])):
                temp.append(self.start[self.k][0][index])
                index += 1
            self.S.append(temp)
        return self.S

    def createSudoku(self):
        sudoku = {}
        for i in range(len(self.X)):
            for j in range(len(self.X[i])):
                sudoku[self.X[i][j]] = self.S[i][j]

        for i in range(len(self.X)):
            for j in range(len(self.X[i])):
                if self.S[i][j] != sudoku[self.X[i][j]]:
                    print("Problem",i,j)
        return sudoku

    
    def createDomains(self,sudoku):
        D = {k : set() for k in sudoku.keys()}
        for key in sudoku:
            if sudoku[key] != "0":
                D[key] = set(sudoku[key])
            else:
                D[key] = set([str(i) for i in range(1,10)])
        return D

    def debug(self,sudoku):
        z = 0
        for i in range(len(self.X)):
            for j in range(len(self.X[i])):
                if sudoku[self.X[i][j]] == self.start[self.k][0][z]:
                    z +=1
        if z != 81:
            print("problem:",z)
        return None
    
    
    def create(self):

        self.X = self.createGrid()
        self.S = self.initialState()
        sudoku = self.createSudoku()
        D = self.createDomains(sudoku)
        self.debug(sudoku)
        
        return sudoku, D, self.X

    def convert(self,sudoku):
        
        string = ""
        for i in range(len(self.X)):
            for j in range(len(self.X[0])):
                string += sudoku[self.X[i][j]]
        return string



class Constraint:
    
    def __init__(self,sudoku, D, X):
        
        self.X = X
        self.col = [str(i) for i in range(1,10)]
        self.row = {k:v for v,k in enumerate("ABCDEFGHI")}
    

    def neighbors(self, X_q):
        
        var_row = self.row[X_q[0]]
        var_col = int(X_q[1]) - 1
        # select box
        i_start = (var_row//3)*3
        j_start = (var_col//3)*3

        neigh = []
        i = i_start
        j = j_start
        while i < i_start+3:
            while j < j_start+3:
                neigh.append(self.X[i][j]) 
                j +=1
            i +=1
            j = j_start
        # select row
        neigh.extend(self.X[var_row])
        i = 0
        while i < len(self.X):
            neigh.append(self.X[i][var_col])
            i +=1
        if len(set(neigh)) != 21:
            print("Problem")
        neigh = set(neigh)
        neigh.remove(X_q)
        return neigh
    
    
    def forwardChecking(self,D,var, value):
        # simple inference ----> remove the value from the neighbors of the variable
        #D_copy = copy.deepcopy(D)
        neig = self.neighbors(var)

        for n in neig:
            if value in D[n]:
                D[n].remove(value)

                if len(D[n]) == 0:
                    return False, D       
        return True, D


    def unaryConstraint(self,sudoku, D,var):
        # on variables
        neig = self.neighbors(var)
        values = set(D[var])
        elements = set()
        for n in neig:
            elements.add(sudoku[n])
        for e in elements:
            if e in values:
                D[var].remove(e)
        if len(D[var]) == 0:
            return False, D
        return True, D


    def revise(self,D,X_i,X_j):   # subroutine AC3
        logic = False
        var = False
        r = []
        for x in D[X_i]:
            for y in D[X_j]:
                if x != y:
                    var = True
            if var == False:
                logic = True
                r.append(x)
            var = False
        for i in r:
            D[X_i].remove(i)
        return logic, D
    
    def AC3(self,D):
        # on binary 
        arcs = queue.PriorityQueue()
        
        for X_i in D:
            for X_j in self.neighbors(X_i):
                arcs.put((X_i,X_j))
        
        while not arcs.empty():
            X_i,X_j = arcs.get()
            logic, D = self.revise(D,X_i,X_j)
            if logic:                       # if something changes
                
                if len(D[X_i]) == 0:   # inconsistency
                    return False, D
                
                neigh = self.neighbors(X_i)
                neigh.remove(X_j)
                for X_k in neigh:
                    arcs.put((X_k,X_i))
        return True, D
    
    def MAC3(self,D, X_q):
        # on binary 
        arcs = queue.PriorityQueue()
        
        for X_j in self.neighbors(X_q):
            if len(D[X_j]) >1:
                arcs.put((X_j,X_q))
        
        while not arcs.empty():
            X_i,X_j = arcs.get()
            logic, D = self.revise(D,X_i,X_j)
            if logic:                       # if something changes
                
                if len(D[X_i]) == 0:   # inconsistency
                    return False, D
                
                neigh = self.neighbors(X_i)
                neigh.remove(X_j)
                for X_k in neigh:
                    arcs.put((X_k,X_i))
        return True, D
    
    
    def newState(self,sudoku,D):
        sudoku = {k:"0" for k in sudoku.keys()}
        for key in D:
            if len(D[key]) == 1:
                sudoku[key] = str(list(D[key])[0])
        return sudoku



class Check:
    
    def __init__(self,sudoku, D, X):
        
        self.X = X
        self.col = [str(i) for i in range(1,10)]
        self.row = {k:v for v,k in enumerate("ABCDEFGHI")}
    
    def checkGoal(self, sudoku):
        # check rows
        i = 0
        j = 0
        allDiff = 0
        goal = set([str(i) for i in range(1,10)])
        s = []
        while i < len(self.X):
            while j < len(self.X[0]):
                s.append(sudoku[self.X[i][j]])
                j +=1
            j = 0
            i +=1
            if set(s) == goal:
                allDiff += 1
            s = []
        # check cols
        i = 0
        j = 0
        s = []
        while j < len(self.X[0]):
            while i < len(self.X):    
                s.append(sudoku[self.X[i][j]])
                i +=1
            i = 0
            j +=1
            if set(s) == goal:
                allDiff += 1
            s = []
        # check boxs
        i = 0
        j = 0
        k = 1
        s = []
        while k < 4:
            while i < len(self.X):
                while j < 3*k:
                    s.append(sudoku[self.X[i][j]])
                    j += 1
                i += 1
                j = 3*(k-1)
                if i%3 == 0:
                    if set(s) == goal:
                        allDiff += 1
                    s = []
            i = 0
            k += 1
        return allDiff == len(self.X)*(k-1)
    
    
    def neighbors(self, X_q):
        
        var_row = self.row[X_q[0]]
        var_col = int(X_q[1]) - 1
        # select box
        i_start = (var_row//3)*3
        j_start = (var_col//3)*3

        neigh = []
        i = i_start
        j = j_start
        while i < i_start+3:
            while j < j_start+3:
                neigh.append(self.X[i][j]) 
                j +=1
            i +=1
            j = j_start
        # select row
        neigh.extend(self.X[var_row])
        i = 0
        while i < len(self.X):
            neigh.append(self.X[i][var_col])
            i +=1
        if len(set(neigh)) != 21:
            print("Problem")
        neigh = set(neigh)
        neigh.remove(X_q)
        return neigh
    
    
    def consistency(self, sudoku, value, var):
    # control if this value assigment for this variable is consistent or not
        logic = True
        #neig = neighbors(self.var,self.X)
        elements = set()
        for n in self.neighbors(var):
            elements.add(sudoku[n])
        if "0" in elements:
            elements.remove("0")
        if value in elements:
            logic = False
        return logic

    def countZeros(self,sudoku):
        c = []
        for key in sudoku:
            if sudoku[key] == "0":
                c.append((key,sudoku[key]))
        return c