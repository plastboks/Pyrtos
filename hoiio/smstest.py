from hoiio.rest import HoiioRestClient
from config import api

client = HoiioRestClient(api['id'], api['token'])

dest = raw_input('To: ')
msg = raw_input('Text: ')

# Send an SMS
resp = client.sms.send({'dest': dest,
                        'msg': msg,
                        })

