#!/usr/bin/python2
#
# This is a simple debug/test sms program for sending sms
# trough the Hoiio API
#
#

from hoiio.rest import HoiioRestClient
from config import api

client = HoiioRestClient(api['id'], api['token'])

dest = raw_input('To: ')
msg = raw_input('Text: ')
#sender = raw_input('From: ') # optional feature @ Hoiio.

# Send the SMS
resp = client.sms.send({'dest': dest,
                        'msg': msg,
                        #'sender_name': sender,
                        })
