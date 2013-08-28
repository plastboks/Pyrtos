#!/usr/bin/python
#
# reminder daemon for pyrtos
#
# usage: python(2) reminder.py development/production.ini
#

__requires__ = 'pyramid==1.4.2'
import sys
from pkg_resources import load_entry_point

from paste.deploy import appconfig
from reminderdaemon import Cron
from pyrtos.models.meta import DBSession, Base
from pyrtos.models import User
from sqlalchemy import create_engine, pool

if not len(sys.argv) is 2:
    print('You must specify a .ini file')
    sys.exit()

try:
    f = sys.argv[1]
    c = appconfig('config:'+f, relative_to=".")
except Exception as e:
    print(e)
    sys.exit()

target_metadata = Base.metadata

engine = create_engine(c['sqlalchemy.url'], poolclass=pool.NullPool)
DBSession.configure(bind=engine)
Base.metadata.bind = engine
