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

class Player:

    def __init__(self, login, color):
        self.login = login

        # list comprehension for getting the checkers list
        self.checkers = [checker.Checker(color) for chk in range(4)]
        print self.checkers

    def getPlayerLogin(self):
        return self.login

    def getPlayerCheckers(self):
        return self.checkers
            
    def move(self, checkerId, result):
        checkerToMove = self.checkers[checkerId]

        print "Moving " + str(checkerToMove.getColor()) + \
              " checker: " + str(checkerToMove)

        checkerToMove.move(result)

        print "Moved " + str(checkerToMove) + \
              " " + str(checkerToMove.getColor()) + \
              " to position " + str(checkerToMove.getPosition())


