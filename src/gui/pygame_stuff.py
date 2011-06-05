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

import os
import sys
import pygame
from pygame.locals import RLEACCEL, Rect

#COLORS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 255)


def load_image(name, colorKey=None):
    # All platforms
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit(message)
    image = image.convert()
    if colorKey is not None:
        if colorKey is -1:
            colorKey = image.get_at((0, 0))
        image.set_colorkey(colorKey, RLEACCEL)
    return image, image.get_rect()


class ButtonRect:
    """Button class for add players based on the Command pattern."""

    def __init__(self, x, y, w, h, command):
        """ Constructor """
        self.rect = Rect(x, y, w, h)
        self.command = command

    def handleMouseDown(self, x, y):
        if self.rect.collidepoint(x, y):
            if self.command <> None:
                self.command.do()

    def draw(self, surface):
        # TODO : use picture here.
        # This method could also be implemented by subclasses.
        pygame.draw.rect(surface, (100, 100, 100), self.rect)


class ButtonCircle:
    """Button class for add players based on the Command pattern."""

    def __init__(self, x, y, r, command, color=(100,100,100)):
        """ Constructor """
        self.r = r
        self.rect = Rect(x-r, y-r, r*2, r*2)
        self.command = command
        self.color = color

    def handleMouseDown(self, x, y):
        if self.rect.collidepoint(x, y):
            if self.command <> None:
                self.command.do()

    def draw(self, surface):
        # TODO : use picture here.
        # This method could also be implemented by subclasses.
        pygame.draw.circle(surface, self.color, (self.rect.x, self.rect.y),
                           self.r)
