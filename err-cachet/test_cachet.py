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

import os

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = '.'

# See also:
# http://errbot.io/en/latest/user_guide/plugin_development/testing.html

ONLY_ENDPOINT = {'api_endpoint': "XXXXXXXXXXXXXXXX"}
ONLY_TOKEN = {'api_token': "XXXXXXXXXXXXXXXXXXXXX"}
CONFIG = {'api_endpoint': 'https://status/api/v1',
          'api_token': 'XXXXXXXXXXXXXXXXXXXXX'}


def test_cachet_plugin_configuration(testbot):
    """Test the cachet_plugin_configuration command"""
    testbot.push_message('!plugin config Cachet %s' % str(ONLY_ENDPOINT))
    assert 'api_token must be specified.' in testbot.pop_message()
    testbot.push_message('!plugin config Cachet %s' % str(ONLY_TOKEN))
    assert 'api_endpoint must be specified.' in testbot.pop_message()
    testbot.push_message('!plugin config Cachet %s' % str(CONFIG))
    assert 'Plugin configuration done.' in testbot.pop_message()


def test_cachet_plugin_version(testbot):
    """Test the cachet_plugin_version command"""
    testbot.push_message('!cachet plugin version')
    assert "Cachet plugin version:" in testbot.pop_message()


def test_cachet_comp_status(testbot):
    """Test the cachet_comp_status command"""
    testbot.push_message('!cachet comp status')
    assert "Components problems:" in testbot.pop_message()


def test_cachet_comp_list_all(testbot):
    """Test the cachet_comp_list_all command"""
    testbot.push_message('!cachet comp list all')
    assert "Available components:" in testbot.pop_message()


def test_cachet_comp_list_groups(testbot):
    """Test the cachet_comp_list_groups command"""
    testbot.push_message('!cachet comp list groups')
    assert "Available groups:" in testbot.pop_message()


def test_cachet_comp_list_group(testbot):
    """Test the cachet_comp_list_group command"""
    testbot.push_message('!cachet comp list group 1')
    assert 'Group: 1' in testbot.pop_message()


def test_cachet_comp_show(testbot):
    """Test the cachet_comp_show command"""
    testbot.push_message('!cachet comp show 999999')
    assert 'Unknown component id 999999' in testbot.pop_message()
    testbot.push_message('!cachet comp show 1')
    assert 'Component: 1' in testbot.pop_message()


def test_cachet_comp_search(testbot):
    """Test the cachet_comp_search command"""
    testbot.push_message('!cachet comp search test')
    assert 'Strong the unimplementation' in testbot.pop_message()


def test_cachet_comp_set_status(testbot):
    """Test the cachet_comp_set_status command"""
    testbot.push_message('!cachet comp set status 1 unknown')
    assert 'Unknown component status: unknown' in testbot.pop_message()
    testbot.push_message('!cachet comp set status 1 op')
    assert 'Component 1 status has been set' in testbot.pop_message()


def test_cachet_maint_forecast(testbot):
    """Test the cachet_maint_forecast command"""
    testbot.push_message('!cachet maint forecast --num 0')
    assert 'No operation found' in testbot.pop_message()
    testbot.push_message('!cachet maint forecast')
    assert 'Upcoming operations:' in testbot.pop_message()


def test_cachet_maint_last(testbot):
    """Test the cachet_maint_last command"""
    testbot.push_message('!cachet maint last --num 0')
    assert 'No maintenance found' in testbot.pop_message()
    testbot.push_message('!cachet maint last')
    assert 'Past maintenances:' in testbot.pop_message()


def test_cachet_maint_new(testbot):
    """Test the cachet_maint_new command"""
    testbot.push_message('!cachet maint new 2017-04-23 27 Maintenance Test')
    assert 'Strong the unimplementation' in testbot.pop_message()


def test_cachet_inci_last(testbot):
    """Test the cachet_inci_last command"""
    testbot.push_message('!cachet inci last')
    assert 'Last incidents:' in testbot.pop_message()


