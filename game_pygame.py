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
sys.path.append('src/core')
sys.path.append('src/gui')

import game
import table
import player
import pygame
from pygame_stuff import load_image, ButtonRect, ButtonCircle
from pygame.locals import *


class ParcheeseUI(game.Game):
    """ Main class """

    def __init__(self):
        """ Initialize game """

        pygame.init()
        pygame.display.set_caption('Parcheese')
        self.screen = pygame.display.set_mode((640, 640))
        self.clock = pygame.time.Clock()
        self.going = True
        pygame.mouse.set_visible(1)
        self.buttons = []

        #Create The Background
        self.background, self.rect = load_image('board_640.png', -1)

        #Create buttons for adding players
        self.addButton(ButtonRect(76, 448, 85, 20,
                       AddPlayerC(self, "pipo", "red")))
        self.addButton(ButtonRect(480, 448, 85, 20,
                       AddPlayerC(self, "neo", "green")))

        #Create button for starting game
        self.addButton(ButtonCircle(350, 350, 30, StartGameC(self)))

    def addButton(self, button):
        self.buttons = self.buttons + [button]

    def run(self):
        self.loop()     # Run the event loop
        pygame.quit()   # Close the Pygame window

    def loop(self):
        while self.going:
            self.clock.tick(60)
            self.__handleEvents()
            self.__draw()

    def __handleEvents(self):
        """ Handle all events """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.going = False
            elif event.type == MOUSEBUTTONDOWN:
                self.__handleMouseDown(pygame.mouse.get_pos())

    def __handleMouseDown(self, (x, y)):
        for button in self.buttons:
            button.handleMouseDown(x, y)

    def __draw(self):
        """ Draw graphics """
        self.screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw(self.screen)
        # update if we want to repaint known areas
        pygame.display.flip()

    def initGame(self):
        """ Initialize the game """
        self.start()
        self.buttons = []


class AddPlayerC:
    """ Command for add players """

    def __init__(self, app, name, color):
        self.app = app
        self.name = name
        self.color = color

    def do(self):
        self.app.addPlayer(self.name, self.color)


class StartGameC:
    """ Command for starting game """

    def __init__(self, app):
        self.app = app

    def do(self):
        self.app.initGame()


def main():
    ''' Main function '''

    logging.basicConfig(level=logging.DEBUG)
    ParcheeseUI().run()

if __name__ == '__main__':
    main()
