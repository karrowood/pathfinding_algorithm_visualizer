# Kyle Arrowood
# 7/20/2020
# A pathfinding algorithm visualizer
# This program shows a grid. The user can choose to draw barriers on the grid,
# they can then pick an algorithm and watch how that specific algorthim works.


import math
from tkinter import *
from queue import Queue

class window:
    def __init__(self, screen, canvas_width, canvas_height):
        self.screen = screen
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
    def create_window(self):
        self.screen.title("Pathfinding Algorithm Visualizer")
        option_variable = StringVar()
        option_variable.set("A* Search")
        option_menu = OptionMenu(self.screen, option_variable,
                                "A* Search", "Dijkstra's Algorithm", "Greedy Best First Search",
                                "Breadth First Search")
        # Start and end points for path
        self.start = (2, 2)
        self.end = (95, 45)
        self.rows = 50
        self.columns = 100
        option_menu.config(bg = "yellow")
        def button_callback():
            go_button["state"] = DISABLED
            option_menu["state"] = DISABLED
            clear_button["state"] = DISABLED
            move_button["state"] = DISABLED
            if option_variable.get() == "A* Search":
                path = a_star(self)
                for i, node in enumerate(path):
                    self.draw_cube(node[0], node[1], "lime")
            elif option_variable.get() == "Dijkstra's Algorithm":
                path = dijkstra(self)
                for i, node in enumerate(path):
                    self.draw_cube(node[0], node[1], "lime")
            elif option_variable.get() == "Greedy Best First Search":
                path = greedy(self)
                for i, node in enumerate(path):
                    self.draw_cube(node[0], node[1], "lime")
            elif option_variable.get() == "Breadth First Search":
                path = bfs(self)
                for i, node in enumerate(path):
                    self.draw_cube(node[0], node[1], "lime")
            self.refresh()
            go_button["state"] = "normal"
            option_menu["state"] = "normal"
            clear_button["state"] = "normal"
            move_button["state"] = "normal"
        go_button = Button(self.screen, text = "GO!", command = button_callback,
                        bg = "yellow", activebackground = "white")
        def clear_callback():
            self.create_grid()
            self.grid = [[0 for i in range(self.rows)] for j in range(self.columns)]
        clear_button = Button(self.screen, text = "Clear", command = clear_callback,
                        bg = "yellow", activebackground = "white")
        def move_callback():
            popup = Tk()
            label = Label(popup, text='x range = (0, 99)\ny range = (0, 49)')
            l1 = Label(popup, text='Start(x,y): ')
            startBox = Entry(popup)
            l2 = Label(popup, text='End(x,y): ')
            endBox = Entry(popup)
            
            def onsubmit():
                s = startBox.get().split(',')
                e = endBox.get().split(',')
                self.start = (int(s[0]), int(s[1]))
                self.end = (int(e[0]), int(e[1]))
                popup.quit()
                popup.destroy()
                self.create_grid()
            submit = Button(popup, text='Submit', command=onsubmit)
            label.grid(row = 0, columnspan = 2)
            submit.grid(columnspan = 2, row = 3)
            l2.grid(row = 2, pady = 3)
            endBox.grid(row = 2, column = 1, pady = 3)
            startBox.grid(row = 1, column = 1, pady = 3)
            l1.grid(row = 1, pady = 3)
            popup.update()
            popup.mainloop()
        move_button = Button(self.screen, text = "Move start and end nodes", command = move_callback,
                        bg = "yellow", activebackground = "white")
        option_menu.place(x = 400, y = 7)
        go_button.place(x = 625, y = 9)
        clear_button.place(x = 325, y = 9)
        move_button.place(x = 125, y = 9)
        self.canvas = Canvas(self.screen, width = self.canvas_width, height = self.canvas_height)
        def callback(event):
            # Checks range
            if not (math.floor(event.x / 10) > (len(self.grid) - 1) or math.floor(event.x / 10) < 0 or 
                math.floor(event.y / 10) > (len(self.grid[len(self.grid) - 1]) - 1) 
                or math.floor(event.y / 10) < 0):
                self.grid[math.floor(event.x / 10)][math.floor(event.y / 10)] = 1
                self.draw_cube(math.floor(event.x / 10), math.floor(event.y / 10), "black")
        self.canvas.bind("<B1-Motion>", callback)
        self.canvas.bind("<Button-1>", callback)
        self.canvas.place(x = 3, y = 50)
        self.create_grid()
        self.refresh()
        self.screen.mainloop()
    def refresh(self):
        self.canvas.update()
    def create_grid(self):
        # Creates the grid variable that will store values which will represent different colors
        self.grid = [[0 for i in range(self.rows)] for j in range(self.columns)]
        self.canvas.delete("all")
        col_width = self.canvas_width / self.columns
        position = 0
        for i in range(self.columns):
            position = position + col_width
            # Draws vertical line
            self.canvas.create_line(position, 0, position, self.canvas_height)
        row_height = self.canvas_height / self.rows
        position = 0
        for i in range(self.columns):
            position = position + row_height
            # Draws horizontal line
            self.canvas.create_line(0, position, self.canvas_width, position)
        self.draw_cube(self.start[0], self.start[1], "blue")
        self.draw_cube(self.end[0], self.end[1], "red")
    def draw_cube(self, x, y, color):
        cube_width = 10 # Constant unless size of grid changes
        self.canvas.create_rectangle(x * cube_width, y * cube_width, (x * cube_width) + cube_width, (y * cube_width) + cube_width, fill=color)
