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

class Square:

    def __init__(self, squareId, position, secure):
        self.squareId = squareId
        self.position = position
        self.checkerQty = 0
        self.locked = False
        self.checkers = [] 
        self.isSecure = secure

    def setLocked(self):
        self.locked = not self.locked

    def setCheckerQty(self):
        seld.checkerQty = len(self.checkers)

    def addChecker(self, checker):
        self.checkers.append(checker)

    def getSquareId(self):
        return self.squareId

    def getPosition(self):
        return self.position

    def getCheckers(self):
        return self.checkers
