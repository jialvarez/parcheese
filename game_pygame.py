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
from src.core import dice
import pygame

from src.gui.pygame_stuff import load_image
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
        self.background = self.loadBg(os.path.join(self.image_path,
                                                    'board_640.png'))

        self.addPlayer('neonigma', 'red')
        self.addPlayer('piponazo', 'green')
        self.addPlayer('darkesa', 'yellow')
        self.addPlayer('frawny', 'blue')

        self.initGame()

        self.dice = dice.Dice()
        self.counterDC = 0

        # turn of the game: in sense of the hands of the clock
        self.players = self.getPlayers()
        self.players.reverse()

        self.drawCheckers()

    def drawCheckers(self):
        """ Draw the checkers of all players in screen """
        self.chkSprites = [] # list of sprites drawing checkers
        coordinates = [] # coordinates of square
        pyr_idx = 0 # player index

        # iterate players
        for player in self.players:
            checkers = player.getCheckers()

            # add a group of sprites (four checker of a player)
            # to the list of chkSprites
            self.chkSprites.append(pygame.sprite.Group())

            # iterate checkers for this player
            for chk in checkers:
                chkSprite = CheckerSprite(chk, self.image_path)

                # add chkSprite with image checker to current group
                self.chkSprites[pyr_idx].add(chkSprite)

            # inc player index
            pyr_idx += 1

        # iterate over sprites GROUP
        for chkSprite in self.chkSprites:
            chkCheckers = []
            zeros = 0

            # iterate checker for current group
            for checker in chkSprite:
                chk = checker.getChk()
                # don't process barriers if already did it in processBarrier
                if chk not in chkCheckers:
                    barrier = self._processBarrier(chk,
                                                   checker.getImage(),
                                                   chkCheckers,
                                                   self.chkSprites)

                # if chk wasn't processed in processBarrrier,
                # draw it separately
                if chk not in chkCheckers:
                    square = chk.getSquare()

                    # detect checkers at home, indexes changes for these,
                    # so we fix index number for each one
                    if chk.getPos() == 0:
                        coordinates = square.getCoord(chk, zeros)
                        zeros += 1
                    else:
                        coordinates = square.getCoord()

                    self.screen.blit(checker.getImage(), coordinates)
                    chk.setCoordPos(coordinates)

    def _processBarrier(self, searChk, searchChkImg, chkCheckers, chkSprites):
        normalChks = []
        schSqu = searChk.getPos()

        for chkSprite in chkSprites:
            for checker in chkSprite:
                chk = checker.getChk()
                squ = chk.getPos()

                if searChk <> chk and schSqu == squ and schSqu <> 0:
                    coordinates = chk.getSquare().getCoord(chk)

                    # get coordinates for barrier
                    coorDrawing = self._getIncDecCoord(squ, coordinates)

                    # paint two checkers of the barrier
                    self.screen.blit(checker.getImage(), coorDrawing[0])
                    self.screen.blit(searchChkImg, coorDrawing[1])

                    # update coordinates position for these checkers
                    chk.setCoordPos(coorDrawing[0])
                    searChk.setCoordPos(coorDrawing[1])

                    # don't process this checkers again
                    chkCheckers.append(chk)
                    chkCheckers.append(searChk)

                    # tell barrier detected!
                    return True

        return False

    def _getIncDecCoord(self, squPos, coordinates):
        if ((squPos >= 1 and squPos <= 8) or \
           (squPos >= 26 and squPos <= 42) or \
           (squPos >= 60 and squPos <= 76) or \
           (squPos >= 85 and squPos <= 92)):
            return [(coordinates[0], coordinates[1] - 15),
                    (coordinates[0], coordinates[1] + 15)]
        elif ((squPos >= 9 and squPos <= 25) or \
           (squPos >= 43 and squPos <= 59) or \
           (squPos >= 77 and squPos <= 84) or \
           (squPos >= 93 and squPos <= 100)):
            return [(coordinates[0] - 15, coordinates[1]),
                    (coordinates[0] + 15, coordinates[1])]

    def getScreen(self):
        return self.screen

    def addButton(self, button):
        self.buttons = self.buttons + [button]

    def run(self):
        self.loop()     # Run the event loop
        pygame.quit()   # Close the Pygame window

    def loop(self):
        self.__draw() # first time for background
        while self.going:
            self.clock.tick(120)
            for player in self.players:
                #dVal = self.dice.throwDice()
                dVal = self.throwDice()
                logging.info("%s gets %s ", player.getName(), str(dVal))

                self.manageTurn(player, dVal, None)
                self.__draw()

    def throwDice(self):
        # return self.dice.throwDice()
        
        # TEST: a checker enemy in other checker's init pos was eated
        # dices = [5, 6, 6, 4, 1, 1, 1, 1, 1, 1, 5, 3, 3, 3, 3]

        # TEST: 2 checkers in init pos, and player wants take another one out
        # dices = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]

        # TEST: selecting a checker enemy in other checker's init pos
        # dices = [5, 6, 6, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        # TEST: selecting a checker enemy in other checker's secure pos
        # dices = [6, 1, 6, 6, 4, 1, 1, 5, 6, 2, 1, 1, 1, 1]

        # TEST: selecting a checker enemy in other checker's secure pos
        # dices = [1, 5, 1, 1, 1, 2, 2, 2, 1, 5, 1, 1, 1, 3, 1, 1, 2, 5, 1, 1, 1, 6, 1, 1, 1]

        # TEST: not breaking a barrier with 5
        # dices = [1, 5, 1, 1, 1, 4, 1, 1, 1, 5, 1, 1, 1, 5, 1, 1, 1]

        # TEST: if player can not move, pass turn
        # dices = [5, 5, 1, 1, 
        #         1, 6, 6, 4, 1, 1, 
        #         5, 6, 6, 4, 1, 1, 
        #         1, 5, 1, 1, 
        #         1, 5, 1, 1,
        #         5, 5, 1, 1,
        #         1, 5, 1, 1,
        #         1, 5, 1, 1,
        #         1, 5, 1, 1,
        #         1, 5, 1, 1,
        #         1, 5, 1, 1,
        #         1, 5, 1, 1,
        #         1, 5, 1, 1]

        # TEST: if player got two barriers, take both in consideration
        # dices = [5, 5, 1, 1, 
        #         1, 6, 6, 4, 1, 1, 
        #         5, 6, 6, 4, 1, 1, 
        #         1, 5, 1, 1, 
        #         1, 5, 1, 1,
        #         5, 6, 6, 4, 1, 1,
        #         1, 6, 6, 4, 1, 1,
        #         1, 5, 1, 1,
        #         1, 5, 1, 1,
        #         1, 5, 1, 1,
        #         1, 5, 1, 1,
        #         1, 5, 1, 1,
        #         1, 5, 1, 1]

        # TEST: eat a simple checker
        # dices = [1, 6, 6, 4, 1, 1, 1, 3, 1, 1, 1]

        # TEST: eat a checker when you have more checkers in game
        # dices = [1, 5, 1, 1, 1, 6, 6, 4, 1, 1, 1, 4, 1, 1, 1, 1]

        # TEST: checking stairs and nirvana
        #dices = [1, 5, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 5,
        #               1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 6, 6, 4,
        #               1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 1,
        #               1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        # TEST: checking stairs and nirvana
        dices = [1, 5, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 5,
                       1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4,
                       1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 6, 6, 4, 1, 1, 1, 5, 1, 1, 1, 6, 6, 4,
                       1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        dVal = dices[self.counterDC]
        self.counterDC += 1
        return dVal

    def __blockUntilSelect(self, player, dVal, breakBarrier = True):
        chk = None

        if dVal == 5 and breakBarrier == True:
            for chkSprite in self.chkSprites:
                for checker in chkSprite:
                    chkSearch = checker.getChk()
                    if chkSearch.getPlayer().getName() == player.getName():
                        if chkSearch.getPos() == 0:
                            chk = chkSearch

        if chk == None:
            chk = self.__handleEvents()
        else:
            return chk # move without select (get out from home)

        while chk == False or chk.getPlayer() <> player:
            chk = self.__handleEvents()
        return chk

    def breakFiveBarrier(self, processTurn, player, chkID, dVal):
        breakBarrier = True

        if processTurn == -1:
            # recall for processing break barrier at
            # initial position with dVal = 5, sending -1
            # for advice
            checkers = player.getCheckers()

            for chk in checkers:
                chkToMove = player.checkIfHasBarrier(chk, dVal,
                                            self.getNormalSquares(),
                                            self.getStairSquares(player))
                if chk == chkToMove:
                    # this chk is not in a barrier
                    movement = player.checkIfChkCanMove(chk, dVal, 
                                             self.getNormalSquares(),
                                             self.getStairSquares(player))

                    # this chk can move, it is not necessary break barrier
                    if movement <> False:
                        breakBarrier = False

            logging.info("break barrier: %s", breakBarrier)

            if breakBarrier == True:
                processTurn = self.nextTurn(player, -1, chkID, False)
            else:
                chk = self.__blockUntilSelect(player, dVal, breakBarrier)
                chkID = chk.getID()
                logging.info("barrier in dVal: %s and chkID: %s", dVal, chkID)
                processTurn = self.nextTurn(player, -1, chkID, True)

        if processTurn <> False:
            return processTurn
        else:
            return dVal

    def breakSixBarrier(self, player, dVal, chkID):
        chkSelected = None

        if player.checkersAtHome() == False:
            if dVal == 6 or dVal == 12:
                chkSelected = player.checkIfHasBarrier(None, dVal, 
                                        self.getNormalSquares(),
                                        self.getStairSquares(player))

        if chkSelected == None:
            # wait until player select one checker
            chk = self.__blockUntilSelect(player, dVal)
        else:
            chk = chkSelected

        return chk.getID()

    def playerCanMove(self, dVal, player):
        # if player can not move, pass turn
        playerCanMove = player.checkIfPlayerCanMove(dVal, 
                                            self.getNormalSquares(),
                                            self.getStairSquares(player))

        if playerCanMove == False:
            return False
        else:
            return True

    def manageTurn(self, player, dVal, chkID):
        # if player has all checkers at home, pass turn
        if dVal <> 5 and player.getNumChksAtHome() == 4:
            return

        if self.playerCanMove(dVal, player) == False: 
            return

        chkID = self.breakSixBarrier(player, dVal, chkID)
        
        processTurn = self.nextTurn(player, dVal, chkID)

        result = self.breakFiveBarrier(processTurn, player, chkID, dVal)

        # manual select succedeed
        if result == True:
            return

        while isinstance(processTurn, int) or processTurn == False:
            if isinstance(processTurn, int):
                self.__draw()

            if processTurn == 6 or processTurn == 12:
                #processTurn = self.dice.throwDice()
                processTurn = self.throwDice()
                logging.info("%s gets %s ", player.getName(), str(processTurn))

            if processTurn == -6:
                # checker can not be moved in last turn, retry
                processTurn = 6

            if isinstance(processTurn, int):
                result = processTurn

            # if player has all checkers at home, pass turn
            if dVal <> 5 and player.getNumChksAtHome() == 4:
                return
    
            if self.playerCanMove(processTurn, player) == False:
                logging.info("%s can move with %s ", player.getName(), str(dVal))
                return

            chkID = self.breakSixBarrier(player, processTurn, chkID)

            processTurn = self.nextTurn(player, result, chkID)

            result = self.breakFiveBarrier(processTurn, player, chkID, dVal)

            # manual select succedeed
            if result == True:
                return

    def __handleEvents(self):
        """ Handle all events """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.going = False
            elif event.type == MOUSEBUTTONDOWN:
                self.__handleMouseDown(pygame.mouse.get_pos())
                if event.button == 1:
                    return self.__selectChecker(event)

        return False

    def __selectChecker(self, event):
        for chkSprite in self.chkSprites:
            for checker in chkSprite:
                chk = checker.getChk()
                square = chk.getSquare()
                #coord = square.getCoord(chk, chk.getID())
                coord = chk.getCoordPos()
                imgDim = checker.getImgDim()

                #coordSrc = (coord[0], coord[1])
                #coordTgt = (coord[0] + imgDim[0], coord[1] + imgDim[1])

                #pygame.draw.line(self.screen, (0, 0, 255), coordSrc, coordTgt)
                #pygame.display.flip()

                if coord[0] < event.pos[0] < (coord[0] + imgDim[0]):
                    if coord[1] < event.pos[1] < (coord[1] + imgDim[1]):
                        return chk
        return False

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

    def loadBg(self, filename, transparent=False):
        fullname = os.path.join('data', filename)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            raise SystemExit, message
        image = image.convert()
        if transparent:
            color = image.get_at((0, 0))
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

    def getImgDim(self):
        return (self.image_w, self.image_h)


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
