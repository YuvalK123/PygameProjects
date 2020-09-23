import pygame, math
from queue import PriorityQueue

#colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#pygame init
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Algorithm")

class Node(object):
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def make_start(self):
		self.color = ORANGE

	def make_end(self):
		self.color = TURQUOISE

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_path(self):
		self.color = PURPLE

	def  draw(self, win):
		#rect(window, color, (x,y,width, height))
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []

		#down neighbour
		if self.row < self.total_rows -1:
			down = grid[self.row + 1][self.col]
			if not down.is_barrier(): self.neighbors.append(down)

		#up neighbor
		if self.row > 0:
			up = grid[self.row - 1][self.col]
			if not up.is_barrier(): self.neighbors.append(up)

		#left neighbor
		if self.col > 0:
			left = grid[self.row][self.col - 1]
			if not left.is_barrier(): self.neighbors.append(left)

		#right neighbour
		if self.col < self.total_rows -1:
			right = grid[self.row][self.col + 1]
			if not right.is_barrier(): self.neighbors.append(right)


	def __lt__(self):
		'''less then method.'''
		return False


def heuristic(p1, p2):
	'''manhattan distance point1, point2'''
	x1,y1 = p1
	x2,y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)
	return grid

def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		y = i * gap
		#line(window, bg, start_line, end_line)
		pygame.draw.line(win, GREY, (0, y), (width, y))
		for j in range(rows):
			x = i * gap
			#line(window, bg, start_line, end_line)
			pygame.draw.line(win, GREY, (x, 0), (x, width))

def draw(win, grid, rows, width):
	win.fill(WHITE)
	for row in grid:
		for node in row:
			node.draw(win)
	draw_grid(win, rows, width)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos
	row = y // gap
	col = x // gap
	return row,col
def get_node_from_pos(grid, rows, width):
	pos = pygame.mouse.get_pos()
	row, col = get_clicked_pos(pos, rows, width)
	node = grid[row][col]
	return node

def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)
	start, end = None, None
	run, started = True, False
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			if started:
				continue

			if pygame.mouse.get_pressed()[0]: #left click
				node = get_node_from_pos(grid, ROWS, width)
				if not start and node != end:
					start = node
					start.make_start()
				elif not end and node != start:
					end = node
					end.make_end()
				elif node != end and node != start:
					node.make_barrier()
			elif pygame.mouse.get_pressed()[2]: # right click
				node = get_node_from_pos(grid, ROWS, width)
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)
					AstarAlgorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
				if event.key == pygame.K_c:
					start, end = None, None
					grid = make_grid(ROWS,width)
	pygame.quit()

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		if current.is_start(): break
		current = came_from[current]
		current.make_path()
		draw()

def AstarAlgorithm(draw, grid, start, end):
	count, open_set = 0, PriorityQueue() #count for tie breaker
	open_set.put((0,count,start))
	came_from, open_set_hash = {}, {start}
	pause = False
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = heuristic(start.get_pos(), end.get_pos())

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if pause:
						pause = False 
					else:
					 	pause = True

		if pause:
			continue
		current = open_set.get()[2]
		if current in open_set_hash:
			open_set_hash.remove(current) #check


		if current == end:
			end.make_end()
			reconstruct_path(came_from, current, draw)
			return True #make path
		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1
			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set.queue:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
		draw()
		if current != start:
			current.make_closed()
if __name__ == '__main__':
	main(WIN,WIDTH)