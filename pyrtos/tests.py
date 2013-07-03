import unittest
import transaction

from pyramid import testing
from webtest import TestApp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cryptacular.bcrypt import BCRYPTPasswordManager as BPM

from webob import multidict

from pyrtos import main
from .models import (
    DBSession,
    Base,
    User,
)

class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite://')

    def setUp(self):
        Base.metadata.create_all(self.engine)
        DBSession.configure(bind=self.engine)
        self.session = DBSession
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
        self.session.remove()

def _initTestingDB(makeuser=False):
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    if makeuser:
      m = BPM()
      hashed = m.encode(u'1234567')
      with transaction.manager:
          user = User(
                          username=u'user',
                          email=u'user@email.com',
                          password=hashed
                      )
          DBSession.add(user)
    return DBSession


class UserModelTests(BaseTestCase):

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
    

class CategoryModelTests(BaseTestCase):

    def _getTargetClass(self):
        from pyrtos.models import Category
        return Category

    def _makeOne(self, id, title, name):
        return self._getTargetClass()(id=id, title=title, name=name)

    def test_constructor(self):
        instance = self._makeOne(100, 'Test', 'best')
        self.session.add(instance)

        qn = self._getTargetClass().by_name('best')
        self.assertEqual(qn.title, 'Test')

        qi = self._getTargetClass().by_id(100)
        self.assertEqual(qi.title, 'Test')


class ViewTests(BaseTestCase):

    def test_index(self):
        from .views import index
        request = testing.DummyRequest()
        response = index(request)
        self.assertEqual(response['title'], 'Hello world')

    def test_login(self):
        from .views import login
        request = testing.DummyRequest()
        request.POST = multidict.MultiDict()
        response = login(request)
        self.assertEqual(response['title'], 'Login')

    def test_categories(self):
        from .views import categories
        request = testing.DummyRequest()
        response = categories(request)
        self.assertEqual(response['title'], 'Categories')

    def test_category_create(self):
        from .views import category_create
        request = testing.DummyRequest()
        request.POST = multidict.MultiDict()
        request.matchdict = {'name' : 'test'}
        response = category_create(request)
        self.assertEqual(response['title'], 'New category')


class IntegrationTestBase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        settings = {'sqlalchemy.url' : 'sqlite://'}
        cls.app = main({}, **settings)
        super(IntegrationTestBase, cls).setUpClass()
    
    def setUp(self):
        self.app = TestApp(self.app)
        self.config = testing.setUp()
        super(IntegrationTestBase, self).setUp()

class TestViews(IntegrationTestBase):

    def setUp(self):
        self.app = TestApp(self.app)
        self.session = _initTestingDB(makeuser=True)

    def tearDown(self):
        del self.app
        self.session.remove()

    def test_root_as_anonymous(self):
        res = self.app.get('/', status=302)
        self.assertTrue(res.location, 'http://localhost/login')

    def test_login(self):
        res = self.app.get('/login', status=200)
        self.assertTrue('Login' in res.body)

    def test_anonymous_user_cannot_se_logout(self):
        res = self.app.get('/logout', status=302)
        self.assertTrue(res.location, 'http://localhost/login')

    def test_try_login(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                           'csrf_token' : token,
                                           'email': 'user@email.com',
                                           'password' : '1234567',}
                               )
        self.assertTrue(res.status_int, 302)
        logged_in = self.app.get('/login')
        self.assertTrue(res.status_int, 302)

    def test_fail_login(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                           'email': 'fake@email.com',
                                           'password' : 'abcdefg',
                                           'csrf_token' : token}
                               )
        self.assertTrue(res.status_int, 200)

    def test_categories_as_anonymous(self):
        res = self.app.get('/categories', status=302)
        self.assertTrue(res.location, 'http://localhost/login')

    def test_categories(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                           'csrf_token' : token,
                                           'email': 'user@email.com',
                                           'password' : '1234567',}
                               )
        res = self.app.get('/categories')
        self.assertTrue(res.status_int, 200)

        res = self.app.get('/category/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/category/new', {'name' : 'testbest',
                                                  'title' : 'testbest',
                                                  'csrf_token' : token}
                               )
        res = self.app.get('/categories', status=200)
        self.assertTrue('testbest' in res.body)

        res = self.app.get('/category/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/category/edit/1', params={'id' : 1,
                                                            'name' : 'besttest',
                                                            'title' : 'besttest',
                                                            'csrf_token' : token}
                               )
        categories = self.app.get('/categories', status=200)
        self.assertTrue('besttest' in categories.body)

        res = self.app.get('/category/edit/1', status=200)
        self.assertTrue('besttest' in res.body)
        res = self.app.get('/category/edit/100', status=404)

        self.testapp.get('/category/delete/1', status=302)
        res = self.testapp.get('/categories/archived', status=200)
        self.assertTrue('besttest' in res.body)

        self.testapp.get('/category/restore/1', status=302)
        res = self.testapp.get('/categories', status=200)
        self.assertTrue('besttest' in res.body)

        self.testapp.get('/category/edit/100', status=404)
        self.testapp.get('/category/delete/100', status=404)
        self.testapp.get('/category/restore/100', status=404)
