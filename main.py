import pygame
from queue import PriorityQueue
from random import randint

pygame.init()
# colors
DARK_RED = (129, 31, 31)
RED = (130, 20, 20, 100)
DARK_GREEN = (10, 100, 10)
GREEN = (30, 215, 96, 250)
GREY = (215, 215, 215, 20)
DARK_GREY = (123, 85, 85)
BLACK = (25, 20, 20)
WHITE = (250, 250, 250)
BLUE = (51, 153, 255)
YELLOW = (250, 250, 153)
PURPLE = (128, 0, 128)
ORANGE = (255, 128, 0)
BRIGHT_GREEN = (102, 250, 250)

# text
# pygame.font.init()


# CONSTANTS
bar_HEIGHT = 40
WIDTH = 700  # also height - square GUI

pause_width, pause_height = 200, 400

BAR_X, BAR_Y = 1 + WIDTH // 3, 0

BAR_WIDTH = WIDTH - 2 * WIDTH // 3 - 1

button_width = 80
button_height = 37
ROWS = 35
COLS = 50
clock = pygame.time.Clock()

button_1_x = BAR_WIDTH // 10
button_1_y = BAR_Y + 2
button_2_x = BAR_WIDTH - BAR_WIDTH // 10 - button_width
button_2_y = BAR_Y + 2

# Skeleton
WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("Path-Finding Algorithm Visualizer")
BAR = pygame.Surface((BAR_WIDTH, bar_HEIGHT))

# LOGIC
ALGORITHM = 1
Start_Algorithm = pygame.event.Event(pygame.USEREVENT, {"greeted": False, "jumped": 10, "ID": 1})


