import unittest
import transaction

from pyramid import testing
from cryptacular.bcrypt import BCRYPTPasswordManager as BPM

from .models import DBSession

def _initTestingDB():
    from sqlalchemy import create_engine
    from pyrtos.models import (
        DBSession,
        Base,
        User,
        )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    m = BPM()
    hashed = m.encode(u'abc123')
    with transaction.manager:
        user = User(
                        username=u'admin',
                        email=u'admin@local',
                        password=hashed
                    )
        DBSession.add(user)
    return DBSession

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            User,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_it(self):
        from .views import index
        request = testing.DummyRequest()
        response = index(request)
        self.assertEqual(response['title'], 'Hello world')

class FunctionlTests(unittest.TestCase):
    def setUp(self):
        from pyrtos import main
        settings = {'sqlalchemy.url' : 'sqlite://'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        _initTestingDB()

    def tearDown(self):
        del self.testapp
        from pyrtos.models import DBSession
        DBSession.remove()

    def test_it(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'Hello world', res.body)
