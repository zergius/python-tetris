# tetris.py
import tkinter
import math
import random

cellsize = 20
cells_h = 20
cells_w = 10
fieldwidth = cellsize * cells_w
fieldheight = cellsize * cells_h
width = fieldwidth + 105
height = fieldheight + 5
offset = 2
color = "#fff", "#eee", "#ccc"

elements = [
    [
        [1, 1],
        [1, 1]
    ],
    [
        [1, 1, 0],
        [0, 1, 1]
    ],
    [
        [0, 1, 1],
        [1, 1, 0]
    ],
    [
        [0, 1, 0],
        [1, 1, 1]
    ],
    [
        [1, 1, 1, 1]
    ],
    [
        [1, 0, 0],
        [1, 1, 1]
    ],
    [
        [0, 0, 1],
        [1, 1, 1]
    ]
]
rotation = [0, 90, 180, 270]

class Game_state:
    def __init__(self):
        self.game_started = False
        self.game_paused = False
        self.game_speed = .4
        self.game_speed_p = 0
        self.game_score = 0
        self.game_level = 0
        self.cur_figure = 0
        self.next_figure = 0
    
    def get_state(self, state):
        if state == 'started':
            return self.game_started
        else:
            return self.game_paused
    
    def get_speed(self):
        return self.game_speed

    def get_score(self):
        return self.game_score

    def add_score(self, lines):
        if lines == 1:
            self.game_score += 100
        elif lines == 2:
            self.game_score += 300
        elif lines == 3:
            self.game_score += 500
        else:
            self.game_score += 700
            
        if math.floor(self.game_score / 1000) > self.game_level:
            self.game_speed += .2
            self.game_level += 1
        # print(self.game_speed, self.game_level)

    def toggle_state(self, state):
        global the_figure, elements
        if state == 'started':
            if self.game_started == False:
                self.game_score = 0
                self.game_started = True
                self.cur_figure = self.prepare_figure(random.randint(0, len(elements) - 1))
                self.next_figure = self.prepare_figure(random.randint(0, len(elements) - 1))
                the_figure = self.create_figure()
            else:
                self.game_started = False
        else:
            if self.game_paused == False:
                self.game_paused = True
                self.game_speed_p = self.game_speed
                self.game_speed = 0
            else:
                self.game_paused = False
                self.game_speed = self.game_speed_p
                self.game_speed_p = 0

    def stop_game(self):
        self.game_speed = .4
        self.game_speed_p = 0
        self.game_started = False
        self.game_paused = False
        the_figure = None
        matrix.clear()
    
    def game_active(self):
        if self.game_started == True and self.game_paused == False:
            return True
        else:
            return False
    
    def prepare_figure(self, figure_index):
        global rotation
        figure = elements[figure_index]
        figure_height = len(figure)
        figure_length = len(figure[0])
        init_rotation = random.choice(rotation)
        while init_rotation > 0:
            rotated = []
            i = figure_length - 1
            while i >= 0:
                nrow = []
                j = 0
                while j < figure_height:
                    nrow.append(figure[j][i])
                    j += 1
                rotated.append(nrow)
                i -= 1
            figure = rotated
            figure_height = len(figure)
            figure_length = len(figure[0])
            init_rotation -= 90
        return figure
    
    def create_figure(self):
        global elements, cells_w
        figure = self.cur_figure
        figure_height = len(figure)
        figure_length = len(figure[0])
        the_figure = Figure(figure, [math.floor((cells_w - figure_length) / 2), -1 * figure_height])
        return the_figure

    def station_figure(self):
        global the_figure, matrix, elements
        # print('station figure ',  the_figure.get_position())
        if the_figure.get_position()[1] < 0:
            print('game over')
            game_state.stop_game()
        else:
            matrix.add(the_figure)
            self.cur_figure = self.next_figure
            self.next_figure = self.prepare_figure(random.randint(0, len(elements) - 1))
            the_figure = self.create_figure()
    
    def get_next_figure(self):
        return self.next_figure


