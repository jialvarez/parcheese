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
                 1: (606, 252),
                 2: (575, 252),
                 3: (548, 252),
                 4: (522, 252),
                 5: (496, 251),     # Secure
                 6: (462, 252),
                 7: (429, 251),
                 8: (403, 253),
                 9: (380, 230),
                 10: (381, 201),
                 11: (384, 172),
                 12: (385, 144),    # Secure
                 13: (386, 117), 
                 14: (387, 85), 
                 15: (383, 53), 
                 16: (385, 25), 
                 17: (313, 28),     # Secure
                 18: (262, 26), 
                 19: (257, 64), 
                 20: (256, 89),
                 21: (251, 114),
                 22: (252, 140),    # Secure
                 23: (250, 176),
                 24: (246, 199),
                 25: (251, 229),
                 26: (233, 252),
                 27: (206, 251),
                 28: (174, 250),
                 29: (149, 247),    # Secure
                 30: (116, 251), 
                 31: (88, 251), 
                 32: (57, 251), 
                 33: (29, 251), 
                 34: (26, 317),    # Secure
                 35: (27, 384), 
                 36: (58, 383), 
                 37: (86, 385),
                 38: (120, 386),
                 39: (130, 370),    # Secure
                 40: (174, 385),
                 41: (203, 388),
                 42: (231, 384),
                 43: (252, 402),
                 44: (252, 432),
                 45: (251, 454),
                 46: (251, 485),    # Secure
                 47: (248, 516),
                 48: (250, 546),
                 49: (251, 574),
                 50: (250, 598),
                 51: (319, 608),    # Secure
                 52: (386, 606),
                 53: (385, 578),
                 54: (385, 549),
                 55: (384, 517),
                 56: (370, 475),    # Secure
                 57: (381, 460),
                 58: (381, 430),
                 59: (380, 405),
                 60: (405, 376),
                 61: (432, 385),
                 62: (459, 385),
                 63: (491, 383),    # Secure
                 64: (519, 386),
                 65: (546, 383),
                 66: (578, 383),
                 67: (608, 383),
                 68: (608, 324)}    # Secure

yellowSquares = {69: (578, 319),
                 70: (548, 318),
                 71: (523, 317),
                 72: (492, 319),
                 73: (460, 319),
                 74: (435, 319),
                 75: (409, 317),
                 76: (364, 315)}    # Nirvana

blueSquares = {77: (319, 58),
               78: (321, 87),
               79: (316, 112),
               80: (319, 140),
               81: (316, 174),
               82: (319, 201),
               83: (318, 232),
               84: (316, 266)}    # Nirvana

redSquares = {85: (60, 318),
              86: (83, 315),
              87: (116, 317),
              88: (147, 316),
              89: (175, 317),
              90: (204, 319),
              91: (227, 319),
              92: (270, 318)}    # Nirvana

greenSquares = {93:  (317, 578),
                94: (316, 548),
                95: (313, 522),
                96: (316, 491),
                97: (317, 459),
                98: (318, 430),
                99: (318, 402),
               100: (318, 352)}   # Nirvana

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
