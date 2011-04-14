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

class Table:

    def __init__(self, players):
        # get the players
        self.players = players

        # get the dice
        self.dice = dice.Dice()

        # construct game table with 101 squares
        self.squares = []

        for key in table_squares:
            _secured = [5, 12, 17, 22, 29, 34, 39, 46, 51, 56, 63, 68]

            if key in _secured:
                _isSecure = True
            else:
                _isSecure = False

            self.squares.append(square.Square(key, table_squares.get(key), _isSecure))

        for player in players:
            # get the first checker and put in game
            firstChecker = player.getCheckers()[0]

            # get initial position for this first checker
            checkerInitialPos = firstChecker.getInitialPosition()

            # move to the initial position (1, 22, 39 or 56),
            # depending on the color of the checker
            player.move(firstChecker, checkerInitialPos)

            # add the checker to its initial square
            _square = self.squares[checkerInitialPos]
            _square.addChecker(firstChecker)

            print "I'm square " + str(_square.getSquareId()) + " and I have " + \
                  "this checkers in me: " + str(_square.getCheckers())


    # the checker must be indicated by sending the mouse selection
    def playerMoves(self, player, checkerId):
        # get checker to move
        checkerToMove = player.getChecker(checkerId)

        # throw the dice!
        result = self.dice.throwDice()

        print "\nPlayer " + str(player.getLogin()) + \
                          " gets " + str(result)

        oldCheckerPosition = checkerToMove.getPosition()

        _square = self.squares[oldCheckerPosition]
        _squares = _square.getCheckers()
        print "square " + str(oldCheckerPosition) + " before: " + str(_squares)
        if checkerToMove in _squares:
            _squares.pop(_squares.index(checkerToMove))
            
        print "square " + str(oldCheckerPosition) + " after: " + str(_squares)

        print "Checker " + str(checkerToMove) + " leaves position " + str(oldCheckerPosition)
        newCheckerPosition = player.move(checkerToMove, result)

        _square = self.squares[newCheckerPosition]
        _square.addChecker(checkerToMove)

        print "I'm square " + str(_square.getSquareId()) + " and I have " + \
              "this checkers in me: " + str(_square.getCheckers())

