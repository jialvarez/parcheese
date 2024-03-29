# Parcheese
#
# Copyright 2011 Parcheese Team.
# Author: J. Ignacio Alvarez <neonigma@gmail.com>
# Author: Luis Diaz Mas <piponazo@gmail.com>
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

import checker
import table
import square
import table_squares

import logging


class Table:

    def __init__(self, players):
        self.players = players  # get the players

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

    def getNormalSquares(self):
        """ Get normal squares of the board """
        return self.squares

    def getStairSquares(self, player):
        """ Get stair squares of the board """
        if player.getColor() == "blue":
           return self.bStair
        elif player.getColor() == "red":
            return self.rStair
        elif player.getColor() == "yellow":
            return self.yStair
        elif player.getColor() == "green":
            return self.gStair

    def turn(self, player, dVal=0, chkID=None, manualSelect=False):
        """ Method where player throw the dice and makes his movement """

        logging.info("Received checker: %s", chkID)

        result = None
        resOut = None

        stairSquares = []
        if player.getColor() == "red":
            stairSquares = self.rStair
        elif player.getColor() == "green":
            stairSquares = self.gStair
        elif player.getColor() == "blue":
            stairSquares = self.bStair
        else:                    # Yellow
            stairSquares = self.yStair

        # If dice is 5 and player have checkers in home, take out one of them
        if dVal == 5:
            player.resetSixTimes()
            chkFive = player.checkersAtHome()
            if chkFive is not False: # you have checkers at home
                resOut = player.toInitPos(chkFive, self.squares)
                if resOut == True:
                    return True # chk moved to initial pos, else go on
                elif resOut == False:
                    return -1
                elif resOut == 20:
                    return 20

        if dVal == -1:
            # if we can select a checker, we select it, otherwise enter here
            if manualSelect == False:
                # we jump previous condition, because we can't take out more
                # checkers from home, but take all others below in consideration
                chk = player.checkIfHasBarrier(None, 5, self.squares,
                                               stairSquares)
                chkID = chk.getID()

            player.resetSixTimes()

            dVal = 5

        # If we got 20 moving to initial pos, we eat a enemy checker
        if resOut <> 20 and resOut <> 10:
            canMove = player.checkIfPlayerCanMove(dVal, self.squares,
                                                  stairSquares)

            # in this case, we can not move none of our checkers
            if canMove == False:
                logging.info("player %s cannot move none of his checkers ",
                        player.getName())
                return True

            # check if selected checker is in Nirvana or at home
            chk = player.selectChecker(dVal, stairSquares, chkID)

            if chk == False: # in Nirvana or at home
                return False

            logging.info("Selected checker: %s", chkID)

            newSq = player.checkIfChkCanMove(chk, dVal, self.squares,
                                              stairSquares)

            # in this case, we can not move this checker
            if newSq == False:
                logging.info("player %s cannot move this checker ",
                        player.getName())
                # follow in player turn, but try another checker
                if dVal == 6 or dVal == 12:
                    return -6
                else:
                    logging.info("player %s has a bug ", 
                            player.getName())
                    return dVal

            # Check how many times the player has obtained six consecutively
            if dVal == 6:
                if player.incSixTimes() == False:
                    # Move checker to HOME
                    logging.info("Player obtained 6 three times, GO HOME!")
                    player.toHome(chk, self.squares)
                    return True
                elif player.checkersAtHome() == False:
                    # you do not have checkers at home
                    dVal = dVal * 2
                    logging.info("%s do not have checkers at home, got 12!",
                                 player.getName())
                    # check if we have barrier, with 12 we must break it
                    chk = player.checkIfHasBarrier(chk, dVal, self.squares,
                                                   stairSquares)
                    newSq = player.checkIfChkCanMove(chk, dVal, self.squares,
                                                     stairSquares)

                    # in this case, we can not move this checker
                    #if newSq == False:
                    #    logging.info("player %s cannot move this checker, return -6 ",
                    #            player.getName())
                    #    # follow in player turn, but try another checker
                    #    #self.turn(player, 6, chkID)
                    #    return -12
            elif not ((dVal == 20 or dVal == 10) and player.getSixTimes() > 0):
                player.resetSixTimes()

        # Step 3 - Move
        if resOut == False or resOut == None:
            # nothing happened taking out one of my checkers,
            # or two checkers are in my initial position
            result = player.move(chk, chk.getSquare(), newSq, self.squares)
            logging.info("number of six: %s", player.getSixTimes())
            logging.info("dVal: %s", dVal)
            if player.getSixTimes() == 2 and \
                    (dVal == 20 or dVal == 10):
                return 6

        # if we got 10 or 20 reward, move checker this quantity
        # resOut points eating when take out a checker to init pos
        if result == 10 or result == 20 or resOut == 20:
            if resOut == 20:
                result = resOut

            #self.getReward(player, result, stairSquares, chkID)
            canMove = player.checkIfPlayerCanMove(result, self.squares,
                                                  stairSquares)
            if canMove == True:
                chk = player.selectChecker(result, stairSquares, chkID)
                newSq = player.checkIfChkCanMove(chk, result, self.squares,
                                                  stairSquares)
                # in this case, we can not move this checker
                if newSq == False:
                    logging.info("player %s cannot move selected checker ",
                            player.getName())
                    # follow in player turn, but try another checker
                    #self.getReward(player, result, stairSquares)
                    return result
    
                #player.move(chk, chk.getSquare(), newSq, self.squares)
                return result
            else:
                logging.info("player %s cannot move none of his checkers ",
                        player.getName())
                return True

        # If dice is 6 throw again
        if dVal == 6 or dVal == 12:
            #self.turn(player, 0, chkID)
            return dVal
        
        return True

