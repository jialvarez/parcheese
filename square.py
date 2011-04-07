class Square:

    def __init__(self, squareId, position):
        self.squareId = squareId
        self.position = position
        self.checkerQty = 0
        self.locked = False
        self.checkers = ()

    def setLocked(self):
        self.locked = not self.locked

    def setCheckerQty(self):
        seld.checkerQty = len(self.checkers)

    def addChecker(self, checker):
        self.checkers = checker
