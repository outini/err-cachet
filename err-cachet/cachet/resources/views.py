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

from datetime import datetime
from inspect import cleandoc


COMPONENT_VIEW = """
**Component**: `%s` %s
**Status:** %s %s
**Link:** %s
**Description:** %s
_Last updated_ %s

**Active incidents:**
%s
"""


INCIDENT_VIEW = """
**Incident status:** `%s`
**Component:** %s
**Component status:** %s %s
_Created at_ `%s`
_Last updated_ `%s`
**Description:**
%s
"""


def message_header(istatus, cstatus):
    """Build message header

    :param str istatus: Incident status name
    :param str cstatus: Component status name
    :return: Message header (:class:`str`)
    """
    return "##### [%s] %s: %s" % (datetime.now(), istatus, cstatus)


def updates_separator():
    """Get incident updates separator

    :return: Incident updates separator (:class:`str`)
    """
    return "\n---"


def unknown_incident(iid):
    """Get unknown incident error message

    :param str iid: Incident ID
    :return: Error message  (:class:`str`)
    """
    return cleandoc("""
        :warning: Unknown incident number %s.
        Try `incident last` to find your incident.
    """ % iid)


def unknown_component(cid):
    """Get unknown component error message

    :param str iid: Component ID
    :return: Error message  (:class:`str`)
    """
    return cleandoc("""
        :warning: Unknown component id %s.
        Try `component list all` to find your component.
    """ % cid)