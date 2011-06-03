# Parcheese
#
# Copyright 2011 Parcheese Team.
# Author: J. Ignacio Alvarez <neonigma@gmail.com>
# Author: Edorta Garcia Gonzalez <edortagarcia@gmail.com>
#
# Parcheese is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# Parcheese is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Parcheese. If not, see <http://www.gnu.org/licenses/>.

import dice
import square
import checker
import table
from table_squares import tableSquares, yellowSquares, greenSquares, \
        redSquares, blueSquares


class Table:

    def __init__(self, players):
        # get the players
        self.players = players

        # get the dice
        self.dice = dice.Dice()

        # construct game table with 68 squares + specific for each color
        self.squares = []
        self.specialSquares = []

        # 0: yellow, 1: blue, 2: red, 3: green
        self.specialYSquares = []
        self.specialBSquares = []
        self.specialRSquares = []
        self.specialGSquares = []

        self.fillTableSquares()

        # get players in game
        self.getPlayers()

    def fillTableSquares(self):

        for key in tableSquares:
            _secured = [5, 12, 17, 22, 29, 34, 39, 46, 51, 56, 63, 68]
            _isSecure = key in _secured and True or False
            self.squares.append(square.Square(key, \
                    tableSquares.get(key), _isSecure))

        # four moveCheckerHereerent paths for four colors :)
        for yellowKey in yellowSquares:
            self.specialYSquares.append(square.Square(yellowKey, \
                    yellowSquares.get(yellowKey), True))

        print self.specialYSquares

        for blueKey in blueSquares:
            self.specialBSquares.append(square.Square(blueKey, \
                    blueSquares.get(blueKey), True))

        for redKey in redSquares:
            self.specialRSquares.append(square.Square(redKey, \
                    redSquares.get(redKey), True))

        for greenKey in greenSquares:
            self.specialGSquares.append(square.Square(greenKey, \
                    greenSquares.get(greenKey), True))

    def getPlayers(self):

        for player in self.players:
            # get the first checker and put in game
            firstChecker = player.getCheckers()[0]

            # get initial position for this first checker
            initPos = firstChecker.getInitialPosition()

            # move to the initial position (1, 22, 39 or 56),
            # depending on the color of the checker
            player.move(firstChecker, initPos)

            # add the checker to its initial square
            square = self.squares[initPos]
            square.addChecker(firstChecker)

            print "I'm square " + str(square.getSquareId()) + " and I have " +\
                  "this checkers in me: " + str(square.getCheckers())

    # the checker must be indicated by sending the mouse selection

    def playerMoves(self, player, checkerId):
        """ Method where player throw the dice and makes his move """

        # Step 1 - throw the dice!
        dVal = self.dice.throwDice()

        # Step 2 - Select checker to move
        chk = player.getChecker(checkerId)

        if chk.inNirvana() == True:
            print "CHECKER " + str(checkerId) + " OF " + \
            str(player.getLogin()) + " IS IN NIRVANA!"
            return

        cColor = chk.getColor()

        # dVal = 6 #___THIS is ::ONLY:: for test the next "if". this line
        # will be removed soon.

        # checking how many times player has obtained six as dVal
        # consecutively
        # check if dVal was 6. If it was, increment counter var (resWasSix)
        if dVal == 6:
            player.setResWasSix() #increment counter

            #check if player has obtained 6 as dVal 3 times or more
            if player.getResWasSix() >= 3:
                #:::HERE checker have to be moved to initial position
                print "D'oh!" #for testing
                #newPos = chk.initialPosition
                return
        # if dVal wasn't 6 reinitialize counter
        else:
            player.setResWasSix(reinitialize=True)

        print "\nPlayer " + str(player.getLogin()) + \
                          " gets " + str(dVal) + \
                          " with last position " + \
                          str(player.getLastCheckerPosition())

        oldPos = chk.getPosition()      # Get initial position of checker
        newPos = oldPos + dVal          # Calculate new position

        # move to new position and get it
        if chk.isAtHome() == True and newPos > 8:
            print "CHECKER " + str(checkerId) + " OF " + \
            str(player.getLogin()) + " CANNOT BE MOVED!"
            return

        # get checkers in square to leave
        if chk.isAtHome() == False:
            square = self.getSquareToAddChecker(None, oldPos)
        else:
            square = self.getSquareToAddChecker(cColor, oldPos)

        squares = square.getCheckers()
        print "square " + str(oldPos) + " before: " + str(squares)

        # pop this checker from square to leave
        if chk in squares:
            squares.pop(squares.index(chk))

        print "square " + str(oldPos) + " after: " + str(squares)

        print "Checker " + str(chk) + " leaves position " + \
                str(oldPos)

        # get initial and last checker position
        # initPos = player.getInitialCheckerPosition() # It isn't used
        lastPos = player.getLastCheckerPosition()

        # get square in new position
        square = self.getNewSquare(player, chk, newPos, lastPos, cColor, dVal)

        square.addChecker(chk)

        print "I'm square " + str(square.getSquareId()) + " and I have " + \
              "this checkers in me: " + str(square.getCheckers())

        if chk.isAtHome() == True and newPos == 8:
            chk.setInNirvana()
            print "CHECKER " + str(checkerId) + " OF " + \
                               str(player.getLogin()) + \
                               " ENTERED AT HOME!"

    def getNewSquare(self, player, chk, newPos, lastPos, cColor, dVal):
        # see if we are at home squares
        if chk.isAtHome() == False:
            # first time we enter at home
            if chk.isEnteringAtHome(newPos) == True:
                moveCheckerHere = newPos - lastPos

                chk.setAtHome()
                newPos = player.move(chk, moveCheckerHere)

                return self.getSquareToAddChecker(cColor, moveCheckerHere)
            # normal case (normal squares in the board)
            else:
                if cColor is not 'yellow' and newPos > 68:
                    moveCheckerHere = newPos - 68
                    passSixtyEight = True
                else:
                    moveCheckerHere = dVal
                    passSixtyEight = False

                newPos = player.move(chk, moveCheckerHere, passSixtyEight)

                return self.getSquareToAddChecker(None, newPos)
        # we are in home squares (from 1 to 8)
        else:
            moveCheckerHere = newPos

            newPos = player.move(chk, moveCheckerHere)
            return self.getSquareToAddChecker(cColor, moveCheckerHere)

    def getSquareToAddChecker(self, color, checkerPosition):

        if color is None:
            return self.squares[checkerPosition]
        else:
            if color == 'yellow':
                return self.specialYSquares[checkerPosition-1]
            if color == 'red':
                return self.specialRSquares[checkerPosition-1]
            if color == 'blue':
                return self.specialBSquares[checkerPosition-1]
            if color == 'green':
                return self.specialGSquares[checkerPosition-1]
