import time
import math
import queue
import resource

class Priority_Queue(queue.PriorityQueue):           # MANAHTTAN DISTANCE

    def addSet(self,explored,item):
        explored.add(item)
        return explored

class State:
    
    def __init__(self,state):
        
        self.state = state[:]
        self.goal = [i for i in range(0,len(self.state))]
        self.path = []
        
    def getSize(self):
        return len(self.state)
        
    def getState(self):
        return self.state
    
    def getGoal(self):
        return self.goal
    
    def checkState(self):
        return self.state == self.goal
    
    def writePath(self,string):
        
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
    
    '''
    this class controls the moves on the board at a low-level
    '''
    
    def __init__(self,state):
        
        self.state = state[:]
        self.n = int(math.sqrt(len(self.state)))
        
    def getSizeBoard(self):
        return self.n
    
    # this four methods return the different possible new configurations starting in a generic point
    
    def up(self,index):
        
        stateC = self.state[:]
        stateC[index], stateC[index-self.n] = stateC[index-self.n], stateC[index]
        return stateC

    def down(self,index):
        
        stateC = self.state[:]
        stateC[index], stateC[index+self.n] = stateC[index+self.n], stateC[index]
        return stateC

    def left(self,index):
        
        stateC = self.state[:]
        stateC[index], stateC[index-1] = stateC[index-1], stateC[index]
        return stateC

    def right(self,index):
        
        stateC = self.state[:]
        stateC[index], stateC[index+1] = stateC[index+1], stateC[index]
        return stateC
    
    # these add the new state to the frontier
    
    def getUp(self,index,frontier,explored,cost,path_cost):
        
        u = self.up(index)
        weight = cost.manhattanCost(path_cost,u)
        if str(u) not in explored:
            frontier.put(tuple((weight,1,u)))
            return frontier, u
        return frontier, -1
            
    def getDown(self,index,frontier,explored,cost,path_cost):
        
        d = self.down(index)
        weight = cost.manhattanCost(path_cost,d)
        if str(d) not in explored:
            frontier.put(tuple((weight,2,d)))
            return frontier, d
        return frontier, -1
            
    def getLeft(self,index,frontier,explored,cost,path_cost):
        
        l = self.left(index)
        weight = cost.manhattanCost(path_cost,l)
        if str(l) not in explored:
            frontier.put(tuple((weight,3,l)))
            return frontier, l
        return frontier, -1
            
    def getRight(self,index,frontier,explored,cost,path_cost):
        
        r = self.right(index)
        weight = cost.manhattanCost(path_cost,r)
        if str(r) not in explored:
            frontier.put(tuple((weight,4,r)))
            return frontier, r
        return frontier, -1

class Cost:
    
    def __init__(self,n):
        
        self.n = n
        self.cost_tot = 0

    def heuristic(self,state):
        h = []
        for index, val in enumerate(state):
            print(index,val)
            if val !=0:
                
                row_correct = val//self.n
                col_correct = val%self.n

                row_actual = index//self.n
                col_actual = index%self.n

                h.append(abs(col_actual-col_correct)+abs(row_actual-row_correct))
                print(h)

        return sum(h)

    def manhattanCost(self,path_cost,state):

        self.cost_tot = path_cost + self.heuristic(state)

        return self.cost_tot



