# Kyle Arrowood
# 7/18/2020
# A pathfinding algorithm visualizer

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
                                "Breadth First Search", "Depth First Search")
        # Start and end points for path
        self.start = (2, 2)
        self.end = (48, 28)
        self.rows = 50
        self.columns = 100
        option_menu.config(bg = "yellow")
        def button_callback():
            go_button["state"] = DISABLED
            option_menu["state"] = DISABLED
            if option_variable.get() == "A* Search":
                pass
            elif option_variable.get() == "Dijkstra's Algorithm":
                pass
            elif option_variable.get() == "Greedy Best First Search":
                path = greedy(self)
                for i, node in enumerate(path):
                    self.draw_cube(node[0], node[1], "lime")
            elif option_variable.get() == "Breadth First Search":
                path = bfs(self)
                for i, node in enumerate(path):
                    self.draw_cube(node[0], node[1], "lime")
            elif option_variable.get() == "Depth First Search":
                pass
            self.refresh()
            go_button["state"] = "normal"
            option_menu["state"] = "normal"
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

def a_star(window, start, end):
    pass
def dijkstra(window, start, end):
    pass
class greedy_node:
    # Node used for greedy search
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position
def greedy(window):
    # Returns list of coords of the path
    start_node = greedy_node(None, window.start)
    end_node = greedy_node(None, window.end)
    open_list = []
    closed_list = []
    open_list.append(start_node)
    while len(open_list) > 0:
        # Grabs next current
        current = open_list[0]
        index = 0
        for i, node in enumerate(open_list):
            if node.f < current.f and node.f != 0:
                current = node
                index = i
        # Puts in closed list
        open_list.pop(index)
        closed_list.append(current)
        # When path is done
        if current == end_node:
            path = []
            cur = current
            while cur is not None:
                path.append(cur.position)
                cur = cur.parent
            return path[::-1] # Reversed path

        for i in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
            node_position = (current.position[0] + i[0], current.position[1] + i[1])
            # Checks range
            if node_position[0] > (len(window.grid) - 1) or node_position[0] < 0 or node_position[1] > (len(window.grid[len(window.grid) - 1]) - 1) or node_position[1] < 0:
                continue
            # Checks if it is a wall
            if window.grid[node_position[0]][node_position[1]] != 0:
                continue
            child = greedy_node(current, node_position)
            if i == (-1, -1) or i == (-1, 1) or i == (1, -1) or i == (1, 1):
                child.g = child.g + 0.414
            # Child already on closed list
            for closed in closed_list:
                if child == closed:
                    break
            else:
                # f, g, and h values
                child.g = current.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h
            # Child already on open list
            for open_node in open_list:
                if child == open_node and child.g >= open_node.g:
                    break
            else:
                open_list.append(child)
                window.draw_cube(child.position[0], child.position[1], "magenta")
                window.refresh()
def bfs(window):
    q = Queue()
    q.put(window.start)
    path = dict()
    path[window.start] = None
    while not q.empty():
        current = q.get()
        for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
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
def dfs(window):
    pass
            
        






def main():
    screen = Tk()
    screen.geometry("1010x565")
    gui = window(screen, 1000, 500)
    gui.create_window()
main()