def test_cachet_inci_show(testbot):
    """Test the cachet_inci_show command"""
    testbot.push_message('!cachet inci show 999999')
    assert 'Unknown incident number 999999' in testbot.pop_message()
    testbot.push_message('!cachet inci show 1')
    assert 'Incident status:' in testbot.pop_message()


def test_cachet_inci_new(testbot):
    """Test the cachet_inci_new command"""
    testbot.push_message(
        '!cachet inci new XX - - "Test" "Fail creation."'
    )
    assert 'Unknown incident status: XX' in testbot.pop_message()
    testbot.push_message(
        '!cachet inci new invest - - "Test" "Test creation."'
    )
    assert 'New incident declared.' in testbot.pop_message()
    testbot.push_message(
        '!cachet inci new invest 1 - "Test" "Test creation."'
    )
    assert 'New incident declared.' in testbot.pop_message()
    testbot.push_message(
        '!cachet inci new invest 1 po "Test" "Test creation."'
    )
    assert 'New incident declared.' in testbot.pop_message()
    testbot.push_message(
        '!cachet inci new invest 9999 po "Test" "Fail creation."'
    )
    assert 'Unknown component id 9999' in testbot.pop_message()
    testbot.push_message(
        '!cachet inci new invest 9999 XX "Test" "Fail creation."'
    )
    assert 'Unknown component status: XX' in testbot.pop_message()


def test_cachet_inci_update(testbot):
    """Test the cachet_inci_update command"""
    testbot.push_message('!cachet inci update 1 XX po "Test update."')
    assert 'Unknown incident status: XX' in testbot.pop_message()
    testbot.push_message('!cachet inci update 1 invest XX "Fail update."')
    assert 'Unknown component status: XX' in testbot.pop_message()
    testbot.push_message('!cachet inci update 999999 invest po "Fail update."')
    assert 'Unknown incident number 999999' in testbot.pop_message()
    testbot.push_message('!cachet inci update 1 - - "Test update."')
    assert 'Incident has been updated.' in testbot.pop_message()
    testbot.push_message('!cachet inci update 1 invest po "Test update."')
    assert 'Incident has been updated.' in testbot.pop_message()


def test_cachet_inci_search(testbot):
    """Test the cachet_inci_search command"""
    testbot.push_message("!cachet inci search test")
    assert "not implemented." in testbot.pop_message()


def test_cachet_inci_set_component(testbot):
    """Test the cachet_inci_set_component command"""
    testbot.push_message('!cachet inci set component 9999999 1')
    assert 'Unknown incident number 9999999' in testbot.pop_message()
    testbot.push_message('!cachet inci set component 1 9999999')
    assert 'Unknown component id 9999999' in testbot.pop_message()
    testbot.push_message('!cachet inci set component 1 1')
    assert 'Impacted component has been updated.' in testbot.pop_message()


def test_cachet_inci_set_date(testbot):
    """Test the cachet_inci_set_date command"""
    testbot.push_message("!cachet inci set date 1 2017-04-23")
    assert "API does not support this operation" in testbot.pop_message()


def test_cachet_inci_rename(testbot):
    """Test the cachet_inci_rename command"""
    testbot.push_message("!cachet inci rename 9999999 'New name'")
    assert 'Unknown incident number 9999999' in testbot.pop_message()
    testbot.push_message("!cachet inci rename 1 'New name'")
    assert "Incident name has been updated." in testbot.pop_message()


def test_cachet_inci_set_hidden(testbot):
    """Test the cachet_inci_set_hidden command"""
    testbot.push_message("!cachet inci set hidden 9999999")
    assert 'Unknown incident number 9999999' in testbot.pop_message()
    testbot.push_message("!cachet inci set hidden 1")
    assert "Incident is hidden from status page." in testbot.pop_message()


def test_cachet_inci_set_visible(testbot):
    """Test the cachet_inci_set_visible command"""
    testbot.push_message("!cachet inci set visible 9999999")
    assert 'Unknown incident number 9999999' in testbot.pop_message()
    testbot.push_message("!cachet inci set visible 1")
    assert "Incident has been set to visible" in testbot.pop_message()
