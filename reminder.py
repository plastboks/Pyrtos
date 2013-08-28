#!/usr/bin/python
#
# reminder daemon for pyrtos
#
# usage: python(2) reminder.py development/production.ini
#

__requires__ = 'pyramid==1.4.2'
import sys
from pkg_resources import load_entry_point

from paste.deploy.loadwsgi import ConfigLoader
from reminderdaemon import Cron

if not len(sys.argv) is 2:
    print('You must specify a .ini file')
    sys.exit()

f = sys.argv[1]
c = ConfigLoader(f)