class Matrix:
    def __init__(self, cells_h, cells_w):
        self.matrix = []
        i = 0
        while i < cells_h:
            row = []
            j= 0
            while j < cells_w:
                row.append(0)
                j += 1
            self.matrix.append(row)
            i += 1
    
    def add(self, figure):
        shape = figure.get_figure()
        position = figure.get_position()
        row = 0
        for r in shape:
            col = 0
            for c in r:
                if c == 1:
                    self.matrix[position[1] + row][position[0] + col] = 1
                col += 1
            row += 1
        # print(self.matrix)
        pass
    
    def draw(self, canvas):
        global color
        row = 0
        for r in self.matrix:
            col = 0
            for c in r:
                if c == 1:
                    # self.matrix[position[1] + row][position[0] + col] = 1
                    canvas.create_rectangle(
                        col * cellsize + offset, 
                        row * cellsize + offset, 
                        (col + 1) * cellsize + 1, 
                        (row + 1) * cellsize + 1, 
                        fill=color[2], 
                        outline=color[1]
                    )
                col += 1
            row += 1
        pass
        
    def is_occupied(self, row, col):
        if row >= 0 and col >= 0:
            return self.matrix[row][col]
        else:
            return 0
    
    def check_full_line(self):
        full_lines = 0
        full_lines_no = []
        row_no = 0
        for r in self.matrix:
            if r.count(1) == cells_w:
                full_lines += 1
                full_lines_no.append(row_no)
            row_no += 1
        if len(full_lines_no) > 0:
            print(full_lines)
            for row_no in full_lines_no:
                del self.matrix[row_no]
                new_row = []
                j = 0
                while j < cells_w:
                    new_row.append(0)
                    j += 1
                self.matrix.insert(0, new_row)
        return full_lines
        
    def clear(self):
        # print('clear matrix')
        row = 0
        for r in self.matrix:
            col = 0
            for c in r:
                self.matrix[row][col] = 0
                col += 1
            row += 1
        pass


class Figure:
    def __init__(self, figure, pos):
        self.figure = figure
        self.pos = [pos[0], pos[1]]
        self.cubes = []
        self.counter = 0
    
    def draw(self, canvas):
        global cellsize, color, offset, game_state
        row = 0
        for r in self.figure:
            col = 0
            for c in r:
                if c == 1:
                    self.cubes.append(canvas.create_rectangle(
                        (self.pos[0] + col) * cellsize + offset, 
                        (self.pos[1] + row) * cellsize + offset, 
                        (self.pos[0] + col + 1) * cellsize + 1, 
                        (self.pos[1] + row + 1) * cellsize + 1, 
                        fill=color[2], 
                        outline=color[1]
                    ))
                col += 1
            row += 1
        self.counter += game_state.get_speed()
        if self.counter > cellsize:
            col = self.collision('D')
            if col == False:
                self.pos[1] += 1
            else:
                game_state.station_figure()
            self.counter = 0
    
    def get_position(self):
        return self.pos
    
    def get_figure(self):
        return self.figure
    
    def collision(self, dir):
        global cells_h, cells_w
        collide = False
        row = 0
        for r in self.figure:
            col = 0
            for c in r:
                if c == 1:
                    if collide == False:
                        if dir == 'D':
                            if self.pos[1] + row >= cells_h - 1:
                                collide = True
                            elif matrix.is_occupied(self.pos[1] + row + 1, self.pos[0] + col) == 1:
                                collide = True
                        if dir == 'L':
                            if self.pos[0] + col - 1 < 0:
                                collide = True
                            elif matrix.is_occupied(self.pos[1] + row, self.pos[0] + col - 1) == 1:
                                collide = True
                        if dir == 'R':
                            if self.pos[0] + col + 1 >= cells_w:
                                collide = True
                            elif matrix.is_occupied(self.pos[1] + row, self.pos[0] + col + 1) == 1:
                                collide = True
                        if dir == 'C':
                            if matrix.is_occupied(self.pos[1] + row, self.pos[0] + col) == 1:
                                collide = True
                col += 1
            row +=1
        return collide
    
    def move(self, direction, state = False):
        if state == True:
            if direction == 'Left':
                col = self.collision('L')
                if col == False:
                    self.pos[0] -= 1
            if direction == 'Right':
                col = self.collision('R')
                if col == False:
                    self.pos[0] += 1
            if direction == 'Down':
                col = self.collision('D')
                if col == False:
                    self.pos[1] += 1
        pass
        
    def rotate(self, direction, state = False):
        if state == True:
            rotate_border_collision = False
            cols = len(self.figure)
            rows = len(self.figure[0])
            rotated = []
            # print(rows, cols, self.pos)
            if self.pos[0] + cols > cells_w:
                rotate_border_collision = True
            i = rows - 1
            while i >= 0:
                nrow = []
                j = 0
                while j < cols:
                    nrow.append(self.figure[j][i])
                    j += 1
                rotated.append(nrow)
                i -= 1
            # check if rotated figure collides with existed blocks
            old_pos = self.pos
            old_figure = self.figure
            if rotate_border_collision:
                self.pos[0] -= 1
            self.figure = rotated
            rotate_collision = self.collision('C')
            if rotate_collision:
                self.pos = old_pos
                self.figure = old_figure
            # print('rotate collision', rotate_collision)
        pass

