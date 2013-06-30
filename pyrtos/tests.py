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
      hashed = m.encode(u'1234')
      with transaction.manager:
          user = User(
                          username=u'user0',
                          email=u'user0@local',
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

    def _makeOne(self, username, email, password, id=False):
        m = BPM()
        hashed = m.encode(password)
        if id:
          return self._getTargetClass()(id=id,
                                        username=username,
                                        email=email,
                                        password=hashed)
        return self._getTargetClass()(username=username,
                                      email=email,
                                      password=hashed)

    def test_constructor(self):
        instance = self._makeOne(username='user1',
                                 email='user1@email.com',
                                 password='1234')
        self.assertEqual(instance.username, 'user1')
        self.assertEqual(instance.email, 'user1@email.com')
        self.assertTrue(instance.verify_password('1234'))

    def test_by_email(self):
        instance = self._makeOne(username='user2',
                                 email='user2@email.com',
                                 password='1234')
        self.session.add(instance)
        q = self._getTargetClass().by_email('user2@email.com')
        self.assertEqual(q.username, 'user2')
        self.assertEqual(q.email, 'user2@email.com')

    def test_by_id(self):
        instance = self._makeOne(id=1000,
                                 username='user3',
                                 email='user3@email.com',
                                 password='1234')
        self.session.add(instance)
        q = self._getTargetClass().by_id(instance.id)
        self.assertEqual(q.username, 'user3')
        self.assertEqual(q.email, 'user3@email.com')
    

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

    def test_index(self):
        from .views import index
        request = testing.DummyRequest()
        response = index(request)
        self.assertEqual(response['title'], 'Hello world')

    def test_login(self):
        from .views import login
        request = testing.DummyRequest()
        response = login(request)
        self.assertEqual(response['title'], 'Login')


class FunctionlTests(unittest.TestCase):
    def setUp(self):
        from pyrtos import main
        settings = {'sqlalchemy.url' : 'sqlite://'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.i = _initTestingDB(makeuser=True)

    def tearDown(self):
        del self.testapp
        from .models import DBSession
        DBSession.remove()

    def test_root(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'Hello world', res.body)

    def test_login(self):
        res = self.testapp.get('/login', status=200)
        self.assertTrue('Login' in res.body)

    def test_anonymous_user_cannot_se_logout(self):
        res = self.testapp.get('/logout', status=302)
        self.assertTrue(res.location, '/login')

    def test_try_login(self):
        res = self.testapp.post('/login', params={'email': 'user0@email.com',
                                                 'password' : '1234'},
                                          status=302)
        self.assertFalse('Login' in res.body)

    def test_fail_login(self):
        res = self.testapp.post('/login', params={'email': 'fakeuser@email.com',
                                                  'password' : 'abcd'},
                                          status=302)
        self.assertTrue('Login' in res.body)
