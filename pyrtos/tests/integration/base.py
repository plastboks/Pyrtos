import transaction

from sqlalchemy import create_engine
from cryptacular.bcrypt import BCRYPTPasswordManager as BPM
from pyrtos import main
from pyrtos.models.meta import DBSession, Base
from pyrtos.tests import BaseTestCase
from pyrtos.models import User


def _initTestingDB(makeuser=False):
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    if makeuser:
        m = BPM()
        hashed = m.encode(u'1234567')
        with transaction.manager:
            user = User(email=u'user@email.com',
                        password=hashed,
                        group='admin',
                        )
            DBSession.add(user)
    return DBSession


class IntegrationTestBase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        settings = {'sqlalchemy.url': 'sqlite://'}
        cls.app = main({}, **settings)
        super(IntegrationTestBase, cls).setUpClass()