class Dashboard:
    def __init__(self):
        self.score = 0
        self.state = ''

    def draw(self, canvas):
        pre_pos = [210, 99]
        pre_size = 80
        if not game_state.get_state('started'):
            self.state = 'Press "Space" to start.'
        else:
            if game_state.get_state('paused'):
                self.state = 'Game paused. Press "Space" to resume.'
            else:
                self.state = ''
        canvas.create_text(pre_pos[0], 10, text = self.state, anchor = 'nw', width = 100)
        canvas.create_text(pre_pos[0], 50, text = 'Score:', anchor = 'nw', width = 100)
        canvas.create_text(pre_pos[0], 62, text = game_state.get_score(), anchor = 'nw', width = 100, font = ('Helvetica', '16'))
        canvas.create_rectangle(pre_pos[0] + offset, pre_pos[1] + offset, pre_pos[0] + pre_size + offset, pre_pos[1] + pre_size + offset, fill=color[0], outline=color[1])

        i = 0
        while i < pre_size:
            i += cellsize
            canvas.create_line(pre_pos[0] + i - cellsize+offset, pre_pos[1] + offset, pre_pos[0] + i - cellsize + offset, pre_pos[1] + pre_size + offset, fill=color[1])
            if i < pre_size:
                canvas.create_line(pre_pos[0] + i - 1 + offset, pre_pos[1] + offset, pre_pos[0] + i - 1 + offset, pre_pos[1] + pre_size + offset, fill=color[1])
        i = 0
        while i < pre_size:
            i += cellsize
            canvas.create_line(pre_pos[0] + offset, pre_pos[1] + i - cellsize + offset, pre_pos[0] + pre_size + offset, pre_pos[1] + i - cellsize + offset, fill=color[1])
            if i < pre_size:
                canvas.create_line(pre_pos[0] + offset, pre_pos[1] + i - 1 + offset, pre_pos[0] + pre_size + offset, pre_pos[1] + i - 1 + offset, fill=color[1])
        if game_state.get_state('started'):
            next_figure = game_state.get_next_figure()
            figure_height = len(next_figure)
            figure_length = len(next_figure[0])
            offset_v = 0
            offset_h = 0
            if figure_height < 4:
                offset_v = cellsize
            if figure_length < 4:
                offset_h = cellsize
            row = 0
            for r in next_figure:
                col = 0
                for c in r:
                    if c == 1:
                        canvas.create_rectangle(
                            col * cellsize + offset + pre_pos[0] + offset_h, 
                            row * cellsize + offset + pre_pos[1] + offset_v, 
                            (col + 1) * cellsize + 1 + pre_pos[0] + offset_h, 
                            (row + 1) * cellsize + 1 + pre_pos[1] + offset_v, 
                            fill=color[2], 
                            outline=color[1]
                        )
                    col += 1
                row += 1
        pass


def draw():
    global fieldwidth, fieldheight, cellsize, color, offset, game_state
    canvas.delete('all')
    canvas.create_rectangle(0+offset, 0+offset, fieldwidth+offset, fieldheight+offset, fill=color[0], outline=color[1])
    i = 0
    while i < fieldwidth:
        i += cellsize
        canvas.create_line(i-cellsize+offset, 0+offset, i-cellsize+offset, fieldheight+offset, fill=color[1])
        if i < fieldwidth:
            canvas.create_line(i-1+offset, 0+offset, i-1+offset, fieldheight+offset, fill=color[1])
    i = 0
    while i < fieldheight:
        i += cellsize
        canvas.create_line(0+offset, i-cellsize+offset, fieldwidth+offset, i-cellsize+offset, fill=color[1])
        if i < fieldheight:
            canvas.create_line(0+offset, i-1+offset, fieldwidth+offset, i-1+offset, fill=color[1])
    dashboard.draw(canvas)
    if game_state.get_state('started') == True:
        the_figure.draw(canvas)
        lines = matrix.check_full_line()
        if lines > 0:
            game_state.add_score(lines)
        matrix.draw(canvas)
    root.after(20, draw)


def keyup(key):
    for i in inputs:
        if key.keysym == i:
            inputs[i](i)
    pass

def keydown(key):
    for i in inputs:
       if key.keysym == i:
           inputs[i](i, True)
    pass
    
def move_figure(direction, state = False):
    global the_figure
    if game_state.game_active():
        if state == True:
            if direction == 'Left':
                the_figure.move('Left', True)
            if direction == 'Right':
                the_figure.move('Right', True)
            if direction == 'Up':
                the_figure.rotate('Up', True)
            if direction == 'Down':
                the_figure.move('Down', True)
    pass
    
def toggle_mode(key, state = False):
    global game_state
    if state == True:
        if game_state.get_state('started') == False:
            game_state.toggle_state('started')
        else:
            game_state.toggle_state('paused')
    pass

game_state = Game_state()
dashboard = Dashboard()
matrix = Matrix(cells_h, cells_w)


root = tkinter.Tk()
frame = tkinter.Frame(root)
root.wm_title('Tetris')
frame.pack()
canvas = tkinter.Canvas(root, width = width, height = height)
canvas.pack()

inputs = {'Left': move_figure, 'Right': move_figure, 'Up': move_figure, 'Down': move_figure, 'space':toggle_mode}

root.bind("<Key>", keydown)
root.bind("<KeyRelease>", keyup)

draw()

tkinter.mainloop()