class Button:
    def __init__(self, surface, color, x, y, width, height, text='', text_size=20, text_color=BLACK):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.surface = surface

    # menu_button_1 = pygame.Rect(pause_width // 2 - 25, 30, menu_button_width, menu_button_height)
    # menu_button_2 = pygame.Rect(pause_width // 2 - 25, 130, menu_button_width, menu_button_height)

    def drawButton(self):  # , outline=None):
        # Call this method to draw the button on the screen
        # if outline:
        #    pygame.draw.rect(self.surface, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))

        if self.text != '':
            font = pygame.font.SysFont('arial', self.text_size)

            text = font.render(self.text, True, self.text_color)
            self.surface.blit(text, (
                self.x + (self.width // 2 - text.get_width() // 2),
                self.y + (self.height // 2 - text.get_height() // 2)))

    def isOver(self, pos, color=GREEN):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                self.color = color
                return True
        self.color = GREY
        return False


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width  # height
        self.color = BLACK
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.t = 0.1
        self.grad = 0.1
        self.forred = 0
        self.redgrad = 0
        self.was_weight = 0
        self.distance = 1  # for weighted path its more

        # counter = times to animate from <value> to 1
        self.counter = 0

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):

        return self.color == GREY

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = BLACK
        self.distance = 1
        self.was_weight = 0

    def set_closed(self):
        self.forred = 1.2
        self.t = 0.7
        self.redgrad = 0.025
        self.grad = 0.005
        self.counter = 1
        self.color = RED

    def set_open(self):
        self.t = 0.6
        self.grad = 0.04
        self.counter = 1
        if self.was_weight:
            self.color = DARK_GREEN
        else:
            self.color = GREEN

    def set_barrier(self):
        self.color = GREY
        self.grad = 0.04
        self.t = 0
        self.counter = 1
        self.distance = 1
        self.was_weight = 0

    def set_weight(self):
        self.color = DARK_GREY
        self.grad = 0.04
        self.t = 0
        self.counter = 1
        self.distance = 4
        self.was_weight = 1

    def set_end(self):
        self.grad = 0.08
        self.t = 0
        self.color = BRIGHT_GREEN
        self.counter = 1

    def set_start(self):
        self.grad = 0.08
        self.t = 0
        self.color = BLUE
        self.counter = 1
        self.distance = 1

    def set_path(self):
        self.color = ORANGE
        self.t = 0
        self.grad = 0.4
        self.counter = 1
        self.distance = 1

    def animated_draw(self, win):
        if self.color == RED:
            # if self.t <= 1:
            self.t = min(1, self.t)
            pygame.draw.rect(win, (max(80, self.color[0] * self.forred), max(20, self.color[1] * self.forred),
                                   max(20, self.color[2] * self.forred)), (
                                 self.x + self.width // 2 - self.t * self.width // 2,
                                 self.y + self.width // 2 - self.t * self.width // 2,
                                 self.width * self.t, self.width * self.t))
            self.t += self.grad
            self.forred -= self.redgrad

        # else:
        # self.draw(win)

        else:
            if self.t <= 1 and self.counter > 0:
                self.t = min(1, self.t)
                pygame.draw.rect(win, (self.color[0] * self.t, self.color[1] * self.t, self.color[2] * self.t), (
                    self.x + self.width // 2 - self.t * self.width // 2,
                    self.y + self.width // 2 - self.t * self.width // 2,
                    self.width * self.t, self.width * self.t))
                self.t += self.grad

                if self.t >= 1:
                    self.counter -= self.t // 1
                    self.t = 0.5
            else:
                self.draw(win)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid, diagonal_permitted=0):

        self.neighbors = []
        if diagonal_permitted:
            col_right = self.col + 1 < self.total_rows
            col_left = self.col - 1 > 0
            row_down = self.row + 1 < self.total_rows
            row_up = self.row - 1 > 0

            upper_right = col_right and row_up
            down_right = col_right and row_down
            upper_left = col_left and row_up
            down_left = col_left and row_down
            if upper_left and not grid[self.row - 1][self.col - 1].is_barrier():
                self.neighbors.append(grid[self.row - 1][self.col - 1])
            if upper_right and not grid[self.row - 1][self.col + 1].is_barrier():
                self.neighbors.append(grid[self.row - 1][self.col + 1])
            if down_left and not grid[self.row + 1][self.col - 1].is_barrier():
                self.neighbors.append(grid[self.row + 1][self.col - 1])
            if down_right and not grid[self.row + 1][self.col + 1].is_barrier():
                self.neighbors.append(grid[self.row + 1][self.col + 1])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # down
            self.neighbors.append(grid[self.row + 1][self.col])
        # right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    # less than- compare two spots
    def __lt__(self, other):
        return False


# point = (x,y)
# distance between 2 points
def h(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return abs(x1 - x2) + abs(y1 - y2)


# create the grid with objects
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


# draw the grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, (169, 169, 169), (i * gap, 0), (i * gap, width))
    for j in range(rows):
        pygame.draw.line(win, (169, 169, 169), (0, j * gap), (width, j * gap))
    WIN.blit(BAR, (BAR_X, BAR_Y))


# draw everything
def draw(win, grid, rows, width, buttons=None):
    if buttons is None:
        buttons = {}
    win.fill(BLACK)
    for row in grid:
        for spot in row:
            if spot.color != BLACK:
                spot.animated_draw(win)
            elif spot.color != BLACK:
                spot.draw(win)

    draw_grid(win, rows, width)
    for key in buttons.keys():
        buttons[key].drawButton()
    pygame.display.update()


def clear_closed_opens(grid):
    for row in grid:
        for Cube in row:
            if (Cube.is_open() or Cube.is_closed() or Cube.color == ORANGE) and Cube.was_weight == 0:
                Cube.reset()
            elif Cube.was_weight == 1:
                Cube.set_weight()


# get mouse coordinate
# get grid coordinates from mouse pos

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x_pos = pos[0] // gap
    y_pos = pos[1] // gap
    return x_pos, y_pos


def button1_clicked():
    global ALGORITHM
  
    ALGORITHM = 1


def button2_clicked():
    global ALGORITHM

    ALGORITHM = 2


def button3_clicked(grid, buttons, end, start):
    generate_maze(grid, lambda: draw(WIN, grid, ROWS, WIDTH, buttons=buttons), end, start)


# clear
def Clear(grid, end, start):
    for row in grid:
        for elem in row:
            elem.reset()

    start: Spot = grid[start[0]][start[1]]
    end: Spot = grid[end[0]][end[1]]
    start.set_start()
    end.set_end()

    for i in range(11, 24):
        for j in range(0, 3):
            grid[i][j].set_barrier()


def menu(menu_width, menu_height, buttons=None, grid=None, endloc=(25, 25), startloc=(5, 5)):
    if buttons is None:
        buttons = {}
    if grid is None:
        grid = [[]]
    pause_screen = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
    menu_button_width = 100
    menu_button_height = 50

    menu_button_1 = pygame.Rect(menu_width // 2 - 25, 30, menu_button_width, menu_button_height)
    menu_button_2 = pygame.Rect(menu_width // 2 - 25, 130, menu_button_width, menu_button_height)
    menu_button_3 = pygame.Rect(menu_width // 2 - 39, 231, menu_button_width + 20, menu_button_height)
    menu_button_4 = pygame.Rect(menu_width // 2 - 39, 332, menu_button_width + 20, menu_button_height)

    Button1 = Button(pause_screen, GREY, menu_button_1.x, menu_button_1.y, menu_button_1.width, menu_button_1.height,
                     "A*")
    Button2 = Button(pause_screen, GREY, menu_button_2.x, menu_button_2.y, menu_button_2.width, menu_button_2.height,
                     "Dijkstra")
    Button3 = Button(pause_screen, GREY, menu_button_3.x, menu_button_3.y, menu_button_3.width, menu_button_3.height,
                     "Generate Maze")
    Button4 = Button(pause_screen, GREY, menu_button_4.x, menu_button_4.y, menu_button_4.width, menu_button_4.height,
                     "Clear")

    pause_screen.fill((50, 50, 50, 0))

    # animate entry
    # t = pause_width
    # while t >= 0:
    #    WIN.blit(pause_screen, (WIDTH - pause_width + t, 0))
    #    pygame.display.update()
    #    t -= 1

    running = True
    while running:
        clock.tick(60)
        m_x, m_y = pygame.mouse.get_pos()
        m_x -= WIDTH - menu_width
        pos = (m_x, m_y)
        onButton1 = Button1.isOver(pos)
        onButton2 = Button2.isOver(pos)
        onButton3 = Button3.isOver(pos)
        onButton4 = Button4.isOver(pos)
        if onButton1:
            Button1.color = BLUE
            Button2.color = GREY
            Button3.color = GREY
            Button4.color = GREY

        elif onButton2:
            Button1.color = GREY
            Button2.color = BLUE
            Button3.color = GREY
            Button4.color = GREY
        elif onButton3:
            Button1.color = GREY
            Button2.color = GREY
            Button3.color = BLUE
            Button4.color = GREY
        elif onButton4:
            Button1.color = GREY
            Button2.color = GREY
            Button3.color = GREY
            Button4.color = BLUE

        else:
            Button1.color = GREY
            Button2.color = GREY
            Button3.color = GREY
            Button4.color = GREY

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return
            if pygame.mouse.get_pressed(3)[0]:
                if m_x < 0:
                    running = False
                    break

                if onButton1:
                    button1_clicked()
                    pygame.event.clear()
                    return

                elif onButton2:
                    button2_clicked()
                    pygame.event.clear()
                    return

                elif onButton3:
                    button3_clicked(grid, buttons, endloc, startloc)
                    pygame.event.clear()
                    return

                elif onButton4:
                    Clear(grid, endloc, startloc)
                    pygame.event.clear()
                    return

        Button1.drawButton()
        Button2.drawButton()
        Button3.drawButton()
        Button4.drawButton()
        WIN.blit(pause_screen, (WIDTH - menu_width, 0))

        pygame.display.update()


# random maze
def generate_maze(grid, draw2, endp, startp):
    x = False

    while not x:

        for row in grid:
            for elem in row:
                elem.reset()

        start: Spot = grid[startp[0]][startp[1]]
        end: Spot = grid[endp[0]][endp[1]]
        start.set_start()
        end.set_end()
        for i in range(11, 24):
            for j in range(0, 3):
                grid[i][j].set_barrier()
        for elem in grid[0]:
            elem.set_barrier()
        for elem in grid[ROWS - 1]:
            elem.set_barrier()
        for i in range(ROWS):
            grid[i][ROWS - 1].set_barrier()
        row = 0

        leng = len(grid[0])
        while row < leng - 2:

            col = 0
            while col < leng - 2:

                elem = grid[row][col]
                if elem.is_start() or elem.is_end():
                    continue
                x1 = randint(0, 10000)

                if x1 < 5000:
                    x = randint(0, 3)
                    grid[row][col].set_barrier()
                    grid[row - 1][col].set_barrier()
                    grid[row + 1][col].set_barrier()
                if x == 0:
                    grid[row - 2][col].set_barrier()
                    grid[row + 2][col].set_barrier()

                elif x1 > 8200:
                    x = randint(0, 1)
                    grid[row][col].set_barrier()
                    grid[row][col + 1].set_barrier()
                    grid[row][col - 1].set_barrier()
                    if x == 0:
                        grid[row][col + 2].set_barrier()
                        grid[row][col - 2].set_barrier()

                col += 2
            row += 2

        for row in grid:
            for spot in row:
                spot.update_neighbors(grid)

        x = maze_checker(grid, start, end)
        draw2()


# def r_d_helper(mask, draw2, end, start, counter, row_start, row_end, col_start, col_end):
#    pass
#
# def recursive_division_maze(grid, draw2, end, start):
#    Clear(grid, end, start)
#    mask = np.zeros_like(grid)
#    shape = np.shape(mask)
#    r_d_helper(mask, draw2, end, start, 0, 0, shape[0], 0, shape[1])
#
#    for i in range(shape[0]): #all rows
#        for j in range(shape[1]):
#            if mask[i, j] == 1:
#                grid[i][j].set_barrier()
#                draw2()
#
#
# searching algorithms***
def reconstruct_path(came_from, current, draw_func):
    while current in came_from:
        clock.tick(40)
        current = came_from[current]
        current.set_path()
        draw_func()


def maze_checker(grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {spot: float("inf") for row in grid for spot in row}  # for every spot a value of infinity
    g_score[start] = 0  # gscore of start node is 0
    # start is at start
    f_score = {spot: float("inf") for row in grid for spot in row}  # for every spot a value of infinity
    # start is H distance from end
    f_score[start] = h(start.get_pos(), end.get_pos())  # gscore of start node is 0

    # how to check if something is in priority queue ? - dict
    open_set_hash = {start}

    while not open_set.empty():

        current = open_set.get()[2]  # popping lower fscore from open_set - priority queue1
        open_set_hash.remove(current)

        if current == end:
            return True

        for neighbor in current.neighbors:

            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                # if neighbor not inside open set
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

    # path not found
    return False


def algorithm_a_star(draw_func, grid, start, end, buttons=None):
    if buttons is None:
        buttons = {}
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {}
    f_score = {}
    for row in grid:
        for spot in row:
            g_score[spot] = float("inf")  # for every spot a value of infinity
            f_score[spot] = float("inf")  # for every spot a value of infinity

    g_score[start] = 0  # gscore of start node is 0
    # start is at start
    # start is H distance from end
    f_score[start] = h(start.get_pos(), end.get_pos())  # gscore of start node is 0

    # how to check if something is in priority queue ? - dict
    open_set_hash = {start}

    while not open_set.empty():
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        on_Start = buttons["Start"].isOver(mouse_pos, RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    clear_closed_opens(grid)

                    return False

            if pygame.mouse.get_pressed(3)[0]:
                if on_Start:
                    clear_closed_opens(grid)
                    pygame.event.clear()
                    return False

        current = open_set.get()[2]  # popping lower fscore from open_set - priority queue1
        open_set_hash.remove(current)

        if current == end:
            for key in open_set_hash:
                key.grad = 0.5

            reconstruct_path(came_from, end, draw_func)
            end.set_end()
            start.set_start()
            return True

        for neighbor in current.neighbors:
            neighbor: Spot
            temp_g_score = g_score[current] + neighbor.distance

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                # if neighbor not inside open set
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_open()
                    draw_func()

        if current != start:
            current.set_closed()
            draw_func()
    # path not found
    return False


def dijkstra_algorithm(draw_func, grid, start, end, buttons=None):
    # set up dist with inf in everything and <start> with 0
    if buttons is None:
        buttons = {}
    dist = {elem: float("inf") for row in grid for elem in row}
    dist[start] = 0
    count = 0
    # set up prev as undefined for every element
    prev = {}
    # create set Q and insert start to PQ
    PQ = PriorityQueue()
    # to check if something is in it
    PQ.put((0, count, start))
    PQ_hash = {start}

    # insert every elem except start into PQ with inf
    for row in grid:
        for elem in row:
            if elem != start:
                PQ.put((dist[elem], float('inf'), elem))
                PQ_hash.add(elem)

    # iterate until PQ is empty
    while not PQ.empty():
        clock.tick(60)
        # event handling
        mouse_pos = pygame.mouse.get_pos()
        on_Start = buttons["Start"].isOver(mouse_pos, RED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    clear_closed_opens(grid)

                    return False

            if pygame.mouse.get_pressed(3)[0]:
                if on_Start:
                    clear_closed_opens(grid)
                    pygame.event.clear()
                    return False

        current = PQ.get()[2]  # get element with min distance

        # if what's left is inf - no path to end
        if dist[current] == float('inf'):
            return False

        PQ_hash.remove(current)  # remove element from Hash table

        current.set_closed()
        draw_func()

        # been_there.add(current)

        if current == end:
            for key in PQ_hash:
                if key is not None:
                    key.grad = 0.5
            reconstruct_path(prev, current, draw_func)
            end.set_end()
            start.set_start()
            return True

        for neighbor in current.neighbors:
            # if neighbor inside PQ
            if neighbor in PQ_hash:  # and neighbor not in been_there:
                # alt = dist[current] + h(neighbor.get_pos(), current.get_pos())
                alt = dist[current] + (neighbor.distance - 1) + h(neighbor.get_pos(), current.get_pos())
                if alt < dist[neighbor]:
                    count += 1
                    dist[neighbor] = alt
                    prev[neighbor] = current
                    PQ.put((dist[neighbor], count, neighbor))
                    neighbor.set_open()
                    draw_func()
    return False


def tut(win):
    font = pygame.font.SysFont('arial', 40)

    tut_text = 'Hello, click on the mouse to skip the tutorial :)'
    text1 = 'Use the mouse to draw barriers, '
    text2 = 'LEFT Click - barrier | Middle- Weighted path'
    text3 = 'RIGHT Click - remove barrier'
    text4 = 'Press M or the button above to open the menu'
    text5 = 'Press SPACE or the START button to'
    text5_more = 'visualize the chosen algorithm.'
    text6 = 'Press C to clear the board'
    text7 = 'And press D to generate a maze, Enjoy :) '

    tut_obj = font.render(tut_text, True, WHITE)
    textobj1 = font.render(text1, True, BLUE)
    textobj2 = font.render(text2, True, BLUE)
    textobj3 = font.render(text3, True, BLUE)
    textobj4 = font.render(text4, True, BLUE)
    textobj5 = font.render(text5, True, BLUE)
    textobj5_more = font.render(text5_more, True, BLUE)
    textobj6 = font.render(text6, True, BLUE)
    textobj7 = font.render(text7, True, BLUE)
    texts = [tut_obj, textobj1, textobj2, textobj3, textobj4, textobj5, textobj5_more, textobj6, textobj7]

    for i in range(len(texts)):
        win.blit(texts[i], (20, 20 + i * 60))
    pygame.display.update()
    Skip_keys = [pygame.K_KP_ENTER, pygame.K_ESCAPE, pygame.KSCAN_KP_ENTER]

    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key in Skip_keys:
                    waiting = False
            elif pygame.mouse.get_pressed(3)[0]:
                waiting = False

    # pygame.time.delay(10000)


def main(win, width):
    global ALGORITHM
    grid = make_grid(ROWS, width)
    draw(WIN, grid, ROWS, WIDTH)
    # set default starting and ending positions
    button1_location_x = button_1_x + BAR_X
    button2_location_x = button_2_x + BAR_X

    buttons = {}
    Start_Button = Button(WIN, GREY, button1_location_x, button_1_y, button_width, button_height, "Start")
    Menu_Button = Button(WIN, GREY, button2_location_x, button_2_y, button_width, button_height, "Menu")

    buttons["Menu"] = Menu_Button
    buttons["Start"] = Start_Button

    # set default start-end positions

    start: Spot = grid[5][5]
    end: Spot = grid[ROWS - 5][ROWS - 5]
    start.set_start()
    end.set_end()
    for i in range(11, 24):
        for j in range(0, 3):
            grid[i][j].set_barrier()

    run = True
    started = False

    while run:
        clock.tick(100)
        draw(WIN, grid, ROWS, WIDTH, buttons=buttons)
        mouse_pos = pygame.mouse.get_pos()

        on_Start_Button = Start_Button.isOver(mouse_pos)
        on_Menu_Button = Menu_Button.isOver(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue
            if pygame.mouse.get_pressed(3)[0]:  # left mouse

                row, col = get_clicked_pos(mouse_pos, ROWS, width)
                spot: Spot = grid[row][col]

                if on_Start_Button and event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.event.post(Start_Algorithm)
                    continue

                elif on_Menu_Button:
                    menu(pause_width, pause_height, buttons=buttons, grid=grid, startloc=start.get_pos(),
                         endloc=end.get_pos())

                elif not start and spot != end:
                    start = spot
                    start.set_start()

                elif not end and spot != start:
                    end = spot
                    spot.set_end()

                elif spot != end and spot != start:
                    spot.set_barrier()

            elif pygame.mouse.get_pressed(3)[2]:  # right mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            elif pygame.mouse.get_pressed(3)[1]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cube = grid[row][col]
                if cube != start and cube != end:
                    cube.set_weight()
            if event.type == pygame.USEREVENT and not started:
                if event.ID == 1:
                    if start is None:
                        start: Spot = grid[5][5]
                        start.set_start()
                    if end is None:
                        end: Spot = grid[ROWS - 5][ROWS - 5]
                        end.set_end()
                    buttons["Start"].text = "Stop"
                    clear_closed_opens(grid)
                    for row in grid:
                        for spot in row:
                            spot.draw(win)
                            spot.update_neighbors(grid)
                    if ALGORITHM == 2:
                        dijkstra_algorithm(lambda: draw(win, grid, ROWS, width, buttons=buttons), grid, start,
                                           end, buttons=buttons)

                    if ALGORITHM == 1:
                        algorithm_a_star(lambda: draw(win, grid, ROWS, width, buttons=buttons), grid, start,
                                         end, buttons=buttons)

                    buttons["Start"].text = "Start"
                    start.set_start()
                    # end.set_end()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    pygame.event.post(Start_Algorithm)
                if event.key == pygame.K_m:
                    menu(pause_width, pause_height, buttons=buttons, grid=grid)
                if event.key == pygame.K_c:
                    main(win, width)
                if event.key == pygame.K_d:
                    generate_maze(grid, lambda: draw(win, grid, ROWS, width, buttons=buttons), end.get_pos(),
                                  start.get_pos())

    pygame.quit()


pygame.init()
tut(WIN)
main(WIN, WIDTH)
