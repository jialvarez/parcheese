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


class Player:

    def __init__(self, login, color):
        # login of player
        self.login = login

        # list comprehension for getting the checkers list
        self.checkers = [Checker(color) for chk in range(4)]
        print self.checkers

        # when throw dice, times that player has obtained 6 as result
        # consecutively
        self.resWasSix = 0

    def getResWasSix(self):
        return self.resWasSix

    def setResWasSix(self, reinitialize=False):
        ''' Set "resWasSix". You can increment or reinitialize it (call the \
                function sending to it the "reinitilize" parametre '''
        # if the function receive reinitilize=True, resWasSix is reinitialized
        if reinitialize == True:
            self.resWasSix = 0
        else: #if not, resWasSix is incremented
            self.resWasSix = self.resWasSix + 1

    def getLogin(self):
        return self.login

    def getCheckers(self):
        return self.checkers

    def getChecker(self, checkerId):
        return self.checkers[checkerId]

    def getInitialCheckerPosition(self):
        return self.checkers[0].getInitialPosition()

    def getLastCheckerPosition(self):
        return self.checkers[0].getLastPosition()

    def move(self, checkerToMove, result, passSixtyEight=False):

        print "Moving " + str(checkerToMove.getColor()) + \
              " checker: " + str(checkerToMove)

        checkerToMove.move(result, passSixtyEight)

        print "Moved " + str(checkerToMove) + \
              " " + str(checkerToMove.getColor()) + \
              " to position " + str(checkerToMove.getPosition())

        return checkerToMove.getPosition()
