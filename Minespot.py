class minespot:
    def __init__(self):
        self.isMine = False
        self.isFlagged = False
        self.numAdjMines = 0
        self.name = ''

    def setName(self, str):
        self.name = str
    def getName(self):
        return self.name
    def setMineStatus(self):
        self.isMine = True

    def flag(self):
        self.isFlagged = True

    def tickAdjMines(self):
        self.numAdjMines += 1

    def getMineStatus(self):
        return self.isMine

    def isFlagged(self):
        return self.isFlagged
    def setNumAdjMines(self,x):
        self.numAdjMines = x

    def getAdjMines(self):
        return self.numAdjMines
