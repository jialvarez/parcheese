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

import logging


class Square:
    """ Represent a square of the board. """

    def __init__(self, squareId, squareType):
        """ Constructor.
        Arguments:
        squareId - Unique ID for the square
        squareType - 0 : normal; 1 : secured; 2 : stairs; 3 : Nirvana
        """
        self.squareId = squareId    # Unique ID
        self.locked = False         # Locked by two checkers
        self.checkers = []          # Checkers in the square
        self.sType = squareType     # Type of square

    def setLock(self, val):
        """ Change the status of the Set this square as blocked """
        assert(type(val) == bool)
        self.locked = val

    def isLocked(self):
        """ Get if this square is locked """
        return self.locked

    def addChecker(self, chk):
        """ Add a checker to this square"""
        self.checkers.append(chk)
        chk.setSquare(self)

    def popChecker(self, chk):
        """ Remove and existing checker from the list of checkers """
        self.checkers.pop(self.checkers.index(chk))
        # remove lock!
        if self.isLocked():
            self.setLock(False)

    def getID(self):
        """ Get ID of square """
        return self.squareId
    
    def getCoord(self, chk=None, chkNum=None):
        """ Get coordinates values for a square """
        from table_squares import tableSquares, yellowSquares,\
                                  redSquares, blueSquares,\
                                  greenSquares

        if self.squareId == 0:
            return self._getStartCoord(chk, chkNum)

        if self.squareId <= 68:
            return tableSquares[self.squareId]
        elif self.squareId > 68 and self.squareId <= 76:
            return yellowSquares[self.squareId]
        elif self.squareId > 76 and self.squareId <= 84:
            return blueSquares[self.squareId]
        elif self.squareId > 84 and self.squareId <= 92:
            return redSquares[self.squareId]
        elif self.squareId > 92 and self.squareId <= 100:
            return greenSquares[self.squareId]

    def _getStartCoord(self, chk, chkNum):
        if chk.getColor() == "red":
            switch = {0:(20, 435),
                      1:(180, 435),
                      2:(180, 580),
                      3:(20, 580),
                     }
        elif chk.getColor() == "green":
            switch = {0:(425, 435),
                      1:(590, 435),
                      2:(425, 580),
                      3:(590, 580),
                     }               
        elif chk.getColor() == "yellow":
            switch = {0:(425, 175),
                      1:(590, 175),
                      2:(425, 20),
                      3:(590, 20),
                     }
        elif chk.getColor() == "blue":
            switch = {0:(20, 175),
                      1:(180, 175),
                      2:(180, 20),
                      3:(20, 20),
                    }

        return switch[chkNum]

    def getCheckers(self):
        """ Get the list of checkers in this square """
        return self.checkers

    def isNormal(self):
        """ Indicate if the square is of normal type """
        return self.sType == 0

    def isSecure(self):
        """ Indicate if the square is of secure type """
        return self.sType == 1

    def isStair(self):
        """ Indicate if the square is of stair type """
        return self.sType == 2

    def isNirvana(self):
        """ Indicate if the square is of nirvana type """
        return self.sType == 3
