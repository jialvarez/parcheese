#!/usr/bin/env python
# Parcheese
#
# Copyright 2011 Parcheese Team.
# Author: J. Ignacio Alvarez <neonigma@gmail.com>
# Author: Edorta Garcia Gonzalez <edortagarcia@gmail.com>
# Author: Luis Diaz Mas <piponazo@gmail.com>
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
import sys

from src.core import game

def main():
    ''' Main function for parcheese game in console mode '''

    logging.basicConfig(level=logging.DEBUG)
    myGame = game.Game()
    myGame.addPlayer('neonigma', 'green')
    myGame.addPlayer('piponazo', 'blue')

    # Testing players. This must be done with pygame and using mouse.
    # This loop is activated when the game starts
    myGame.start()
    end = False
    while not end:
        myGame.nextTurn()

if __name__ == '__main__':
    main()
