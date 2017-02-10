toubib - Mattermost bot for Cachet
==================================

* *Author:* Denis 'jawa' Pompilio <denis.pompilio@gmail.com>
* *Contact:* Denis 'jawa' Pompilio <denis.pompilio@gmail.com>
* *Sources:* https://github.com/outini/python-toubib/

Bot usage
---------

Component actions::

    comp[onents] status                            Show components problems
    comp[onents] list all                          List components
    comp[onents] list groups                       List groups
    comp[onents] list group <group_id>             List group's components
    comp[onents] show <c_id>                       Show component details
    comp[onents] search <search_regex>             Search component by name
    comp[onents] <c_id> status set <c_status>      Set component status

Maintenance actions::

    main[tenances] forecast [number]                         List upcoming maintenances
    main[tenances] last [number]                             List last maintenances
    main[tenances] on <c_id> at <schedule> <name>: <desc>    Schedule upcoming maintenance

Incident actions::

    inci[dents] last [number] [period]                              List last incidents
    inci[dents] show <i_id>                                         Show incident details
    inci[dents] search <search_regex>                               Search incident by name (regex)
    inci[dents] <i_status> [<c_status> on <c_id>] <name>: <desc>    Declare new incident
    inci[dents] <i_id> set date <date>                              Reset incident's date
    inci[dents] <i_id> update [i_status [c_status]]: <desc>         Update incident
    inci[dents] <i_id> rename <new_name>                            Rename incident
    inci[dents] <i_id> set visible                                  Set incident visible on status page
    inci[dents] <i_id> set hidden                                   Hide incident from status page

Variables::

    dates, and periods format:
        YYYYmmdd-HH:MM     Date (or schedule)
        [date]>[date]      Period

    Component ID (c_id) regex: \d+
    Incident ID (i_id) regex: \d+

    Component status (c_status):
        -            (current status)
        red|mo       Major Outage
        orange|po    Partial Outage
        blue|pi      Performance Issue
        green|op     Operational

    Incident status (i_status):
        -                 (current status)
        inv[estigating]   Investigations running
        id[entified]      Root cause identified
        wa[tching]        Fixed, watching stability
        fix[ed]           Fixed

License
-------

"GNU GENERAL PUBLIC LICENSE" (Version 2) *(see LICENSE file)*