class Neighbours(Board):
    
    
    def __init__(self,state):
        
        self.state = state[:]
        self.n = int(math.sqrt(len(self.state)))
        self.max_fringe_size = 0
        self.node_list = []
        
    def getIndex(self):
        for index in range(len(self.state)):
            if self.state[index] == 0:
                return index
            
    def computeChildren(self,elements,index,frontier,explored,cost,path_cost):
        
        for element in elements:

            if element == "U":
                frontier, u = self.getUp(index,frontier,explored,cost,path_cost)
                if u != -1:
                    self.node_list.append([u,"U"])
            elif element == "D":
                frontier, d = self.getDown(index,frontier,explored,cost,path_cost)
                if d != -1:
                    self.node_list.append([d,"D"])
            elif element == "L":
                frontier, l = self.getLeft(index,frontier,explored,cost,path_cost)
                if l != -1:
                    self.node_list.append([l,"L"])
            elif element == "R":
                frontier, r = self.getRight(index,frontier,explored,cost,path_cost)
                if r != -1:
                    self.node_list.append([r,"R"])
        return frontier
    
    def neighboursAST(self,frontier,explored,cost,path_cost):
        
        index = self.getIndex()
    
        if index == 0:
            frontier = self.computeChildren(["D","R"],index,frontier,explored,cost,path_cost)
            
        elif index == (self.n-1):
            frontier = self.computeChildren(["D","L"],index,frontier,explored,cost,path_cost)
                
        elif index == self.n*(self.n-1):
            frontier = self.computeChildren(["U","R"],index,frontier,explored,cost,path_cost)
                
        elif index == (self.n*self.n-1):
            frontier = self.computeChildren(["U","L"],index,frontier,explored,cost,path_cost)

        elif index in range(1,self.n-1):
            frontier = self.computeChildren(["D","L","R"],index,frontier,explored,cost,path_cost)
                
        elif index in range((self.n*(self.n-1))+1,(self.n*self.n)-1):
            frontier = self.computeChildren(["U","L","R"],index,frontier,explored,cost,path_cost)

        elif index%self.n == 0:            
            frontier = self.computeChildren(["U","D","R"],index,frontier,explored,cost,path_cost)
                
        elif index%self.n == self.n-1:
            frontier = self.computeChildren(["U","D","L"],index,frontier,explored,cost,path_cost)
                
        else:
            frontier = self.computeChildren(["U","D","L","R"],index,frontier,explored,cost,path_cost)
                
        return frontier
    
    def getNodeList(self):
        return self.node_list
    

def out(path_to_goal,cost_of_path,nodes_expanded,fringe_size,max_fringe_size,search_depth,max_search_depth,running_time,max_ram_usage):

    with open("output.txt", 'w') as fp:
        
        fp.write("path_to_goal: "      +   str(path_to_goal)      +  "\n")
        fp.write("cost_of_path: "      +   str(cost_of_path)      +  "\n")
        fp.write("nodes_expanded: "    +   str(nodes_expanded)    +  "\n")
        fp.write("fringe_size: "       +   str(fringe_size)       +  "\n")
        fp.write("max_fringe_size: "   +   str(max_fringe_size)   +  "\n")
        fp.write("search_depth: "      +   str(search_depth)      +  "\n")
        fp.write("max_search_depth: "  +   str(max_search_depth)  +  "\n")
        fp.write("running_time: "      +   str(running_time)      +  "\n")
        fp.write("max_ram_usage: "     +   str(max_ram_usage)     +  "\n")
        
    return None



def ast(initial_state):
    
    s = time.time()
    weight = 0
    frontier = Priority_Queue()
    frontier.put(tuple((weight,0,initial_state)))  
    nodes_expanded = 0
    max_fringe_size = 0
    max_search_depth = 0
    path_level = 0
    explored_frontier = set()
    f = {"path":"0", "depth": "1"}
    NODES = {str(initial_state) :{f["path"]:"",f["depth"]:path_level}}  # path and depth of the path
    n = len(initial_state)
    
    while frontier.empty() == False:

        state = frontier.get()
        state = state[2]
        status = State(state)
        neig = Neighbours(state)
        
        if status.checkState():
            
            fringe_size = frontier.qsize()
            path_to_goal = status.writePath(NODES[str(state)][f["path"]])
            cost_of_path = len(path_to_goal)
            search_depth = NODES[str(state)][f["depth"]]
            e = time.time()
            running_time = e-s
            max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024)
            
            return path_to_goal,cost_of_path,nodes_expanded,fringe_size,max_fringe_size,search_depth,max_search_depth,running_time,max_ram_usage 
        
        
        else:
            
            explored_frontier = frontier.addSet(explored_frontier,str(state))             # explored + frontier
            cost = Cost(n)
            path_cost = NODES[str(state)][f["depth"]]
            
            frontier = neig.neighboursAST(frontier,explored_frontier,cost,path_cost)      # select neighbours
            nodes_expanded = nodes_expanded + 1
            
            nodes = neig.getNodeList()
            for node in nodes:
                if str(node[0]) not in NODES: 
                    NODES[str(node[0])] = {f["path"]:"",f["depth"]:0}
                explored_frontier = frontier.addSet(explored_frontier,str(node[0]))
                NODES[str(node[0])][f["path"]] = NODES[str(state)][f["path"]] + node[1]
                
                path_level = NODES[str(node[0])][f["path"]]
                NODES[str(node[0])][f["depth"]] = len(path_level)
                
                if len(path_level) > max_search_depth:
                    max_search_depth += 1

                if frontier.qsize() > max_fringe_size:
                    max_fringe_size = frontier.qsize()
            
    return None