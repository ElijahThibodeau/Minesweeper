import pygame, sys, random
from pygame.locals import *
from Minespot import *

pygame.init()

FPS = 30
WINDOWWIDTH = 600
WINDOWHEIGHT = 320
BOXSIZE = 20
BOARDWIDTH = 30  # number of boxes in a row
BOARDHEIGHT = 16  # number of boxes in a column

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
numCorrectFlags = 0

#          R       G       B
BOXCOLOR = (200, 200, 200)
OUTLINELT = (230, 230, 230)
OUTLINEDK = (100, 100, 100)
mines = []
flaggedBoxes = []
NUMBERIMAGES = []
for i in range(1, 9):
    temp = pygame.transform.scale(pygame.image.load('img%s.png' % i), (19, 19)).convert()
    temp.set_colorkey((0, 0, 0))
    NUMBERIMAGES.append(temp)
IMGMINE = pygame.transform.scale(pygame.image.load('img9.png'), (20, 20)).convert()
IMGMINE.set_colorkey((255, 0, 255))
NUMBERIMAGES.append(IMGMINE)
IMGFLAG = pygame.transform.scale(pygame.image.load('img10.png'), (19, 19)).convert()
IMGFLAG.set_colorkey((255, 0, 255))
NUMBERIMAGES.append(IMGFLAG)
GAMEENDIMG = pygame.transform.scale(pygame.image.load('gameEndImage.jpg'), (420, 269))
numFlags = 0
LEFT = 1
RIGHT = 3
mineCount = 0


def main():
    global mineCount, numFlags, numCorrectFlags, mines, flaggedBoxes, revealedBoxes
    flaggedBoxes = []
    revealedBoxes = []
    numFlags = 0
    numCorrectFlags = 0
    mines = []
    for i in range(0, 30):
        temp = []
        for j in range(0, 16):
            temp.append(minespot())
        mines.append(temp)
    revealedBoxes = []
    mineCount = 0
    for i in range(0, 30):
        temp = []
        temp2 = []
        for j in range(0, 16):
            temp.append(False)
            temp2.append(False)
        revealedBoxes.append(temp)
        flaggedBoxes.append(temp2)
    firstClick = True
    drawBoard()
    mousex, mousey = 0, 0
    while True:
        mouseClicked = False
        executeFlag = False
        for event in pygame.event.get():
            # event handling loop
            if event.type == QUIT or event.type == KEYUP and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_r:
                main()
                mousex, mousey = event.pos
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                if event.button == RIGHT:
                    executeFlag = True
                    mousex, mousey = event.pos
                else:
                    executeFlag = False
                mousex, mousey = event.pos
                mouseClicked = True
        (boxx, boxy) = getBoxAtPixel(mousex, mousey)
        if not executeFlag and boxx != None and boxy != None:
            if mouseClicked and firstClick != True:
                if not revealedBoxes[boxx][boxy] and not flaggedBoxes[boxx][boxy]:
                    revealMine(boxx, boxy, mines[boxx][boxy].getAdjMines())
                    pygame.display.update()
            elif mouseClicked != False and firstClick == True:
                setUpRandomizedBoard(boxx, boxy)
                revealMine(boxx, boxy, 0)
                firstClick = False
                pygame.display.update()
        elif executeFlag and boxx != None and boxy != None:
            if not flaggedBoxes[boxx][boxy] and not revealedBoxes[boxx][boxy] and mouseClicked:
                numFlags += 1
                flaggedBoxes[boxx][boxy] = True
                (left, top) = leftTopCoordsOfBox(boxx, boxy)
                newRect = pygame.Rect(left + 1, top + 1, BOXSIZE, BOXSIZE)
                DISPLAYSURF.blit(NUMBERIMAGES[9], (left, top))
                pygame.display.update()
                if (mines[boxx][boxy].getMineStatus() == 0):
                    numCorrectFlags += 1
                if numCorrectFlags == mineCount:
                    endGame()
            elif flaggedBoxes[boxx][boxy] == True and revealedBoxes[boxx][boxy] == False and mouseClicked:
                flaggedBoxes[boxx][boxy] = False
                revealedBoxes[boxx][boxy] = False
                drawBlankTile(boxx, boxy)
                if (mines[boxx][boxy].getMineStatus() == 0):
                    numCorrectFlags -= 1
            executeFlag = False


def leftTopCoordsOfBox(l, t):
    return l * BOXSIZE, t * BOXSIZE


def rightBottomCoordsOfBox(r, b):
    return ((r + 1) * BOXSIZE, (b + 1) * BOXSIZE)


def drawBoard():
    for i in range(0, len(mines)):
        for j in range(0, len(mines[i])):
            drawBlankTile(i, j)


def drawBlankTile(i, j):
    (left, top) = leftTopCoordsOfBox(i, j)
    (right, bot) = rightBottomCoordsOfBox(i, j)
    pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
    pygame.draw.aaline(DISPLAYSURF, OUTLINEDK, (left, top), (left, bot), 1)
    pygame.draw.aaline(DISPLAYSURF, OUTLINEDK, (left, top), (right, top), 1)
    pygame.display.update()


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def setUpRandomizedBoard(boxx, boxy):
    global mines
    global mineCount
    numMines = 99
    while numMines > 0:
        i = random.randint(0, 29)
        j = random.randint(0, 15)
        if mines[i][j].getMineStatus() == 0 and abs(boxx - i) > 2 or abs(boxy - j) > 2:
            if mines[i][j].getMineStatus() == 0:
                mines[i][j].setMineStatus()
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if 0 <= x + i <= 29 and 0 <= y + j <= 15:
                            mines[x + i][y + j].tickAdjMines()
            numMines -= 1
            mineCount += 1


def endGame():
    DISPLAYSURF.blit(GAMEENDIMG, (0, 0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYUP and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_r:
                main()


def revealMine(x, y, num):
    global mineCount
    if (revealedBoxes[x][y] == False):
        (left, top) = leftTopCoordsOfBox(x, y)
        newRect = pygame.Rect(left + 1, top + 1, BOXSIZE, BOXSIZE)
        revealedBoxes[x][y] = True
        if num != 0:
            try:
                if (mines[x][y].getMineStatus() != 0):
                    pygame.Surface.blit(DISPLAYSURF, NUMBERIMAGES[8], newRect)
                    endGame()
                    mineCount += 1
                else:
                    pygame.Surface.blit(DISPLAYSURF, NUMBERIMAGES[num - 1], newRect)
            except IndexError:
                print(num)
        else:
            pygame.draw.rect(DISPLAYSURF, (140, 140, 140), (left + 1, top + 1, BOXSIZE - 1, BOXSIZE - 1))
            revealAllAdjMines(x, y)
    pygame.display.update()


def revealAllAdjMines(x, y):
    for i in range(-1, 2):
        for j in range(-1, 2):
            try:
                if not (i, j) == (0, 0) and x - i >= 0 and y - j >= 0:
                    revealMine((x - i), (y - j), mines[x - i][y - j].getAdjMines())
            except IndexError:
                doNothing()


def revealAllMines():
    for i in range(0, 30):
        for j in range(0, 16):
            if mines[i][j].getMineStatus():
                revealMine(i, j, 4)


def doNothing():
    inm = 0


def revealAllBoxes():
    for i in range(0, 30):
        for j in range(0, 16):
            revealMine(i, j, mines[i][j].getAdjMines())


main()





