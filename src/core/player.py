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

from checker import Checker
import square
import sys
import logging


class Player:
    """ Represent a player in the game.

    Each player has its color, name and checkers."""

    def __init__(self, name, color):
        """ Constructor """

        assert (color == "red" or color == "blue" or
                color == "green" or color == "yellow")
        self.name = name        # name of player
        self.color = color
        self.checkers = []

        # Determine initial and last positions depending on color
        if color == 'yellow':
            self.initPos = 5
            self.lastPos = 68
        elif color == 'blue':
            self.initPos = 22
            self.lastPos = 17
        elif color == 'red':
            self.initPos = 39
            self.lastPos = 34
        elif color == 'green':
            self.initPos = 56
            self.lastPos = 51

        logging.debug("Init/End positions of %s [%s:%s]", self.name,
            self.initPos, self.lastPos)

        # times that player has obtained 6 with the dice consecutively
        self.sixTimes = 0

    def initCheckers(self, homeSquare):
        """ Initialize checkers of player """
        # list comprehension for getting the checkers list (3 others at home)
        self.checkers = [Checker(self, homeSquare) for chk in range(4)]

    def resetSixTimes(self):
        """ Reset the sixTimes counter. """
        self.sixTimes = 0

    def incSixTimes(self):
        """ Increment the sixTimes counter and return True. If it cannot be
        incremented then it's reseted and the function return False. """
        if self.sixTimes == 2:
            self.resetSixTimes()   # Reset counter
            return False        # Invalid increment. TODO -> kill checker
        else:
            self.sixTimes = self.sixTimes + 1
            return True

    def getName(self):
        """ Get name of player """
        return self.name

    def getCheckers(self):
        """ Get list of checkers """
        return self.checkers

    def getChecker(self, checkerId):
        """ Select a checker by its id """

        chk = self.checkers[checkerId]
        if chk.inNirvana() == True:
            logging.warn("Error: checker in nirvana was selected")
            # TODO: Change direct exit with a warning message
            sys.exit(0)
        else:
            return chk

    def getLastCheckerPosition(self):
        return self.checkers[0].getLastPos()

    def toHome(self, chk, normalS):
        curSq = chk.getSquare()           # Current square
        curSq.popChecker(chk)
        newSq = normalS[0]
        newSq.addChecker(chk)
        logging.info("checker moved to %d", chk.getPos())

    def toInitPos(self, chk, squares):
        """ Move a checker to the initial position of the player """
        squ = squares[self.initPos]
        chkInSq = len(squ.getCheckers())
        if chkInSq == 2:
            logging.warn("You cannot take out more checkers at initial pos,"
                          " it has been occupied by two of your checkers")
            return False
        else:
            squ.addChecker(chk)
            logging.info("%s move checker to initial position", self.name)
            if chkInSq == 1:
                logging.info("Square %d locked!", squ.getID())
                squ.setLock(True) # lock this square
            return True

    def getColor(self):
        """ Get the color of the player """
        return self.color

    def checkersAtHome(self):
        """ If there is a checker at HOME, return it """
        for chk in self.checkers:
            if chk.getPos() == 0:
                return chk
        return False

    def nearStairs(self, chk):
        """ Determine if a checker is near its stairs """
        # Note that high movements are of 6, 10 and 20
        if self.color == "yellow":
            if chk.getPos() > (self.lastPos - 19):
                return True
        else:
            if  chk.getPos() > (self.lastPos - 19) and \
                chk.getPos() < self.initPos:
                return True
        return False

    def checkMobility(self, rng, normalS, newSq):
        """ see if any square in the range of movement is locked """
        for sq in rng:
            # False: you can not move in this range
            if normalS[sq].isLocked():
                logging.warn("You can not pass through the range,"
                             " square %d is locked!", normalS[sq].getID())
                return False

        return newSq

    def checkMobEnterStairs(self, startIdx, endIdx, squares, stairS):
        rng = range(startIdx, endIdx)
        logging.info("Checking range: " + str(rng))
        newSq = self.checkMobility(rng, squares, stairS)

        if newSq == False: return
        else: return newSq


    def move(self, chk, dVal, normalS, stairS):
        """ Do the checker movement
        Arguments
        chk : Checker to move
        dVal: Dice value obtained
        normalS : Ref to Normal squares
        stairS  : Ref to Stair squares of the player color
        """

        curSq = chk.getSquare()           # Current square

        # Check type of movement (normal, from normal to stairs, stairs)
        newPos = curSq.getID() + dVal

        if chk.isInStairs(): # Already in stairs
            logging.debug("in-stairs movement ")
            # Check mobility : we pass the nirvana
            if (newPos) > stairS[7].getID():
                logging.info("You cannot move this checker. Overpass nirvana")
                return
            else:
                # get start and end pos inside the stairs
                startIdx = curSq.getID() - stairS[0].getID() + 1
                endIdx = newPos - stairS[0].getID()

                # exclude nirvana from computing
                endIdx = endIdx if endIdx == 7 else endIdx + 1

                # get range
                rng = range(startIdx, endIdx)

                # Obtain reference to new square
                newSq = self.checkMobility(rng,
                                           stairS,
                                           stairS[newPos - stairS[0].getID()])

                if newSq == False: return
        else:
            # Check if we are going to enter in the stairs
            if self.nearStairs(chk) and newPos > self.lastPos:
                logging.debug("movement entering in stairs")
                chk.setInStairs()

                targetSq = stairS[newPos - self.lastPos - 1]

                # get range until lastPosition
                newSq = self.checkMobEnterStairs(curSq.getID()+1, 
                                                 self.lastPos+1,
                                                 normalS,
                                                 targetSq)

                if newSq is not False:
                    # get range from first stair position to newPosition
                    newSq = self.checkMobEnterStairs(0, newPos - self.lastPos,
                                                     stairS, targetSq)
                else: 
                    return

                if newSq == False: return
                # if we are here, we have a free target square,
                # with nobody inside it
            else:
                logging.debug("Normal movement")
                if newPos > 68:
                    newPos -= 68
                    rng = range(curSq.getID(), 68)
                    rng += range(1, newPos+1)
                else:
                    rng = range(curSq.getID()+1, newPos+1)

                newSq = self.checkMobility(rng, normalS, normalS[newPos])
                if newSq == False: return

        curSq.popChecker(chk)
        newSq.addChecker(chk)
        logging.info("checker moved to %s", str(chk.getPos()))
        if newSq.isNirvana():
            # TODO : Check if all checkers are in nirvana (4)
            chk.setInNirvana()
            logging.info("IN NIRVANA!")
