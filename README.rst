|PythonSupport|_ |License|_ |Codacy|_ |Coverage|_

err-cachet - ErrBot plugin for Cachet
=====================================

.. image:: https://api.codacy.com/project/badge/Grade/0cd02ae19e2c428bbb718d5ff62f650e
   :alt: Codacy Badge
   :target: https://www.codacy.com/app/outini/err-cachet?utm_source=github.com&utm_medium=referral&utm_content=outini/err-cachet&utm_campaign=badger

* *Contact:* Denis 'jawa' Pompilio <denis.pompilio@gmail.com>
* *Sources:* https://github.com/outini/err-cachet/

Plugin usage
------------

**Component actions**::

    !cachet comp status                          Show components problems
    !cachet comp list all                        List components
    !cachet comp list groups                     List groups
    !cachet comp list group <group_id>           List group's components
    !cachet comp show <c_id>                     Show component details
    !cachet comp search <search_regex>           Search component by name
    !cachet comp status set <c_id> <c_status>    Set component status

**Maintenance actions**::

    !cachet maint forecast [--num <number>]               List upcoming maintenances
    !cachet maint last [--num <number>]                   List last maintenances
    !cachet maint new <schedule> <c_id> <name>: <desc>    Schedule upcoming maintenance

**Incident actions**::

    !cachet inci last [--num <number>] [--period <period>]         List last incidents
    !cachet inci show <i_id>                                       Show incident details
    !cachet inci search <search_regex>                             Search incident by name (regex)
    !cachet inci new <i_status> <c_id> <c_status> <name> <desc>    Declare new incident
    !cachet inci set date <i_id> <date>                            Set incident's date
    !cachet inci update <i_id> <i_status> <c_status> <desc>        Update incident
    !cachet inci rename <i_id> <new_name>                          Rename incident
    !cachet inci set visible <i_id>                                Set incident visible on status page
    !cachet inci set hidden <i_id>                                 Hide incident from status page

**Variables**::

    dates, and periods format:
        YYYYmmdd-HH:MM     Date (or schedule)
        [date]>[date]      Period

    Component ID (c_id):   A number or dash (-) for unchanged or unset
    Incident ID (i_id):    A number or dash (-) for unchanged or unset

    Component status (c_status):
        -            (current status or unset)
        red|mo       Major Outage
        orange|po    Partial Outage
        blue|pi      Performance Issue
        green|op     Operational

    Incident status (i_status):
        -                 (current status or unset)
        inv[estigating]   Investigations running
        id[entified]      Root cause identified
        wa[tching]        Fixed, watching stability
        fix[ed]           Fixed

Example
-------
::

    >>> !cachet inci new ident 27 po "NAS filer performance issue" "Major issue with storage performance."
    New incident declared.
    Don't forget to make it visible on status page.
    Try: !incident set visible 10

    >>> !cachet inci show 10
    Status page service: [10] NAS filer performance issue (http://status.domain.tld/incident/10)

    Incident status: Investigating
    Component: 27 RP: Datacenter A
    Component status: :warning: Partial Outage
    Created at 2017-06-30 17:08:00
    Last updated 2017-06-30 17:08:00
    Description:
    Major issue with storage performance.

    >>> !cachet comp status
    Status page service (http://status.domain.tld)

    Components problems:
    -  1  DNS Master: :warning: Partial Outage
    -  5  Storage NAS - Datacenter A: :warning: Performance Issues
    -  27  RP: Datacenter A: :warning: Partial Outage

    >>> !cachet comp show 27
    Status page service (http://status.domain.tld)

    Component: 27 RP: Datacenter A
    Status: :warning: Partial Outage
    Link:
    Description: Production RP on datacenter A
    Last updated 2017-04-21 12:02:35
    Active incidents:
      10 Investigating: NAS filer performance issue
      40 Investigating: test incident

    >>> !cachet inci set visible 10
    Incident has been set to visible on status page.

    >>> !cachet inci update 40 fixed - "Closing the test incident."
    Incident has been updated.

Tests and coverage
------------------

Requisites::

  pip install pytest coverage

Testing and getting coverage::

  coverage run --source errbot-root/plugins/err-cachet -m py.test errbot-root/plugins/err-cachet
  coverage html


License
-------

"GNU GENERAL PUBLIC LICENSE" (Version 2) *(see LICENSE file)*


.. |PythonSupport| image:: https://img.shields.io/badge/python-3.4-blue.svg
.. _PythonSupport: https://github.com/outini/err-cachet/
.. |License| image:: https://img.shields.io/badge/license-GPLv2-green.svg
.. _License: https://github.com/outini/err-cachet/
.. |Codacy| image:: https://api.codacy.com/project/badge/Grade/0cd02ae19e2c428bbb718d5ff62f650e
.. _Codacy: https://www.codacy.com/app/outini/err-cachet
.. |Coverage| image:: https://api.codacy.com/project/badge/Coverage/0cd02ae19e2c428bbb718d5ff62f650e
.. _Coverage: https://www.codacy.com/app/outini/err-cachet