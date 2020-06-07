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
Date and time elements for the French language
============================================================================

"""

from datetime import date, time, timedelta
from ...grammar.elements  import Alternative, Compound, Choice
from ..base.integer       import Integer, IntegerRef


#---------------------------------------------------------------------------

month_names = {
               "Janvier":     1,
               "Fevrier":    2,
               "Mars":       3,
               "Avril":       4,
               "Mai":         5,
               "Juin":        6,
               "Juillet":        7,
               "Aout":      8,
               "Septembre":   9,
               "Octobre":    10,
               "Novembre":   11,
               "Decembre":   12,
              }

day_names   = {
               "Lundi":      0,
               "Mardi":     1,
               "Mercredi":   2,
               "Jeudi":    3,
               "Vendredi":      4,
               "Samedi":    5,
               "Dimanche":      6,
              }


#---------------------------------------------------------------------------

class Month(Choice):

    def __init__(self, name):
        Choice.__init__(self, name=name, choices=month_names)


class Day(Choice):

    def __init__(self, name):
        Choice.__init__(self, name=name, choices=day_names)


class Year(Alternative):

    alts = [
            IntegerRef("year", 2000, 2100),
            Compound(
                     spec="<century> <year>",
                     extras=[Integer("century", 20, 21),
                             IntegerRef("year", 10, 100)],
                     value_func=lambda n, e: e["century"] * 100 + e["year"]
                    ),
            Compound(
                     spec="<century> <year>",
                     extras=[Integer("century", 19, 20),
                             IntegerRef("year", 1, 100)],
                     value_func=lambda n, e: e["century"] * 100 + e["year"]
                    ),
           ]

    def __init__(self, name):
        Alternative.__init__(self, name=name, children=self.alts)


#---------------------------------------------------------------------------

class AbsoluteDate(Compound):

    spec = "(<day> <month> | <month> <day>) [<year>]"
    extras = [IntegerRef("day", 1, 32), Month("month"), Year("year")]

    def __init__(self, name):
        Compound.__init__(self, name=name, spec=self.spec,
                          extras=self.extras)

    def value(self, node):
        month      = node.get_child_by_name("month").value()
        day        = node.get_child_by_name("day").value()
        year_node  = node.get_child_by_name("year")
        if year_node is None:
            today = date.today()
            year = today.year
            if month - today.month > 6:
                # More than six months in the future, use last year.
                year -= 1
            elif month - today.month < -6:
                # More than six months in the past, use next year.
                year += 1
        else:
            year = year_node.value()
        return date(year, month, day)


class RelativeDate(Alternative):

    class _DayOffset(Choice):
        def __init__(self):
            choices = {
                       "il y a <n> jours": -1,
                       "hier":    -1,
                       "aujourd'hui":         0,
                       "demain":     +1,
                       "dans <n> jours":  +1,
                      }
            extras = [IntegerRef("n", 1, 100)]
            Choice.__init__(self, name=None, choices=choices, extras=extras)

        def value(self, node):
            value = Choice.value(self, node)
            n = node.get_child_by_name("n")
            print("November:", n)
            if n is not None:
                value = value * n.value()
            return date.today() + timedelta(days=value)

    class _WeekdayOffset(Choice):
        def __init__(self):
            choices = {
                       "<day> dernier":  "last day",
                       "(ce | prochain) <day>":  "next day",
                       "<day> de la semaine dernière":      "last week",
                       "<day> de la semaine prochaine":      "next week",
                      }
            extras = [Day("day")]
            Choice.__init__(self, name=None, choices=choices, extras=extras)

        def value(self, node):
            value = Choice.value(self, node)
            day = node.get_child_by_name("day").value()
            now = date.today().weekday()
            print(value, day, now)
            if value == "last day":
                if day < now:  day_offset = -now + day
                else:          day_offset = -7 - now + day
            elif value == "next day":
                if day < now:  day_offset = 7 - now + day
                else:          day_offset = day - now
            elif value == "last week":
                day_offset = -now - 7 + day
            elif value == "next week":
                day_offset = -now + 7 + day
            return date.today() + timedelta(days=day_offset)

    alts = [
            _DayOffset(),
            _WeekdayOffset(),
           ]

    def __init__(self, name):
        Alternative.__init__(self, name=name, children=self.alts)


class Date(Alternative):

    alts = [
            AbsoluteDate(None),
            RelativeDate(None),
           ]

    def __init__(self, name):
        Alternative.__init__(self, name=name, children=self.alts)


#---------------------------------------------------------------------------

class MilitaryTime(Compound):

    spec = "<hour> (cenq | zero <min_1_10> | <min_10_60>)"
    extras = [
              Integer("hour", 0, 25),
              IntegerRef("min_1_10", 1, 10),
              IntegerRef("min_10_60", 10, 60),
             ]

    def __init__(self, name):
        Compound.__init__(self, name=name, spec=self.spec,
                          extras=self.extras)

    def value(self, node):
        hour = node.get_child_by_name("hour").value()
        if node.has_child_with_name("min_1_10"):
            minute = node.get_child_by_name("min_1_10").value()
        elif node.has_child_with_name("min_10_60"):
            minute = node.get_child_by_name("min_10_60").value()
        else:
            minute = 0
        return time(hour, minute)


class Time(Alternative):

    alts = [
            MilitaryTime(None),
           ]

    def __init__(self, name):
        Alternative.__init__(self, name=name, children=self.alts)

#---------------------------------------------------------------------------

