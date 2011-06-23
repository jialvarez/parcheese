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

    def selectChecker(self, player):
        chkToMove = []
        checkers = player.getCheckers()

        # select the checkers that can be moved
        i = 0
        for chk in checkers:
            if chk.getPos() <> 0 and not chk.inNirvana():
                chkToMove.append(i)
                i += 1

        if len(chkToMove) > 0:
            from random import choice
            selected = choice(chkToMove)
        else:
            return None

        return player.getChecker(selected)

    def turn(self, player):
        """ Method where player throw the dice and makes his move """

        # Step 1 - throw the dice!
        dVal = self.dice.throwDice()
        logging.info("%s gets %s ", player.getName(), str(dVal))

        # Step 2 - Select checker to move
        # FOR TESTING PURPOSES ONLY: we select randomly
        # a checker. This forces the movement of many checkers.
        chk = self.selectChecker(player)

        # in this case, we can not move none of our checkers
        if not chk:
            logging.info("player %s can not move none of his checkers ", \
                    player.getName())
            return

        logging.info("%s select checker in %s ", player.getName(),
          str(chk.getPos()))

        # if pos is 0, this checker it is at home
        if chk.getPos() == 0:
            logging.info("%s cannot move this checker, it is at home!",\
                         player.getName())
            return

        # If dice is 5 and player have checkers in home, take out one of them
        if dVal == 5:
            chkFive = player.checkersAtHome()
            if chkFive is not False: # you have checkers at home
                res = player.toInitPos(chkFive, self.squares)
                if res == True:
                    return # chk moved to initial pos, else go on

        # Check how many times the player has obtained six consecutively
        if dVal == 6:
            if player.incSixTimes() == False:
                # Move checker to HOME
                logging.info("Player obtained 6 three times, GO HOME!")
                player.toHome(chk, self.squares)
                return
            elif player.checkersAtHome() == False and \
                        chk.inStairs() == False:
                # you do not have checkers at home
                dVal = dVal * 2
                logging.info("%s do not have checkers at home, got 12!",\
                             player.getName())
        else:
            player.resetSixTimes()

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

        result = player.move(chk, dVal, self.squares, stairSquares)

        # if we got 10 or 20 reward, move checker this quantity
        if result == 10 or result == 20:
            chk = self.selectChecker(player)
            if chk:
                player.move(chk, result, self.squares, stairSquares)

        # If dice is 6 throw again
        if dVal == 6:
            self.turn(player)
