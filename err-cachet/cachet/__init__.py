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
from datetime import datetime
import requests
from errbot import BotPlugin, botcmd, arg_botcmd
from . import utils
from .resources import views
from pylls import cachet, client, tests

VERSION = '0.2.0'

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
CACHET_TITLE = 'Status page service'
CACHET_LINK = 'http://status.domain.tld'

CONFIG_TEMPLATE = {'api_endpoint': "http://status.domain.tld/api/v1",
                   'api_token': "XXXXXXXXXXXXXXXXXXXX"}


class Cachet(BotPlugin):
    """Cachet status service plugin"""

    def __init__(self, bot, name=None):
        """Init method"""
        self._cachet_client = None
        self._components = None
        self._incidents = None
        super().__init__(bot, name)

    @staticmethod
    def get_configuration_template():
        """Return configuration hint for user"""
        return CONFIG_TEMPLATE

    def configure(self, configuration):
        """Configure the plugin"""
        if configuration and configuration != {}:
            config = configuration
        else:
            # Try to autoconfigure from environment
            config = {'api_endpoint': os.environ.get("cachet_api_endpoint"),
                      'api_token': os.environ.get("cachet_api_token")}

        super().configure(config)

    @staticmethod
    def check_configuration(config):
        """Check plugin configuration"""
        if "api_token" not in config:
            raise Exception("api_token must be specified.")
        if "api_endpoint" not in config:
            raise Exception("api_endpoint must be specified.")

    def activate(self):
        """Activate the plugin"""
        self.log.debug("Activation of Cachet plugin...")
        if not self.config:
            self.log.info('Cachet plugin is not configured. Abort activation.')
            return

        api_endpoint = self.config["api_endpoint"]
        api_token = self.config["api_token"]
        self.log.debug("Cachet API endpoint: %s" % api_endpoint)
        self.log.debug("Cachet API token: %s" % api_token)

        # Activate mock API of requested
        if os.environ.get('TEST_API'):
            self._cachet_client = tests.test_api.api_client()
        else:
            self._cachet_client = client.CachetAPIClient(
                api_endpoint=api_endpoint,
                api_token=api_token
            )

        self._components = cachet.Components(self._cachet_client)
        self._incidents = cachet.Incidents(self._cachet_client)

        super().activate()

    def reply_card(self, msg, body, opt_params=None):
        """Reply using send_card method

        :arg Object msg: Message object to reply to
        :arg str body: Card body text
        :arg dict opt_params: Optionnal parameters to pass to send_card method
        """
        if opt_params is None:
            opt_params = {}
        options = {
            "title": CACHET_TITLE,
            "link": CACHET_LINK,
            "body": body,
            "color": utils.COLORS[1],
            "in_reply_to": msg
        }
        if len(opt_params):
            options.update(opt_params)

        self.send_card(**options)

    @botcmd(split_args_with=None)
    def cachet_plugin_version(self, msg, args):
        """Show cachet plugin version"""
        self.log.debug('Call cachet_plugin_version')
        return "Cachet plugin version: %s" % VERSION

    #
    # Components actions
    ##########################################################################

    @botcmd(split_args_with=None)
    def cachet_comp_status(self, msg, args):
        """Show components problems"""
        self.log.debug('Call cachet_comp_status')
        worst_status = 1
        reply = ["Components problems:"]
        for component in self._components.get():
            c_status = int(component['status'])
            if c_status > 1:
                if c_status > worst_status:
                    worst_status = c_status
                reply.append("-  `%d`  %s: %s %s" % (
                    component['id'], component['name'],
                    utils.ICONS[c_status], component['status_name']))
        if len(reply) == 1:
            reply.append(":ok: Everything is fine")
        self.reply_card(msg, "\n".join(reply),
                        {'color': utils.COLORS[worst_status]})

    @botcmd(split_args_with=None)
    def cachet_comp_list_all(self, msg, args):
        """List available components"""
        self.log.debug('Call cachet_comp_list_all')
        reply = ["Available components:"]
        for component in self._components.get():
            c_status = int(component['status'])
            reply.append("-  `%d`  **%s**: %s %s" % (
                component['id'], component['name'],
                utils.ICONS[c_status], component['status_name']))
        self.reply_card(msg, "\n".join(reply))

    @botcmd(split_args_with=None)
    def cachet_comp_list_groups(self, msg, args):
        """List available component groups"""
        self.log.debug('Call cachet_comp_list_groups')
        groups = self._components.groups.get()
        reply = ["Available groups:"]
        for group in groups:
            reply.append("-  `%d`  **%s**" % (group['id'], group['name']))
        self.reply_card(msg, "\n".join(reply))

    @arg_botcmd('gid', type=int, help="ID of the group")
    def cachet_comp_list_group(self, msg, gid):
        """List group's components"""
        self.log.debug('Call cachet_comp_list_group')
        worst_status = 1
        group = list(self._components.groups.get(gid))[0]
        reply = [
            "**Group**: `%s` %s" % (group['id'], group['name']),
            "**Components:**"
        ]
        for component in self._components.get(group_id=gid):
            c_status = int(component['status'])
            reply.append("-  `%d`  **%s**:  %s %s" % (
                component['id'], component['name'],
                utils.ICONS[c_status], component['status_name']))
            if c_status > worst_status:
                worst_status = c_status
        self.reply_card(msg, "\n".join(reply),
                        {'color': utils.COLORS[worst_status]})

    @arg_botcmd('cid', type=int, help="ID of the component")
    def cachet_comp_show(self, msg, cid):
        """Show component details"""
        self.log.debug('Call cachet_comp_show')
        try:
            component = list(self._components.get(cid))[0]
        except requests.exceptions.HTTPError:
            return views.unknown_component(cid)

        c_status = int(component['status'])
        incidents = list(self._incidents.get(component_id=cid))
        incidents_lines = []
        for incident in incidents:
            if int(incident['status']) in (0, 4,):
                continue
            line = "`%s` **%s**: %s" % (
                incident['id'], incident['human_status'],
                incident['name'])
            incidents_lines.append(line)
        if not len(incidents_lines):
            incidents_lines = ["No active incident"]
        reply = views.COMPONENT_VIEW % (
            component['id'], component['name'],
            utils.ICONS[c_status], component['status_name'],
            component['link'],
            component['description'],
            component['updated_at'],
            "\n".join(incidents_lines)
        )
        self.reply_card(msg, reply, {'color': utils.COLORS[c_status]})

    # TODO: implement components search function
    @arg_botcmd('text', type=str, help="Search text")
    def cachet_comp_search(self, msg, text):
        """Search component by name"""
        self.log.debug('Call cachet_comp_search')
        return "Strong the unimplementation is with this one"

    @arg_botcmd('cstatus', type=str, help="Status of the component")
    @arg_botcmd('cid', type=int, help="ID of the component")
    def cachet_comp_set_status(self, msg, cid, cstatus):
        """Set component status"""
        self.log.debug('Call cachet_comp_set_status')
        status_info = utils.get_cstatus(cstatus)
        if not status_info:
            return "Unknown component status: %s" % (cstatus,)
        self._components.update(cid, status=status_info[0])
        return "Component `%s` status has been set to `%s`" % (
            cid, status_info[1])

    #
    # Maintenances actions
    ##########################################################################

    @arg_botcmd('--num', type=int, help="Number of entries", default=5)
    def cachet_maint_forecast(self, msg, num):
        """List upcoming maintenances"""
        self.log.debug('Call cachet_maint_forecast')
        # Selecting scheduled operation from "incidents" and sorting
        incidents = self._incidents.get()
        scheduled = [ent for ent in incidents if ent['status'] == '0']
        scheduled.sort(key=lambda entry: entry['scheduled_at'])

        now = datetime.now()

        reply = ["Upcoming operations:"]
        for maintenance in scheduled[0:num]:
            if datetime.strptime(maintenance['scheduled_at'],
                                 DATE_FORMAT) > now:
                reply.append("-  `%s` Scheduled on **%s**: %s" % (
                    maintenance['id'],
                    maintenance['scheduled_at'], maintenance['name']))

        if len(reply) == 1:
            reply.append("No operation found")
        self.reply_card(msg, "\n".join(reply))

    @arg_botcmd('--num', type=int, help="Number of entries", default=5)
    def cachet_maint_last(self, msg, num):
        """List past maintenances"""
        self.log.debug('Call cachet_maint_last')
        # Selecting scheduled operation from "incidents" and sorting
        incidents = self._incidents.get()
        scheduled = [ent for ent in incidents if ent['status'] == '0']
        scheduled.sort(key=lambda entry: entry['scheduled_at'])

        now = datetime.now()

        reply = ["Past maintenances:"]
        for maint in scheduled[0:int(num)]:
            if datetime.strptime(maint['scheduled_at'],
                                 DATE_FORMAT) < now:
                reply.append("-  `%s` **%s**: %s" % (maint['id'],
                                                     maint['scheduled_at'],
                                                     maint['name']))

        if len(reply) == 1:
            reply.append("No maintenance found")
        self.reply_card(msg, "\n".join(reply))

    # TODO: implement maintenance creation function
    @arg_botcmd('desc', type=str, help="Maintenance description")
    @arg_botcmd('name', type=str, help="Maintenance name")
    @arg_botcmd('cid', type=int, help="Component ID")
    @arg_botcmd('schedule', type=str, help="Maintenance schedule date")
    def cachet_maint_new(self, msg, schedule, cid, name, desc):
        """Creation new maintenance"""
        self.log.debug('Call cachet_maint_new')
        return "Strong the unimplementation is with this one"

    #
    # Incidents actions
    ##########################################################################

    @arg_botcmd('--num', type=int, help="Number of entries", default=5)
    def cachet_inci_last(self, msg, num):
        """List last incidents"""
        self.log.debug('Call cachet_inci_last')
        # It is actually not possible to sort incident by date via Cachet
        # We get long list of incident and sort it by ourselves
        incidents = self._incidents.get()
        # Cleaning scheduled operation from "incidents"
        incidents = [ent for ent in incidents if ent['status'] != '0']
        incidents.sort(key=lambda entry: entry['created_at'], reverse=True)
        reply = ["Last incidents:"]
        for incident in incidents[0:int(num)]:
            reply.append("-  `%s`  [%s] `%s` %s" % (incident['id'],
                                                    incident['created_at'],
                                                    incident['human_status'],
                                                    incident['name']))
        self.reply_card(msg, "\n".join(reply))

    @arg_botcmd('i_id', type=int, help="ID of the Incident")
    def cachet_inci_show(self, msg, i_id):
        """Show incident details"""
        self.log.debug('Call cachet_inci_show')
        try:
            incident = list(self._incidents.get(i_id))[0]
        except requests.exceptions.HTTPError:
            return views.unknown_incident(i_id)

        if incident['component_id'] != "0":
            component = list(self._components.get(incident['component_id']))[0]
        else:
            # TODO: clean this
            component = {
                'id': 0,
                'name': "No component specified",
                'status_name': "Unavailable",
                'status': 0
            }
        c_status = int(component['status'])
        reply = [
            '**Incident status:** `%s`' % (incident['human_status']),
            '**Component:** `%d` %s' % (component['id'], component['name']),
            '**Component status:** %s %s' % (utils.ICONS[c_status],
                                             component['status_name']),
            '_Created at_ `%s`' % (incident['created_at']),
            '_Last updated_ `%s`' % (incident['updated_at']),
            '**Description:**',
            incident['message']
        ]
        title = '%s: [%d] %s' % (CACHET_TITLE,
                                 incident['id'], incident['name'])
        link = '%s/incident/%d' % (CACHET_LINK, incident['id'])
        self.reply_card(msg, "\n".join(reply), {
            'title': title, 'link': link, 'color': utils.COLORS[c_status]})

    @arg_botcmd('desc', type=str, help="Incident description message")
    @arg_botcmd('name', type=str, help="Name of the incident")
    @arg_botcmd('cstatus', type=str, help="Status of the impacted component")
    @arg_botcmd('cid', type=str, help="ID the impacted component")
    @arg_botcmd('istatus', type=str, help="Status of the incident")
    def cachet_inci_new(self, msg, istatus, cstatus, cid, name, desc):
        """Declare new incident"""
        self.log.debug('Call cachet_inci_new')
        istatus_info = utils.get_istatus(istatus)
        if not istatus_info:
            return "Unknown incident status: %s" % istatus

        if cstatus == "-":
            cstatus = None
        if cid == "-":
            cid = None

        if cid:
            if not cstatus:
                comp = list(self._components.get(cid))[0]
                cstatus_info = (int(comp['status']), comp['status_name'])
            else:
                cstatus_info = utils.get_cstatus(cstatus)

            if not cstatus_info:
                return "Unknown component status: %s" % cstatus

            try:
                list(self._components.get(cid))
            except requests.exceptions.HTTPError:
                return views.unknown_component(cid)

            msg_header = views.message_header(istatus_info[1], cstatus_info[1])
            updated_msg = msg_header + '\n' + desc
            created = self._incidents.create(
                name, updated_msg, istatus_info[0], 0,
                component_id=cid,
                component_status=cstatus_info[0])
        else:
            msg_header = "##### [%s] %s\n" % (datetime.now(), istatus_info[1])
            created = self._incidents.create(name, msg_header + desc,
                                             istatus_info[0], 0)

        return (
            "New incident declared.\n"
            "Don't forget to make it visible on status page.\n"
            "Try: `!incident set visible %s`" % created['id']
        )

    @arg_botcmd('imsg', type=str, help="Update message")
    @arg_botcmd('cstatus', type=str, help="Status of the component")
    @arg_botcmd('istatus', type=str, help="Status of the Incident")
    @arg_botcmd('iid', type=int, help="ID of the Incident")
    def cachet_inci_update(self, msg, iid, istatus, cstatus, imsg):
        """Update incident"""
        self.log.debug('Call cachet_inci_update')
        try:
            incident = list(self._incidents.get(iid))[0]
        except requests.exceptions.HTTPError:
            return views.unknown_incident(iid)

        if istatus == "-":
            istatus = None
        if cstatus == "-":
            cstatus = None

        if istatus:
            istatus_info = utils.get_istatus(istatus)
            if not istatus_info:
                return "Unknown incident status: %s" % istatus
        else:
            istatus_info = utils.get_istatus(incident['human_status'])

        if cstatus and incident['component_id'] == "0":
            return ("No component impacted by incident, "
                    "please set one before updating component status.")

        if cstatus:
            cstatus_info = utils.get_cstatus(cstatus)
            if not cstatus_info:
                return "Unknown component status: %s" % cstatus
        else:
            component = list(self._components.get(incident['component_id']))[0]
            cstatus_info = utils.get_cstatus(component['status_name'])

        updated_msg = [views.message_header(istatus_info[1], cstatus_info[1]),
                       imsg,
                       views.updates_separator(),
                       incident["message"]]

        self._incidents.update(iid, status=istatus_info[0],
                               component_id=incident['component_id'],
                               component_status=cstatus_info[0],
                               message="\n".join(updated_msg))
        return "Incident has been updated."

    # TODO: implement incidents search function
    @arg_botcmd('text', type=str, help="Search text")
    def cachet_inci_search(self, msg, text):
        """Search incident by name"""
        self.log.debug('Call cachet_inci_search')
        return "This command is still not implemented."

    @arg_botcmd('cid', type=int, help="ID of the component")
    @arg_botcmd('iid', type=int, help="ID of the incident")
    def cachet_inci_set_component(self, msg, iid, cid):
        """Set impacted component"""
        self.log.debug('Call cachet_inci_set_component')
        try:
            list(self._incidents.get(iid))
        except requests.exceptions.HTTPError:
            return views.unknown_incident(iid)

        try:
            component_info = list(self._components.get(cid))[0]
        except requests.exceptions.HTTPError:
            return views.unknown_component(cid)

        self._incidents.update(iid,
                               component_status=component_info['status'],
                               component_id=cid)
        return "Impacted component has been updated."

    # Todo: implement this function when Cachet 2.4 is released
    @arg_botcmd('date', type=str, help="Incident new date")
    @arg_botcmd('iid', type=int, help="ID of the incident")
    def cachet_inci_set_date(self, msg, iid, date):
        """Set incident's date"""
        self.log.debug('Call cachet_inci_set_date')
        return "Cachet 2.3.10 API does not support this operation"

    @arg_botcmd('name', type=str, help="Incident new name")
    @arg_botcmd('iid', type=int, help="ID of the incident")
    def cachet_inci_rename(self, msg, iid, name):
        """Rename incident"""
        self.log.debug('Call cachet_inci_rename')
        try:
            list(self._incidents.get(iid))
        except requests.exceptions.HTTPError:
            return views.unknown_incident(iid)
        self._incidents.update(iid, name=name)
        return "Incident name has been updated."

    @arg_botcmd('iid', type=int, help="ID of the incident")
    def cachet_inci_set_hidden(self, msg, iid):
        """Hide incident from status page"""
        self.log.debug('Call cachet_inci_set_hidden')
        try:
            list(self._incidents.get(iid))
        except requests.exceptions.HTTPError:
            return views.unknown_incident(iid)
        self._incidents.update(iid, visible=0)
        return "Incident is hidden from status page."

    @arg_botcmd('iid', type=int, help="ID of the incident")
    def cachet_inci_set_visible(self, msg, iid):
        """Set incident visible on status page"""
        self.log.debug('Call cachet_inci_set_visible')
        try:
            list(self._incidents.get(iid))
        except requests.exceptions.HTTPError:
            return views.unknown_incident(iid)
        self._incidents.update(iid, visible=1)
        return "Incident has been set to visible on status page."
