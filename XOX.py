import pygame as pg

pg.init()
winSize = (600, 600)
window = pg.display.set_mode(winSize)
pg.display.set_caption("XOX Game")

clock = pg.time.Clock()
FPS = 7

scoreFontSize = 50
scoreFont = pg.font.SysFont(None, scoreFontSize)

gridFontSize = 100
gridFont = pg.font.SysFont(None, gridFontSize)

gridSize = (int(winSize[0] / 3), int(winSize[1] / 3))
halfGridSize = (int(gridSize[0] / 2), int(gridSize[1] / 2))
isTurnOfX = True

scores = (0, 0)
table = [[0,0,0] for _ in range(3)]
spaceLeftInTable = 9

def restart():
	global table, isTurnOfX, spaceLeftInTable
	table = [[0,0,0] for _ in range(3)]
	isTurnOfX = True
	spaceLeftInTable = 9

def display():
	window.fill((0,0,0))

	currX, currY = 0, 0
	for _ in range(2):
		currX += gridSize[0]
		currY += gridSize[1]
		pg.draw.line(window, (255,255,255), (0, currY), (winSize[0], currY))
		pg.draw.line(window, (255,255,255), (currX, 0), (currX, winSize[1]))

	currX, currY = halfGridSize

	for row in table:
		for _id in row:
			if _id == 0:
				currX += gridSize[0]
				continue

			if _id == 1:
				text = gridFont.render("X", True, (255,255,255))
				rect = text.get_rect()
				window.blit(text,
					(currX - rect[2],
					currY - rect[3]))
			if _id == 2:
				text = gridFont.render("O", True, (255,255,255))
				rect = text.get_rect()
				window.blit(text,
					(currX - rect[2],
					currY - rect[3]))

			currX += gridSize[0]

		currX = halfGridSize[0]
		currY += gridSize[1]

	text = scoreFont.render(f"{scores[0]}", True, (255,0,0))
	rect = text.get_rect()
	window.blit(text, (30, rect[3] - 15))

	text = scoreFont.render(f"{scores[1]}", True, (0,0,255))
	rect = text.get_rect()
	window.blit(text, ((winSize[1] - rect[2]) - 30, rect[3] - 15))

	pg.display.update()

def isThere3SameInLine(x:int, y:int, value:int) -> bool:
	values:tuple = (0,0,0)

	def getValues(pos1:tuple, pos2:tuple, pos3:tuple) -> tuple:
		return (
			table[pos1[1]][pos1[0]],
			table[pos2[1]][pos2[0]],
			table[pos3[1]][pos3[0]])

	def check(values:tuple) -> bool:
		return values[0] == values[1] == values[2]

	if x == 0:
		match y:
			case 0: # right, down, left down
				return \
					check(getValues((x,y), (1,0), (2,0))) or \
					check(getValues((x,y), (0,1), (0,2))) or \
					check(getValues((x,y), (1,1), (2,2)))
			case 1: # right, down
				return \
					check(getValues((x,y), (1,1), (2,1))) or \
					check(getValues((0,0), (x,y), (0,2)))
			case 2: # right, up, right up
				return \
					check(getValues((x,y), (1,2), (2,2))) or \
					check(getValues((x,y), (0,1), (0,0))) or \
					check(getValues((x,y), (1,1), (2,0)))
	if x == 1:
		match y:
			case 0: # right, down
				return \
					check(getValues((0,0), (x,y), (2,0))) or \
					check(getValues((x,y), (1,1), (1,2)))
			case 1: # right, down, right down, left down
				return \
					check(getValues((0,1), (x,y), (2,1))) or \
					check(getValues((1,0), (x,y), (1,2))) or \
					check(getValues((0,0), (x,y), (2,2))) or \
					check(getValues((2,0), (x,y), (0,2)))
			case 2: # right, up, right up
				return \
					check(getValues((0,2), (x,y), (2,2))) or \
					check(getValues((x,y), (1,1), (1,0))) or \
					check(getValues((0,1), (x,y), (2,0)))
	if x == 2:
		match y:
			case 0: # right, down, left down
				return \
					check(getValues((0,0), (1,0), (x,y))) or \
					check(getValues((x,y), (2,1), (2,2))) or \
					check(getValues((x,y), (1,1), (0,2)))
			case 1: # right, down
				return \
					check(getValues((0,1), (1,1), (x,y))) or \
					check(getValues((2,0), (x,y), (2,2)))
			case 2: # right, up, left up
				return \
					check(getValues((0,2), (1,2), (x,y))) or \
					check(getValues((x,y), (2,1), (2,0))) or \
					check(getValues((x,y), (1,1), (0,0)))

	return False

def place(x:int, y:int):
	global table, isTurnOfX, scores, spaceLeftInTable

	if y < 0 or y > len(table): return
	if x < 0 or x > len(table[0]): return

	if table[y][x] != 0: return

	value = 1 if isTurnOfX else 2
	table[y][x] = value
	spaceLeftInTable -= 1

	if isThere3SameInLine(x, y, value):
		if isTurnOfX:
			scores = (scores[0]+1, scores[1])
		else:
			scores = (scores[0], scores[1]+1)
		restart()
	else:
		if spaceLeftInTable == 0:
			restart()
		else:
			isTurnOfX = 0 if isTurnOfX else 1

def userInputs() -> bool:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			return False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				return False
			if event.key == pg.K_r:
				restart()
		if event.type == pg.MOUSEBUTTONDOWN:
			x, y = pg.mouse.get_pos()
			resultX, resultY = 0, 0

			if x < gridSize[0]:
				resultX = 0
			elif x < gridSize[0] * 2:
				resultX = 1
			else:
				resultX = 2

			if y < gridSize[1]:
				resultY = 0
			elif y < gridSize[1] * 2:
				resultY = 1
			else:
				resultY = 2

			place(resultX, resultY)

	return True

if __name__ == "__main__":
	while userInputs():
		display()
		clock.tick(FPS)
