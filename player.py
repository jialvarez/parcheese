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

import checker
import square

class Player:

    def __init__(self, login, color):
        # login of player
        self.login = login

        # list comprehension for getting the checkers list
        self.checkers = [checker.Checker(color) for chk in range(4)]
        print self.checkers

        #when throw dice, times that six is obtained as result consecutively
        self.reswassix = 0

    def getResWasSix(self):
        return self.reswassix

    def setResWasSix(self):
        self.reswassix = self.reswassix + 1

    def getLogin(self):
        return self.login

    def getCheckers(self):
        return self.checkers

    def getChecker(self, checkerId):
        return self.checkers[checkerId]

    def getLastCheckerPosition(self):
        return self.checkers[0].getLastPosition()

    def move(self, checkerToMove, result):

        print "Moving " + str(checkerToMove.getColor()) + \
              " checker: " + str(checkerToMove)

        checkerToMove.move(result)

        print "Moved " + str(checkerToMove) + \
              " " + str(checkerToMove.getColor()) + \
              " to position " + str(checkerToMove.getPosition())

        return checkerToMove.getPosition()
