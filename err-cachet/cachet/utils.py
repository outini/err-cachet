#
#    ErrBot plugin for Cachet (err-cachet)
#
#    Copyright (C) 2017 Denis Pompilio (jawa) <denis.pompilio@gmail.com>
#
#    This file is part of err-cachet
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, see <http://www.gnu.org/licenses/>.

import re
from datetime import datetime


def pmatch(word, min_chars=4):
    """Return regexp to match first letters of a word

    Example with the word "components":
      comp(?:o(?:n(?:e(?:n(?:t(?:s)?)?)?)?)?)?
    """
    regex = word[0:min_chars]
    word_len = len(word)
    for char in word[min_chars:]:
        regex += "(?:" + char
    regex += ")?" * (word_len - min_chars)
    return regex


DATE_RE = r'(\d{4})-(\d\d)-(\d\d)'
TIME_RE = r'(\d\d):(\d\d)(?::(\d\d)(?:Z|[+-]\d\d:\d\d)?)?'
DATETIME_RE = r'^%s(?:[ T]%s)?$' % (DATE_RE, TIME_RE)

CACHET_INCIDENT_STATUS = {
    re.compile(pmatch("investigating", 3),
               re.IGNORECASE): (1, "Investigating"),
    re.compile(pmatch("identified", 2),
               re.IGNORECASE): (2, "Identified"),
    re.compile(pmatch("watching", 2),
               re.IGNORECASE): (3, "Watching"),
    re.compile(pmatch("fixed", 3),
               re.IGNORECASE): (4, "Fixed")
}

CACHET_COMPONENT_STATUS = {
    re.compile(r'^(green|op|operational)$',
               re.IGNORECASE): (1, "Operational"),
    re.compile(r'^(blue|pi|Performance ?Issue)$',
               re.IGNORECASE): (2, "Performance Issue"),
    re.compile(r'^(orange|po|Partial ?Outage)$',
               re.IGNORECASE): (3, "Partial Outage"),
    re.compile(r'^(red|mo|Major ?Outage)$',
               re.IGNORECASE): (4, "Major Outage")
}

# Icons by component status
ICONS = [
    '',
    ':ok:',
    ':warning:',
    ':warning:',
    ':interrobang:'
]

# Colors by component status
COLORS = [
    '#59afe1',
    '#59afe1',
    '#e27209',
    '#e27209',
    '#b52127'
]


def get_istatus(istatus):
    """Return incident status info

    :param cstatus: Component status alias
    :return: :func:`tuple` (status (:func:`int`), name (:func:`str`))
             or :obj:`None`
    """
    for regex, numeric_status in CACHET_INCIDENT_STATUS.items():
        if regex.search(istatus):
            return numeric_status
    return None


def get_cstatus(cstatus):
    """Return component status info

    :param cstatus: Component status alias
    :return: :func:`tuple` (status (:func:`int`), name (:func:`str`))
             or :obj:`None`
    """
    for regex, numeric_status in CACHET_COMPONENT_STATUS.items():
        if regex.search(cstatus):
            return numeric_status
    return None
