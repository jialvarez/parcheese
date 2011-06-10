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
    """ Class that represents a checker of a player.

    The checkers doesn't contain the color value because of their owner also
    contains this value and it would be redundant.
    """

    def __init__(self, player, square, atHome):
        """ Constructor.

        Keyword arguments:
        player : The player that have this checker.
        """
        self.inStairs = False       # In stairs ?
        self.isInNirvana = False    # In nirvana ?
        self.player = player        # Ref to player
        self.square = square        # Ref to square

    def getPos(self):
        """ Return the position of checker """
        return self.square.getID()

    def isInStairs(self):
        """ Indicate if the checker is in the stairs """
        return self.inStairs

    def setInStairs(self):
        """ Set the checker in the stairs """
        self.inStairs = True

    def inNirvana(self):
        """ Indicate if the checker is in the nirvana """
        return self.isInNirvana

    def setInNirvana(self):
        """ Set the checker in the stairs """
        self.isInNirvana = True

    def getPlayer(self):
        """ Return the player that owns this checker """
        return self.player

    def setSquare(self, square):
        """ Assign the reference to the square where the checker is """
        self.square = square

    def getSquare(self):
        """ Return the reference to the square where the checker is """
        return self.square
