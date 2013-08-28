#!/usr/bin/python
#
# This is the crondaemon for Pyrtos. This library class is
# responsible for running trough the database and create
# reminders.
#
#

class Cron():
    
    db = ''

    def __init__(self):
        # this class should extend or inherit a SqlAlchemy instance.
        self.initiateDB()

    def initiateDB():
      self.db = 'do nothing'
