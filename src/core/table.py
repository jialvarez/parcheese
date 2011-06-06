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
import checker
import table
import square
import table_squares

#import sys
import logging


class Table:

    def __init__(self, players):
        self.players = players  # get the players
        self.dice = dice.Dice() # get the dice

        # construct game table with 68 squares + specific for each color
        # 0: yellow, 1: blue, 2: red, 3: green
        self.squares = []
        self.yStair = []
        self.bStair = []
        self.rStair = []
        self.gStair = []
        self.fillTableSquares()

        # 1 - Create the checkers of each player referencing to HOME square
        # 2 - Take out one checker of each player into their initial position
        for player in self.players:
            player.initCheckers(self.squares[0])# HOME square
            chk = player.getCheckers()[0]       # Take out a checker from HOME
            player.toInitPos(chk, self.squares) # Move to the initial position

    def fillTableSquares(self):
        """ Create all the squares of the board """

        for key in table_squares.normalSR:
            _isSecure = int(key in table_squares.securesSQ and True or False)
            self.squares.append(square.Square(key, _isSecure))

        # Stair squares for each color
        # with "for key in yellowSquares" the order sometimes varies :S
        for key in table_squares.yStairsSR:
            typ = 3 if (key in table_squares.nirvanasSQ) else 2
            self.yStair.append(square.Square(key, typ))

        for key in table_squares.bStairsSR:
            typ = 3 if (key in table_squares.nirvanasSQ) else 2
            self.bStair.append(square.Square(key, typ))

        for key in table_squares.rStairsSR:
            typ = 3 if (key in table_squares.nirvanasSQ) else 2
            self.rStair.append(square.Square(key, typ))

        for key in table_squares.gStairsSQ:
            typ = 3 if (key in table_squares.nirvanasSQ) else 2
            self.gStair.append(square.Square(key, typ))

    def turn(self, player):
        """ Method where player throw the dice and makes his move """

        # Step 1 - throw the dice!
        dVal = self.dice.throwDice()
        logging.info("%s gets %s ", player.getName(), str(dVal))

        # TODO : If dice is 5 and player have checkers in home, take out one of
        # them.

        # Check how many times the player has obtained six consecutively
        if dVal == 6:
            if player.incSixTimes() == False:
                # TODO: Move checker to initial position or HOME?
                logging.info("Player obtained 6 three times consecutively")
                return
        else:
            player.resetSixTimes()

        # Step 2 - Select checker to move
        chkId = 0
        chk = player.getChecker(chkId)
        logging.info("%s select checker in %s ", player.getName(),
          str(chk.getPos()))

        # Step 3 - Move
        stairSquares = []
        if player.getColor() == "red":
            stairSquares = self.rStair
        elif player.getColor() == "green":
            stairSquares = self.gStair
        elif player.getColor() == "blue":
            stairSquares = self.bStair
        else:                    # Yellow
            stairSquares = self.yStair
        player.move(chk, dVal, self.squares, stairSquares)

        # TODO : If dice is 6 throw again
