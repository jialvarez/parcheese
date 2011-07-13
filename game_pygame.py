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
import os

from src.core import game
from src.core import table
from src.core import player
import pygame

from src.gui.pygame_stuff import load_image, ButtonRect, ButtonCircle
from pygame.locals import *
from pygame.sprite import Sprite


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
        self.image_path = os.getcwd()
        self.image_path = os.path.join(self.image_path, 'data')

        #Create The Background
        self.background = self.load_bg(os.path.join(self.image_path,
                                                    'board_640.png'))

        self.addPlayer('neonigma', 'red')
        self.addPlayer('piponazo', 'green')

        self.initGame()

        self.players = self.getPlayers()

        self.drawCheckers()

        #Create buttons for adding players
        #self.addButton(ButtonRect(76, 448, 85, 20,
        #               AddPlayerC(self, "pipo", "red")))
        #self.addButton(ButtonRect(480, 448, 85, 20,
        #               AddPlayerC(self, "neo", "green")))

        #Create button for starting game
        #self.addButton(ButtonCircle(350, 350, 30, StartGameC(self)))


    def drawCheckers(self):
        """ Draw the checkers of all players in screen """
        chkSprites = [] # list of sprites drawing checkers
        coordinates = [] # coordinates of square
        pyr_idx = 0 # player index

        # iterate players
        for player in self.players:
            idx = 0
            checkers = player.getCheckers()

            # add a group of sprites (four checker of a player)
            # to the list of chkSprites
            chkSprites.append(pygame.sprite.Group())

            # iterate checkers for this player
            for chk in checkers:
                chkSprite = CheckerSprite(chk, self.image_path)

                # add chkSprite with image checker to current group
                chkSprites[pyr_idx].add(chkSprite)

                # get square where this checker is placed
                square = chk.getSquare()

                # get coordinates for this square
                coordinates.append(square.getCoord(chk, idx))

                # inc square list coordinates
                idx += 1

            # inc player index
            pyr_idx += 1

            # reset index
            idx = 0

        # iterate over sprites GROUP
        for chkSprite in chkSprites:
            # iterate checker for current group
            for checker in chkSprite:
                chk = checker.getChk()
                # paint checker in coordinates
                self.screen.blit(checker.getImage(), coordinates[idx])
                idx += 1

    def getScreen(self):
        return self.screen

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
            #self.nextTurn()

    def __handleEvents(self):
        """ Handle all events """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.going = False
            elif event.type == MOUSEBUTTONDOWN:
                print pygame.mouse.get_pos()
                self.__handleMouseDown(pygame.mouse.get_pos())

    def __handleMouseDown(self, (x, y)):
        for button in self.buttons:
            button.handleMouseDown(x, y)

    def __draw(self):
        """ Draw graphics """
        self.screen.blit(self.background, (0, 0))
        #for button in self.buttons:
            #button.draw(self.screen)
        self.drawCheckers()
                    
        # update if we want to repaint known areas
        pygame.display.flip()

    def initGame(self):
        """ Initialize the game """
        self.start()
        self.buttons = []

    def load_bg(self, filename, transparent=False):
        fullname = os.path.join('data', filename)
        try: 
            image = pygame.image.load(fullname)
        except pygame.error, message:
            raise SystemExit, message
        image = image.convert()
        if transparent:
            color = image.get_at((0,0))
            image.set_colorkey(color, RLEACCEL)
        return image

class CheckerSprite(Sprite):

    def __init__(self, checker, image_path):
        """ Constructor.

        Keyword arguments:
        player : The player that have this checker.
        """
        Sprite.__init__(self)
        self.checker = checker
        self.image_path = image_path

        #box_list = Box(3)
        #self.start = box_list.get_box_pos()

        chkColor = self.checker.getPlayer().getColor()
        self.image, self.rect = self.loadImgame(os.path.join(self.image_path, 
                                                chkColor + "_checker.png"), 
                                                True)
        self.image, self.rect = pygame.transform.scale(self.image, (30, 30)),\
                                                        self.rect
        self.rect = self.image.get_rect()
        #self.pos_x = self.start[0]
        #self.pos_y = self.start[1]
        #self.checker_pos = (self.pos_x, self.pos_y)
        self.image_w, self.image_h = self.image.get_size()
        self.rect.centerx = 800 / 2
        self.rect.centery = 800 / 2

    def loadImgame(self, name, get_alpha):
        """ Load image and return image object"""
        try:
            image = pygame.image.load(name)
            if image.get_alpha is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pygame.error, message:
            print 'Cannot load image:', name
        else:
            return image, image.get_rect()

    def getImage(self):
        return self.image

    def getChk(self):
        return self.checker

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
