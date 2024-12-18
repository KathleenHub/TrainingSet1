import sys
from PIL import Image, ImageDraw

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self,node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1] # -1 takes the last element of the list
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier): # it inherits from the stackfrontier
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():
    def __init__(self, filename):
        #read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()
        
        #validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")
        
        #Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        #keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i,j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i,j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("#", end="")
                elif(i,j) == self.start:
                    print("A", end="")
                elif(i,j) == self.goal:
                    print("B", end="")    
                elif solution is not None and (i,j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state

        #all possible actions
        candidates =[
            ("up", (row -1, col)),
            ("down", (row +1, col)),
            ("left", (row, col-1)),
            ("right", (row, col+1))
        ]

        #Ensure actions are valid
        result = []
        for action, (r,c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r,c)))
            except IndexError:
                continue
        return result
    
    def solve(self):
        """Finds a solution to maze, if one exists."""
        # Keep track of number of states explored
        self.num_explored = 0

        #initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier() #QueueFrontier
        frontier.add(start)

        #initialize an empty explored set
        self.explored = set()

        #keep looping until solution found
        while True:
            # if nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")
            #choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1
            #if node is the goal, then we have a solution
            if node.state == self.goal:
                actions=[]
                cells=[]

                # follow parent nodes to find solution
                while node.parent is not None:
                    actions.append(node.action)
                    cells. append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            # mark node as explored
            self.explored.add(node.state)

            #add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

def output_image(maze, filename, show_solution=True, show_explored=False):
    cell_size = 50
    border = 2

    img = Image.new(
        "RGBA",
        (maze.width * cell_size, maze.height * cell_size),
        "white"
    )
    draw = ImageDraw.Draw(img)

    for i, row in enumerate(maze.walls):
        for j, col in enumerate(row):
            x0 = j * cell_size + border
            y0 = i * cell_size + border
            x1 = (j + 1) * cell_size - border
            y1 = (i + 1) * cell_size - border

            if col:
                draw.rectangle([x0, y0, x1, y1], fill="black")

            elif (i, j) == maze.start:
                draw.ellipse([x0, y0, x1, y1], fill="green")

            elif (i, j) == maze.goal:
                draw.ellipse([x0, y0, x1, y1], fill="red")

            elif show_solution and maze.solution and (i, j) in maze.solution[1]:
                draw.rectangle([x0, y0, x1, y1], fill="blue")

            elif show_explored and (i, j) in maze.explored:
                draw.rectangle([x0, y0, x1, y1], fill="gray")

    img.save(filename)
            
if __name__ == "__main__":
    filename = sys.argv[1]
    maze = Maze(filename)
    maze.solve()
    print("states explored:", maze.num_explored)
    maze.print()
    output_image(maze, "maze_solution.png", show_solution=True, show_explored=True)