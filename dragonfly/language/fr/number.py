#
# This file is part of Dragonfly.
# (c) Copyright 2007, 2008 by Christo Butcher
# Licensed under the LGPL.
#
#   Dragonfly is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Dragonfly is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with Dragonfly.  If not, see
#   <http://www.gnu.org/licenses/>.
#

"""
French language implementations of Integer and Digits classes
============================================================================

"""

from ..base.integer_internal  import (MapIntBuilder, CollectionIntBuilder,
                                      MagnitudeIntBuilder, IntegerContentBase)
from ..base.digits_internal   import DigitsContentBase


#---------------------------------------------------------------------------

int_0           = MapIntBuilder({
                                 "zero":         0,
                               })
int_1_9         = MapIntBuilder({
                                 "un":                 1,
                                 "deux":    2,
                                 "trois":               3,
                                 "quatre":                4,
                                 "cinq":                5,
                                 "six":                 6,
                                 "sept":               7,
                                 "huit":               8,
                                 "neuf":                9,
                               })
int_10_19       = MapIntBuilder({
                                 "dix":       10,
                                 "onze":    11,
                                 "douze":    12,
                                 "treize":  13,
                                 "quatorze":  14,
                                 "quinze":   15,
                                 "seize":   16,
                                 "dix sept": 17,
                                 "dix huit":  18,
                                 "dix neuf":  19,
                               })
int_20_90_10    = MapIntBuilder({
                                 "vingt":     2,
                                 "trente":     3,
                                 "quarante":      4,
                                 "cinquante":      5,
                                 "soixante":      6,
                                 "soixante dix":    7,
                                 "quatre vingt":     8,
                                 "quatre vingt":     9,
                               })
int_20_99       = MagnitudeIntBuilder(
                   factor      = 10,
                   spec        = "<multiplier> [<remainder>]",
                   multipliers = [int_20_90_10],
                   remainders  = [int_1_9],
                  )
int_and_1_99    = CollectionIntBuilder(
                   spec        = "[et] <element>",
                   set         = [int_1_9, int_10_19, int_20_99],
                  )
int_100s        = MagnitudeIntBuilder(
                   factor      = 100,
                   spec        = "[<multiplier>] cent [<remainder>]",
                   multipliers = [int_1_9],
                   remainders  = [int_and_1_99],
                  )
int_100big      = MagnitudeIntBuilder(
                   factor      = 100,
                   spec        = "[<multiplier>] cent [<remainder>]",
                   multipliers = [int_10_19, int_20_99],
                   remainders  = [int_and_1_99]
                  )
int_1000s       = MagnitudeIntBuilder(
                   factor      = 1000,
                   spec        = "[<multiplier>] mille [<remainder>]",
                   multipliers = [int_1_9, int_10_19, int_20_99, int_100s],
                   remainders  = [int_and_1_99, int_100s]
                  )
int_1000000s    = MagnitudeIntBuilder(
                   factor      = 1000000,
                   spec        = "[<multiplier>] million [<remainder>]",
                   multipliers = [int_1_9, int_10_19, int_20_99, int_100s, int_1000s],
                   remainders  = [int_and_1_99, int_100s, int_1000s],
                  )


#---------------------------------------------------------------------------

class IntegerContent(IntegerContentBase):
    builders = [int_0, int_1_9, int_10_19, int_20_99,
                int_100s, int_100big, int_1000s, int_1000000s]

class DigitsContent(DigitsContentBase):
    digits = ["zero", "un", "deux", "trois",
              "quatre", "cinq", "six", "sept", "huit", "neuf"]
