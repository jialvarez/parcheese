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

class Checker:
    """ Class that represents the checker in game """

    def __init__(self, color):
        self.color = color

        if color == 'yellow':
            self.initialPosition = 5
            self.lastPosition = 68
        elif color == 'blue':
            self.initialPosition = 22
            self.lastPosition = 17
        elif color == 'red':
            self.initialPosition = 39
            self.lastPosition = 34
        elif color == 'green':
            self.initialPosition = 56
            self.lastPosition = 51

        self.currentPosition = 0

        self.atHome = False

        self.isInNirvana = False

    def isEnteringAtHome(self, newPosition):
        if self.color is not 'yellow':
            if newPosition > self.lastPosition and \
                    newPosition < self.initialPosition:
                        return True
        elif self.color is 'yellow' and newPosition > 68:
            return True

        return False
    
    def getColor(self):
        return self.color

    def move(self, result, passSixtyEight=False):
        if self.color is not 'yellow' and passSixtyEight is True:
                    self.currentPosition = result
        elif self.atHome == False:
            self.currentPosition = self.currentPosition + result
        else:
            self.currentPosition = result

    def getPosition(self):
        return self.currentPosition

    def getInitialPosition(self):
        return self.initialPosition

    def getLastPosition(self):
        return self.lastPosition

    def isAtHome(self):
        return self.atHome

    def setAtHome(self):
        self.atHome = True

    def inNirvana(self):
        return self.isInNirvana

    def setInNirvana(self):
        self.isInNirvana = True
