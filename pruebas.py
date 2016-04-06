# -*- coding: utf-8 -*-
# !/usr/bin/env python

from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, 'es_AR.utf8')
print locale.getlocale(locale.LC_ALL)

print locale.nl_langinfo(locale.DAY_1)
print datetime.strptime('2016-01-03', '%Y-%m-%d').strftime('%w')
print datetime.strptime('2016-01-03', '%Y-%m-%d').strftime('%a')
print datetime.strptime('2016-01-03', '%Y-%m-%d').strftime('%A')
