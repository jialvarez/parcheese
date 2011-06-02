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

        # four different paths for four colors :)
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
            checkerInitialPos = firstChecker.getInitialPosition()

            # move to the initial position (1, 22, 39 or 56),
            # depending on the color of the checker
            player.move(firstChecker, checkerInitialPos)

            # add the checker to its initial square
            square = self.squares[checkerInitialPos]
            square.addChecker(firstChecker)

            print "I'm square " + str(square.getSquareId()) + " and I have " + \
                  "this checkers in me: " + str(square.getCheckers())


    # the checker must be indicated by sending the mouse selection
    def playerMoves(self, player, checkerId):
        # get checker to move
        checkerToMove = player.getChecker(checkerId)

        if checkerToMove.inNirvana() == True:
              print "THESE CHECKER IS IN NIRVANA!"
              return

        checkerColor = checkerToMove.getColor()
    
        # throw the dice!
        result = self.dice.throwDice()
            
        #result = 6 #___THIS is ::ONLY:: for test the next "if". this line will be removed soon.
            
        # checking how many times player has obtained six as result consecutively
        if result == 6: #check if result was 6. If it was, increment counter var (resWasSix)
            player.setResWasSix() #increment counter

            if player.getResWasSix() >= 3: #check if player has obtained 6 as result 3 times or more
                #:::HERE checker have to be moved to initial position
                print "D'oh!" #for testing
                #newPosition = checkerToMove.initialPosition
                return
        else: #if result wasn't 6 reinitialize counter
            player.setResWasSix(reinitialize = True)

        print "\nPlayer " + str(player.getLogin()) + \
                          " gets " + str(result) + \
                          " with last position " + \
                          str(player.getLastCheckerPosition())

        # get position to leave
        oldCheckerPosition = checkerToMove.getPosition()

        newPosition = oldCheckerPosition + result

        # move to new position and get it
        if checkerToMove.isAtHome() == True and newPosition > 8:
              print "YOU CAN'T MOVE THE CHECKER!"
              return

        # get checkers in square to leave
        if checkerToMove.isAtHome() == False:
            square = self.getSquareToAddChecker(None, oldCheckerPosition)
        else:
            square = self.getSquareToAddChecker(checkerColor, oldCheckerPosition)

        squares = square.getCheckers()
        print "square " + str(oldCheckerPosition) + " before: " + str(squares)

        # pop this checker from square to leave
        if checkerToMove in squares:
            squares.pop(squares.index(checkerToMove))
            
        print "square " + str(oldCheckerPosition) + " after: " + str(squares)

        print "Checker " + str(checkerToMove) + " leaves position " + \
                str(oldCheckerPosition)

        # get initial and last checker position
        initialCheckerPosition = player.getInitialCheckerPosition()
        lastCheckerPosition = player.getLastCheckerPosition()

        # get square in new position 
        square = self.getNewSquare(player, checkerToMove, newPosition, \
                              lastCheckerPosition, checkerColor, result)

        square.addChecker(checkerToMove)

        print "I'm square " + str(square.getSquareId()) + " and I have " + \
              "this checkers in me: " + str(square.getCheckers())

        if checkerToMove.isAtHome() == True and newPosition == 8:
            checkerToMove.setInNirvana()
            print "THESE CHECKER IS AT HOME!"


    def getNewSquare(self, player, checkerToMove, newPosition, \
                     lastCheckerPosition, checkerColor, result):
        # see if we are at home squares
        if checkerToMove.isAtHome() == False:
            # first time we enter at home
            if checkerToMove.isEnteringAtHome(newPosition) == True:
                diff = newPosition - lastCheckerPosition

                checkerToMove.setAtHome() 
                newCheckerPosition = player.move(checkerToMove, diff)

                return self.getSquareToAddChecker(checkerColor, diff)
            # normal case (normal squares in the board)
            else:
                if checkerColor is not 'yellow' and newPosition > 68:
                    diff = newPosition - 68
                    passSixtyEight = True
                else:
                    diff = result
                    passSixtyEight = False

                newCheckerPosition = player.move(checkerToMove, diff, passSixtyEight)

                return self.getSquareToAddChecker(None, newCheckerPosition)
        # we are in home squares (from 1 to 8)
        else:
            diff = newPosition

            newCheckerPosition = player.move(checkerToMove, diff)
            return self.getSquareToAddChecker(checkerColor, diff)

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

