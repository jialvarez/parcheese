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

import table
import player

class Game:

    def __init__(self):
        # here comes pygame window, config rules, etc...
        self.players = [player.Player('neonigma', 'yellow')]
        self.gameTable = table.Table(self.players)

    def getPlayer(self, playerIndex):
        return self.players[playerIndex]
   
    def getGameTable(self):
        return self.gameTable


# TESTING!
startGame = Game()
myGameTable = startGame.getGameTable()

# Testing players. This must be done with pygame and using mouse.
# Example: moves player 0, checker 0
myGameTable.playerMoves(startGame.getPlayer(0), 0)

# New movement for player 0, checker 0
myGameTable.playerMoves(startGame.getPlayer(0), 0)

