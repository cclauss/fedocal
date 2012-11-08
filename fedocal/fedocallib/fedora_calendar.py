# -*- coding: utf-8 -*-

"""
fedora_calendar - HTML Calendar

Copyright (C) 2012 Johan Cwiklinski
Author: Johan Cwiklinski <johan@x-tnd.be>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or (at
your option) any later version.
See http://www.gnu.org/copyleft/gpl.html  for the full text of the
license.
"""

from datetime import date
from calendar import HTMLCalendar
from calendar import month_name
import flask


class FedocalCalendar(HTMLCalendar):
    """ Improve Python's HTMLCalendar object adding
    html validation and some features 'locally required'
    """

    def __init__(self, year, month, day, calendar_name=None):
        """ Constructor.
        Stores the year and the month asked.
        """
        super(FedocalCalendar, self).__init__()
        self.year = year
        self.month = month
        self.day = day
        self.calendar_name = calendar_name

    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        cur_date = date.today()
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            link_day = day
            if self.calendar_name:
                link_day = '<a href="%s">%d</a>' % (flask.url_for(
                        'calendar_fullday',
                        calendar_name=self.calendar_name, year=self.year,
                        month=self.month, day=day), day)
            if day == cur_date.day \
                and self.month == cur_date.month \
                and self.year == cur_date.year:
                return '<td class="%s today">%s</td>' % (
                    self.cssclasses[weekday], link_day)
            else:
                return '<td class="%s">%s</td>' % (
                    self.cssclasses[weekday], link_day)

    # pylint: disable=W0221
    def formatweek(self, theweek, current=False):
        """ Return a complete week as a table row.

        :kwarg current: a boolean stating wether this is the current
            week or not (the current week will have the css class:
            current_week)
        """
        string = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        if current:
            return '<tr class="current_week">%s</tr>' % string
        else:
            return '<tr>%s</tr>' % string

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            string = '%s %s' % (month_name[themonth], theyear)
        else:
            string = '%s' % month_name[themonth]
        prev_month_lnk = '<a class="button" href="#"><</a>'
        next_month_lnk = '<a class="button" href="#">></a>'
        return '<tr><th colspan="7" class="month">%s %s %s</th></tr>' % (
            prev_month_lnk, string, next_month_lnk)

    # pylint: disable=W0221
    def formatmonth(self, withyear=True):
        """
        Return a formatted month as a html valid table.
        """
        values = []
        item = values.append
        item('<table class="month">')
        item('\n')
        item(self.formatmonthname(self.year, self.month, withyear=withyear))
        item('\n')
        #item(self.formatweekheader())
        #item('\n')
        for week in self.monthdays2calendar(self.year, self.month):
            days = [day[0] for day in week]
            if self.day in days:
                item(self.formatweek(week, current=True))
            else:
                item(self.formatweek(week))
            item('\n')
        item('</table>')
        item('\n')
        return ''.join(values)
