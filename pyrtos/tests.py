import unittest
import transaction

from pyramid import testing
from cryptacular.bcrypt import BCRYPTPasswordManager as BPM

from .models import DBSession

def _initTestingDB(makeuser=False):
    from sqlalchemy import create_engine
    from pyrtos.models import (
        DBSession,
        Base,
        User,
        )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    if makeuser:
      m = BPM()
      hashed = m.encode(u'abc123')
      with transaction.manager:
          user = User(
                          username=u'user1',
                          email=u'user1@local',
                          password=hashed
                      )
          DBSession.add(user)
    return DBSession


class UserModelTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB(makeuser=False)

    def tearDown(self):
        self.session.remove()

    def _getTargetClass(self):
        from pyrtos.models import User
        return User

    def _makeOne(self, username, email, password):
        m = BPM()
        hashed = m.encode(password)
        return self._getTargetClass()(username=username,
                                      email=email,
                                      password=hashed)

    def test_constructor(self):
        m = BPM()
        instance = self._makeOne(username='user',
                            email='user@email.com',
                            password='1234')
        self.assertEqual(instance.username, 'user')
        self.assertEqual(instance.email, 'user@email.com')
        self.assertTrue(m.check(instance.password, '1234'))


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
        _initTestingDB(makeuser=True)

    def tearDown(self):
        del self.testapp
        from pyrtos.models import DBSession
        DBSession.remove()

    def test_root(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'Hello world', res.body)

    def test_login(self):
        res = self.testapp.get('/login', status=200)
        self.assertIn(b'Login', res.body)

