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
Characters in text symbols for the French language.
============================================================================

"""

from ...grammar.elements   import (Choice, RuleRef, Repetition, Sequence,
                                   Alternative, Optional, Compound)
from ...grammar.rule_base  import Rule


#---------------------------------------------------------------------------
# Letter names.

letter_names = {
                "Alpha":     "a",
                "Bravo":     "b",
                "Charlie":   "c",
                "Delta":     "d",
                "Echo":      "e",
                "Foxtrot":   "f",
                "Golf":      "g",
                "Hotel":     "h",
                "India":     "i",
                "Juliett":   "j",
                "Kilo":      "k",
                "Lima":      "l",
                "Mike":      "m",
                "November":  "n",
                "Oscar":     "o",
                "Papa":      "p",
                "Quebec":    "q",
                "Romeo":     "r",
                "Sierra":    "s",
                "Tango":     "t",
                "Uniform":   "u",
                "Victor":    "v",
                "Whiskey":   "w",
                "X-ray":     "x",
                "Yankee":    "y",
                "Zulu":      "z",
               }
uppercase_prefix = "Majuscule"

lowercase_letter_names = letter_names
uppercase_letter_names = dict((name, char.upper())
                              for (name, char) in list(letter_names.items()))


#---------------------------------------------------------------------------
# Digit names.

digit_names = {
               "Zero":    "0",
               "Un":     "1",
               "Deux":     "2",
               "Trois":   "3",
               "Quatre":    "4",
               "Cinq":    "5",
               "Six":     "6",
               "Sept":   "7",
               "Huit":   "8",
               "Neuf":    "9",
              }


#---------------------------------------------------------------------------
# Symbol names.

symbol_names = {
                "Entrée":                                                "\n",
                "(Tab | Tabulation)":                                    "\t",
                "Espace":                                                " ",
                "Point Exclamation":                                     "!",
                "At | Arobase":                                          "@",
                "(Croisillon | Diese)":                                  "#",
                "Dollar":                                                "$",
                "(Pourcent | Pour cent)":                                "%",
                "[accent] circonflexe)":                                 "^",
                "Esperluette":                                           "&",
                "(Asterisk | Etoille)":                                  "*",
                "(Paren | Parenthèse) (Gauche | Ouvrante)":              "(",
                "(Paren | Parenthèse) (Droite | Fermante) ":             ")",
                "[Signe] Moins":                                         "-",
                "(Underscore | Tiret du bas)":                           "_",
                "[Signe] Egale":                                         "=",
                "[Signe] Plus":                                          "+",
                "tick":                                                  "`",
                "Tilde":                                                 "~",
                "Crochet (Gauche | Ouvrante)":                           "[",
                "Crochet (Droite | Fermante)":                           "]",
                "Accolade (Gauche | Ouvrante)":                          "{",
                "Accolade (Droite | Fermante)":                          "}",
                "Backslash":                                            "\\",
                "Barre [Verticale]":                                     "|",
                "Deux Points":                                           ":",
                "Apostrophe":                                            "'",
                "Citation":                                              '"',
                "Virgule":                                               ",",
                "Point":                                                 ".",
                "Slash":                                                 "/",
                "Inférieur a":                                           "<",
                "Suppérieur a":                                          ">",
                "Point Interrogation":                                   "?",
               }


#---------------------------------------------------------------------------
# Aggregation of all char names.

char_names = dict(lowercase_letter_names)
char_names.update(digit_names)
char_names.update(symbol_names)


#---------------------------------------------------------------------------
# Helper functions to create special element classes.

class CharChoice(RuleRef):

    def __init__(self, name=None):
        letter_element = Sequence([
                  Optional(Compound(uppercase_prefix, name="upper")),
                  Choice("letter", letter_names),
                ])
        other_choices = {}
        other_choices.update(digit_names)
        other_choices.update(symbol_names)
        other_element = Choice(name="other", choices=other_choices)

        root_element = Alternative([letter_element, other_element])
        root_rule = Rule(element=root_element)
        RuleRef.__init__(self, name=name, rule=root_rule)

    def value(self, node):
        child = node.get_child_by_name("letter")
        if child:
            value = child.value()
            if node.has_child_with_name("upper"):
                value = value.upper()
            return value
        child = node.get_child_by_name("other")
        return child.value()


#---------------------------------------------------------------------------
# Helper functions to create special element classes.

def choice_wrap_class(choices):
    class _ChoiceWrapClass(RuleRef):
        _choices = choices
        def __init__(self, name=None):
            choice_element = Choice(name=None, choices=self._choices)
            choice_rule = Rule(element=choice_element)
            RuleRef.__init__(self, name=name, rule=choice_rule)
    return _ChoiceWrapClass

def choice_series_wrap_class(choices):
    class _ChoiceWrapClass(RuleRef):
        _choices = choices
        def __init__(self, name=None, min=1, max=8):
            choice_element   = Choice(name=None, choices=self._choices)
            choice_rule      = Rule(element=choice_element)
            choice_ref       = RuleRef(rule=choice_rule)
            series_element   = Repetition(child=choice_ref, min=min, max=max)
            series_rule      = Rule(element=series_element)
            RuleRef.__init__(self, name=name, rule=series_rule)
        def value(self, node):
            child_values = RuleRef.value(self, node)
            return "".join(child_values)
    return _ChoiceWrapClass

def element_series_wrap_class(element):
    class _ChoiceWrapClass(RuleRef):
        _element = element
        def __init__(self, name=None, min=1, max=8):
            series_element   = Repetition(child=self._element, min=min, max=max)
            series_rule      = Rule(element=series_element)
            RuleRef.__init__(self, name=name, rule=series_rule)
        def value(self, node):
            child_values = RuleRef.value(self, node)
            return "".join(child_values)
    return _ChoiceWrapClass


#---------------------------------------------------------------------------
# High-level, easy-to-use element classes.

LetterChoice  = choice_wrap_class(lowercase_letter_names)
LetterSeries  = choice_series_wrap_class(lowercase_letter_names)
#CharChoice    = choice_wrap_class(char_names)
#CharSeries    = choice_series_wrap_class(char_names)
CharSeries    = element_series_wrap_class(CharChoice())
