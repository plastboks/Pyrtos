import os
import sys
import transaction

from getpass import getpass
from cryptacular.bcrypt import BCRYPTPasswordManager as BPM
from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Base,
    User,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    m = BPM()
    a_email = raw_input('Enter email for admin account: ')
    a_pw = getpass('Enter password for admin account: ')
    a_hashed = m.encode(a_pw)

    with transaction.manager:
        admin = User(
                        username=u'admin',
                        email=a_email,
                        password=a_hashed
                    )
        DBSession.add(admin)