class Node:
    # Node used for greedy search
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.previous = None
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position
def get_distance(first, second):
    (x1, y1) = first
    (x2, y2) = second
    x = abs(x1 - x2)
    y = abs(y1 - y2)
    if x > y:
        return y + (x - y)
    return x + (y - x)
def a_star(window):
    # Returns list of coords of the path
    start_node = Node(None, window.start)
    end_node = Node(None, window.end)
    open_list = [start_node]
    closed_list = []
    while len(open_list) > 0:
        # Gets current
        low = 0
        for i in range(len(open_list)):
            if open_list[i].f < open_list[low].f:
                low = i
        current = open_list[low]
        open_list.pop(low)
        closed_list.append(current)
        # Checks if found end
        if current == end_node:
            path = []
            cur = current
            while cur is not None:
                path.append(cur.position)
                cur = cur.parent
            return path[::-1] # Reversed path
        for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Neighbor squares
            node_position = (current.position[0] + i[0], current.position[1] + i[1])
            # Checks range
            if node_position[0] > (len(window.grid) - 1) or node_position[0] < 0 or node_position[1] > (len(window.grid[len(window.grid) - 1]) - 1) or node_position[1] < 0:
                continue
            # Checks if it is a wall
            if window.grid[node_position[0]][node_position[1]] != 0:
                continue
            child = Node(current, node_position)
            # Child already on closed list
            if child in closed_list:
                continue
            temp_g = current.g + 1
            if temp_g < child.g or child not in open_list:
                child.g = temp_g
                child.h = get_distance(child.position, end_node.position)
                child.f = child.g + child.h
                child.parent = current
                if child not in open_list:
                    open_list.append(child)
                    window.draw_cube(current.position[0], current.position[1], "magenta")
                    window.refresh()

def dijkstra(window):
    q = Queue()
    q.put(window.start)
    path = dict()
    path[window.start] = None
    cost = dict()
    cost[window.start] = 0
    while not q.empty():
        current = q.get()
        if current == window.end:
                result = []
                while current != window.start: 
                    result.append(current)
                    current = path[current]
                result.append(window.start)
                result.reverse()
                return result
        for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Neighbor squares
            node_position = (current[0] + i[0], current[1] + i[1])
            # Checks range
            if node_position[0] > (len(window.grid) - 1) or node_position[0] < 0 or node_position[1] > (len(window.grid[len(window.grid) - 1]) - 1) or node_position[1] < 0:
                continue
            # Checks if it is a wall
            if window.grid[node_position[0]][node_position[1]] != 0:
                continue
            new_cost = cost[current] + 1
            if node_position not in cost or new_cost < cost[node_position]:
                cost[node_position] = new_cost
                path[node_position] = current
                q.put(node_position)
                window.draw_cube(node_position[0], node_position[1], "magenta")
                window.refresh()
            
def greedy(window):
    # Returns list of coords of the path
    start_node = Node(None, window.start)
    end_node = Node(None, window.end)
    open_list = [start_node]
    closed_list = []
    while len(open_list) > 0:
        # Gets current
        low = 0
        for i in range(len(open_list)):
            if open_list[i].f < open_list[low].f:
                low = i
        current = open_list[low]
        # Checks if found end
        if current == end_node:
            path = []
            cur = current
            while cur is not None:
                path.append(cur.position)
                cur = cur.parent
            return path[::-1] # Reversed path
        open_list.pop(low)
        closed_list.append(current)
        for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Neighbor squares
            node_position = (current.position[0] + i[0], current.position[1] + i[1])
            # Checks range
            if node_position[0] > (len(window.grid) - 1) or node_position[0] < 0 or node_position[1] > (len(window.grid[len(window.grid) - 1]) - 1) or node_position[1] < 0:
                continue
            # Checks if it is a wall
            if window.grid[node_position[0]][node_position[1]] != 0:
                continue
            child = Node(current, node_position)
            # Child already on closed list
            if child not in closed_list:
                temp_g = child.g + 1
                if child in open_list:
                    if child.g > temp_g:
                        child.g = temp_g
                else:
                    child.g = temp_g
                    open_list.append(child)
                child.h = get_distance(child.position, end_node.position)
                child.f = child.g + child.h
                window.draw_cube(child.position[0], child.position[1], "magenta")
                window.refresh()
def bfs(window):
    q = Queue()
    q.put(window.start)
    path = dict()
    path[window.start] = None
    while not q.empty():
        current = q.get()
        for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Neighbor squares
            node_position = (current[0] + i[0], current[1] + i[1])
            # Checks range
            if node_position[0] > (len(window.grid) - 1) or node_position[0] < 0 or node_position[1] > (len(window.grid[len(window.grid) - 1]) - 1) or node_position[1] < 0:
                continue
            # Checks if it is a wall
            if window.grid[node_position[0]][node_position[1]] != 0:
                continue
            if node_position not in path:
                q.put(node_position)
                path[node_position] = current
                window.draw_cube(node_position[0], node_position[1], "magenta")
                window.refresh()
            if current == window.end:
                result = []
                while current != window.start: 
                    result.append(current)
                    current = path[current]
                result.append(window.start)
                result.reverse()
                return result

def main():
    screen = Tk()
    screen.geometry("1010x565")
    gui = window(screen, 1000, 500)
    gui.create_window()
main()
