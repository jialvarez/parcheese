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

# The table/squares mapping with coordinates for each square
tableSquares = {0: (0,0),     # HOME
                 1: (597, 238),
                 2: (567, 238),
                 3: (537, 238),
                 4: (507, 238),
                 5: (480, 238),     # Secure
                 6: (450, 238),
                 7: (420, 238),
                 8: (390, 238),
                 9: (372, 220),
                 10: (372, 190),
                 11: (372, 160),
                 12: (372, 130),    # Secure
                 13: (372, 100), 
                 14: (372, 70), 
                 15: (372, 40), 
                 16: (372, 15), 
                 17: (305, 15),     # Secure
                 18: (237, 15), 
                 19: (237, 42), 
                 20: (237, 72),
                 21: (237, 102),
                 22: (237, 132),    # Secure
                 23: (237, 162),
                 24: (237, 192),
                 25: (237, 222),
                 26: (223, 238),
                 27: (193, 238),
                 28: (163, 238),
                 29: (133, 238),    # Secure
                 30: (103, 238), 
                 31: (73, 238), 
                 32: (43, 238), 
                 33: (15, 238), 
                 34: (15, 304),    # Secure
                 35: (15, 370), 
                 36: (40, 370), 
                 37: (70, 370),
                 38: (100, 370),
                 39: (130, 370),    # Secure
                 40: (160, 370),
                 41: (190, 370),
                 42: (220, 370),
                 43: (237, 388),
                 44: (237, 418),
                 45: (237, 448),
                 46: (237, 478),    # Secure
                 47: (237, 508),
                 48: (237, 538),
                 49: (237, 568),
                 50: (235, 595),
                 51: (305, 595),    # Secure
                 52: (372, 595),
                 53: (372, 568),
                 54: (372, 538),
                 55: (372, 508),
                 56: (372, 478),    # Secure
                 57: (372, 448),
                 58: (372, 418),
                 59: (372, 388),
                 60: (390, 370),
                 61: (420, 370),
                 62: (450, 370),
                 63: (480, 370),    # Secure
                 64: (510, 370),
                 65: (540, 370),
                 66: (570, 370),
                 67: (596, 370),
                 68: (596, 305)}    # Secure

yellowSquares = {69: (570, 304),
                 70: (540, 304),
                 71: (510, 304),
                 72: (480, 304),
                 73: (450, 304),
                 74: (420, 304),
                 75: (390, 304),
                 76: (360, 304)}    # Nirvana

blueSquares = {77: (304, 40),
               78: (304, 70),
               79: (304, 100),
               80: (304, 130),
               81: (304, 160),
               82: (304, 190),
               83: (304, 220),
               84: (304, 266)}    # Nirvana

redSquares = {85: (40, 304),
              86: (70, 304),
              87: (100, 304),
              88: (130, 304),
              89: (160, 304),
              90: (190, 304),
              91: (220, 304),
              92: (250, 304)}    # Nirvana

greenSquares = {93: (304, 568),
                94: (304, 538),
                95: (304, 508),
                96: (304, 478),
                97: (304, 448),
                98: (304, 418),
                99: (304, 388),
               100: (304, 358)}   # Nirvana

# Square ranges
normalSR = range(0, 69)
yStairsSR = range(69, 77)
bStairsSR = range(77, 85)
rStairsSR = range(85, 93)
gStairsSQ = range(93, 101)

# Secures
securesSQ = [5, 12, 17, 22, 29, 34, 39, 46, 51, 56, 63, 68]

# Nirvanas
nirvanasSQ = [76, 84, 92, 100]
