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

import logging
import table
from player import Player


class Game:

    def __init__(self):
        """ Constructor.
        Here comes pygame window, config rules, etc...
        """

        self.players = []   # List of players
        self.turn = -1
        self.playing = False

    def addPlayer(self, name, color):
        ''' Add a new player to the game '''
        logging.info("New player [%s, %s]", name, color)
        self.players.append(Player(name, color))

    def delPlayer(self, idx):
        ''' Remove a player by its index in the list '''
        self.players[idx:idx + 1] = []

    def getPlayer(self, idx):
        ''' Return instance of player by index in the list '''
        return self.players[idx]

    def nextPlayer(self):
        ''' Return the player which plays the next turn '''
        self.turn += 1
        if self.turn  >= len(self.players):
            self.turn = 0
        return self.players[self.turn]

    def start(self):
        ''' Once the game is started some operations are blocked '''
        if self.playing == False:
            self.playing = True
            myTable = table.Table(self.players)
            end = True
            while end:
                myTable.turn(self.nextPlayer())
        else:
            # TODO : Ask user if he want to restart the game
            restart = True # Temporal
#            if restart:
                # TODO : Reset the game


def main():
    ''' Main function '''

    logging.basicConfig(level=logging.DEBUG)

    myGame = Game()
    myGame.addPlayer('neonigma', 'green')
    myGame.addPlayer('piponazo', 'blue')

    # Testing players. This must be done with pygame and using mouse.
    # This loop is activated when the game starts
    myGame.start()

if __name__ == '__main__':
    main()
