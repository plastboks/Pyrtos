import unittest
import transaction

from datetime import datetime, timedelta, date
from pyramid import testing
from webtest import TestApp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cryptacular.bcrypt import BCRYPTPasswordManager as BPM

from webob import multidict

from pyrtos import main

from pyrtos.models.meta import DBSession, Base
from pyrtos.models import (
    User,
    Category,
    Creditor,
    Income,
    Expenditure,
)

def _initTestingDB(makeuser=False):
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    if makeuser:
      m = BPM()
      hashed = m.encode(u'1234567')
      with transaction.manager:
          user = User(
                          email=u'user@email.com',
                          password=hashed,
                          group='admin',
                      )
          DBSession.add(user)
    return DBSession

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

class UserModelTests(BaseTestCase):

    def _getTargetClass(self):
        from pyrtos.models import User
        return User

    def _makeOne(self, email, password, group, id=False):
        m = BPM()
        hashed = m.encode(password)
        if id:
          return self._getTargetClass()(id=id,
                                        email=email,
                                        password=hashed,
                                        group=group)
        return self._getTargetClass()(
                                      email=email,
                                      password=hashed,
                                      group=group)

    def test_constructor(self):
        instance = self._makeOne(
                                 email='user1@email.com',
                                 password='1234',
                                 group='admin',
                                 )
        self.assertEqual(instance.email, 'user1@email.com')
        self.assertTrue(instance.verify_password('1234'))

    def test_by_email(self):
        instance = self._makeOne(
                                 email='user2@email.com',
                                 password='1234',
                                 group='admin')
        self.session.add(instance)
        q = self._getTargetClass().by_email('user2@email.com')
        self.assertEqual(q.email, 'user2@email.com')

    def test_by_id(self):
        instance = self._makeOne(id=1000,
                                 email='user3@email.com',
                                 password='1234',
                                 group='admin')
        self.session.add(instance)
        q = self._getTargetClass().by_id(instance.id)
        self.assertEqual(q.email, 'user3@email.com')
    

class CategoryModelTests(BaseTestCase):

    def _getTargetClass(self):
        from pyrtos.models import Category
        return Category

    def _makeOne(self, id, title):
        return self._getTargetClass()(id=id, title=title, user_id=1)

    def test_constructor(self):
        instance = self._makeOne(100, 'Test')
        self.session.add(instance)

        qi = self._getTargetClass().by_id(100)
        self.assertEqual(qi.title, 'Test')


class TagModelTests(BaseTestCase):

    def _getTargetClass(self):
        from pyrtos.models import Tag
        return Tag

    def _makeOne(self, id, name):
        return self._getTargetClass()(id=id, name=name)

    def test_constructor(self):
        instance = self._makeOne(100, 'Test')
        self.session.add(instance)

        qi = self._getTargetClass().by_id(100)
        self.assertEqual(qi.name, 'Test')


class CreditorModelTests(BaseTestCase):

    def _getTargetClass(self):
        from pyrtos.models import Creditor
        return Creditor

    def _makeOne(self, id, title):
        return self._getTargetClass()(id=id, title=title, user_id=1)

    def test_constructor(self):
        instance = self._makeOne(100, 'Test')
        self.session.add(instance)

        qi = self._getTargetClass().by_id(100)
        self.assertEqual(qi.title, 'Test')


class IncomeModelTests(BaseTestCase):

    def _getTargetClass(self):
        from pyrtos.models import Income
        return Income

    def _makeOne(self, id, title, amount):
        return self._getTargetClass()(id=id,\
                                      title=title,\
                                      user_id=1,\
                                      amount=amount)

    def test_constructor(self):
        instance = self._makeOne(100, 'Test', 1234)
        self.session.add(instance)

        qi = self._getTargetClass().by_id(100)
        self.assertEqual(qi.title, 'Test')
        self.assertEqual(qi.amount, 1234)


class ExpenditureModelTests(BaseTestCase):

    def _getTargetClass(self):
        from pyrtos.models import Expenditure
        return Expenditure

    def _makeOne(self, id, title, amount):
        return self._getTargetClass()(id=id,\
                                      title=title,\
                                      amount=amount,\
                                      category_id=1,\
                                      user_id=1)

    def test_constructor(self):
        instance = self._makeOne(100, 'Test', 1234)
        self.session.add(instance)

        qi = self._getTargetClass().by_id(100)
        self.assertEqual(qi.title, 'Test')
        self.assertEqual(qi.amount, 1234)


class InvoiceModelTests(BaseTestCase):
    
    def _getTargetClass(self):
        from pyrtos.models import Invoice
        return Invoice

    def _makeOne(self, id, title, amount):
        return self._getTargetClass()(id=id,\
                                      title=title,\
                                      amount=amount,\
                                      due=datetime.utcnow(),\
                                      category_id=1,\
                                      creditor_id=1,\
                                      user_id=1)

    def test_constructor(self):
        instance = self._makeOne(1, 'Test', 1234)
        self.session.add(instance)

        qi = self._getTargetClass().by_id(1)
        self.assertEqual(qi.title, 'Test')
        self.assertEqual(qi.amount, 1234)
        
        css_time = instance.css_class_for_time_distance()
        self.assertEqual(css_time, 'expired')

        time_to = instance.time_to_expires_in_words()
        self.assertIn('less', time_to)

        instance.due = datetime.utcnow()+timedelta(days=10)
        css_time = instance.css_class_for_time_distance()
        self.assertEqual(css_time, 'd10')
        
        time_to = instance.time_to_expires_in_words()
        self.assertIn('10 days', time_to)


class ViewTests(BaseTestCase):

    def test_index(self):
        from pyrtos.views import MainViews
        request = testing.DummyRequest()
        m = MainViews(request)
        response = m.index()
        self.assertEqual(response['title'], 'Dashboard')

    def test_notfound(self):
        from pyrtos.views import MainViews
        request = testing.DummyRequest()
        m = MainViews(request)
        response = m.notfound()
        self.assertEqual(response['title'], '404 - Page not found')

    def test_login(self):
        from pyrtos.views import AuthViews
        request = testing.DummyRequest()
        request.POST = multidict.MultiDict()
        a = AuthViews(request)
        response = a.login()
        self.assertEqual(response['title'], 'Login')

    def test_categories(self):
        from pyrtos.views import CategoryViews
        request = testing.DummyRequest()
        c = CategoryViews(request)
        response = c.categories()
        self.assertEqual(response['title'], 'Shared categories')

    def test_private_categories(self):
        from pyrtos.views import CategoryViews
        request = testing.DummyRequest()
        c = CategoryViews(request)
        response = c.categories_private()
        self.assertEqual(response['title'], 'Private categories')

    def test_archived_categories(self):
        from pyrtos.views import CategoryViews
        request = testing.DummyRequest()
        c = CategoryViews(request)
        response = c.categories_archived()
        self.assertEqual(response['title'], 'Archived categories')

    def test_category_create(self):
        from pyrtos.views import CategoryViews
        request = testing.DummyRequest()
        request.POST = multidict.MultiDict()
        request.matchdict = {'name' : 'test'}
        c = CategoryViews(request)
        response = c.category_create()
        self.assertEqual(response['title'], 'New category')

    def test_tags(self):
        from pyrtos.views import TagViews
        request = testing.DummyRequest()
        t = TagViews(request)
        response = t.tags()
        self.assertEqual(response['title'], 'Tags')

    def test_users(self):
        from pyrtos.views import UserViews
        request = testing.DummyRequest()
        u = UserViews(request)
        response = u.users()
        self.assertEqual(response['title'], 'Users')

    def test_archived_users(self):
        from pyrtos.views import UserViews
        request = testing.DummyRequest()
        u = UserViews(request)
        response = u.users_archived()
        self.assertEqual(response['title'], 'Archived users')

    def test_new_user(self):
        from pyrtos.views import UserViews
        request = testing.DummyRequest()
        request.POST = multidict.MultiDict()
        u = UserViews(request)
        response = u.user_create()
        self.assertEqual(response['title'], 'New user')

    def test_creditor(self):
        from pyrtos.views import CreditorViews
        request = testing.DummyRequest()
        c = CreditorViews(request)
        response = c.creditors()
        self.assertEqual(response['title'], 'Shared creditors')

    def test_creditor_private(self):
        from pyrtos.views import CreditorViews
        request = testing.DummyRequest()
        c = CreditorViews(request)
        response = c.creditors_private()
        self.assertEqual(response['title'], 'Private creditors')

    def test_archived_creditors(self):
        from pyrtos.views import CreditorViews
        request = testing.DummyRequest()
        c = CreditorViews(request)
        response = c.creditors_archived()
        self.assertEqual(response['title'], 'Archived creditors')

    def test_creditor_new(self):
        from pyrtos.views import CreditorViews
        request = testing.DummyRequest()
        request.POST = multidict.MultiDict()
        c = CreditorViews(request)
        response = c.creditor_create()
        self.assertEqual(response['title'], 'New creditor')

    def test_income(self):
        from pyrtos.views import IncomeViews
        request = testing.DummyRequest()
        i = IncomeViews(request)
        response = i.incomes()
        self.assertEqual(response['title'], 'Monthly incomes')

    def test_income_archived(self):
        from pyrtos.views import IncomeViews
        request = testing.DummyRequest()
        i = IncomeViews(request)
        response = i.incomes_archived()
        self.assertEqual(response['title'], 'Archived incomes')

    def test_income_new(self):
        from pyrtos.views import IncomeViews
        request = testing.DummyRequest()
        request.POST = multidict.MultiDict()
        i = IncomeViews(request)
        response = i.income_create()
        self.assertEqual(response['title'], 'New income')

    def test_expenditures(self):
        from pyrtos.views import ExpenditureViews
        request = testing.DummyRequest()
        e = ExpenditureViews(request)
        response = e.expenditures()
        self.assertEqual(response['title'], 'Shared expenditures')

    def test_expenditures_archived(self):
        from pyrtos.views import ExpenditureViews
        request = testing.DummyRequest()
        e = ExpenditureViews(request)
        response = e.expenditures_archived()
        self.assertEqual(response['title'], 'Archived expenditures')
    
    def test_invoice(self):
        from pyrtos.views import InvoiceViews
        request = testing.DummyRequest()
        i = InvoiceViews(request)
        response = i.invoices()
        self.assertEqual(response['title'], 'Shared invoices')

    def test_invoice_archived(self):
        from pyrtos.views import InvoiceViews
        request = testing.DummyRequest()
        i = InvoiceViews(request)
        response = i.invoices_archived()
        self.assertEqual(response['title'], 'Archived invoices')

    def test_invoice_search(self):
        from pyrtos.views import InvoiceViews
        request = testing.DummyRequest()
        i = InvoiceViews(request)
        response = i.invoices_search()
        self.assertEqual(response['title'], 'Search')

    def test_invoice_month_switcher(self):
        from pyrtos.views import InvoiceViews
        request = testing.DummyRequest()
        i = InvoiceViews(request)
        r = i.month_switcher(2013, 5)
        self.assertEqual(r[0], 2013)
        self.assertEqual(r[1], 4)

        r = i.month_switcher(2013, 12, next=True)
        self.assertEqual(r[0], 2014)
        self.assertEqual(r[1], 1)

        r = i.month_switcher(2013, 1)
        self.assertEqual(r[0], 2012)
        self.assertEqual(r[1], 12)


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

    def test_creditors_as_anonymous(self):
        res = self.app.get('/creditors', status=302)
        self.assertTrue(res.location, 'http://localhost/login')

    def test_users_as_anonymous(self):
        res = self.app.get('/users', status=302)
        self.assertTrue(res.location, 'http://localhost/login')

    def test_categories(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'user@email.com',
                                       'password' : '1234567',}
                           )

        # create a new user
        res = self.app.get('/user/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/user/new', {'email' : 'test@email.com',
                                          'givenname' : 'testy',
                                          'surname' : 'mctest',
                                          'password' : '123456',
                                          'confirm' : '123456',
                                          'group' : 'admin',
                                          'csrf_token' : token})

        res = self.app.get('/categories')
        self.assertTrue(res.status_int, 200)

        res = self.app.get('/category/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/category/new', {'title' : 'testbest',
                                              'csrf_token' : token}
                           )
        res = self.app.get('/categories', status=200)
        self.assertTrue('testbest' in res.body)

        res = self.app.get('/category/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/category/edit/1', params={'id' : 1,
                                                        'title' : 'besttest',
                                                        'csrf_token' : token}
                           )
        categories = self.app.get('/categories', status=200)
        self.assertTrue('besttest' in categories.body)

        res = self.app.get('/category/edit/1', status=200)
        self.assertTrue('besttest' in res.body)

        res = self.app.get('/category/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/category/edit/1', params={'id' : 1,
                                                        'title' : 'besttest',
                                                        'private' : 'y',
                                                        'csrf_token' : token}
                           )

        res = self.app.get('/categories/private', status=200)
        self.assertTrue('besttest' in res.body)

        res = self.app.get('/categories', status=200)
        self.assertFalse('besttest' in res.body)


        self.app.get('/category/archive/1', status=302)
        res = self.app.get('/categories/archived', status=200)
        self.assertTrue('besttest' in res.body)

        self.app.get('/category/restore/1', status=302)
        res = self.app.get('/categories', status=200)
        self.assertTrue('besttest' in res.body)

        self.app.get('/category/edit/100', status=404)
        self.app.get('/category/archive/100', status=404)
        self.app.get('/category/restore/100', status=404)

        # logout 
        self.app.get('/logout')

        # login with the previously created user
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'test@email.com',
                                       'password' : '123456',}
                           )

        # try to edit a category the user do not have permission to
        self.app.get('/category/edit/1', status=403)
        # try to archive a category the user do not have permission to
        self.app.get('/category/archive/1', status=403)
        # try to restore a category the user do not have permission to
        self.app.get('/category/restore/1', status=403)


    def test_users(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'user@email.com',
                                       'password' : '1234567',}
                           )
        res = self.app.get('/users', status=200)
        self.assertTrue(res.status_int, 200)
        
        res = self.app.get('/user/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/user/new', {'email' : 'test@email.com',
                                          'givenname' : 'testy',
                                          'surname' : 'mctest',
                                          'password' : '123456',
                                          'confirm' : '123456',
                                          'group' : 'admin',
                                          'csrf_token' : token})
        res = self.app.get('/users', status=200)
        self.assertTrue('test@email.com' in res.body)

        res = self.app.get('/users/archived', status=200)
        self.assertTrue('No users found' in res.body)

        res = self.app.get('/user/edit/2', status=200)
        self.assertTrue('test@email.com' in res.body)
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/user/edit/2', {'id' : 2,
                                             'email' : 'best@email.com',
                                             'password' : '123456',
                                             'confirm' : '123456',
                                             'group' : 'admin',
                                             'csrf_token' : token,
                                             })
        res = self.app.get('/users', status=200)
        self.assertTrue('best@email.com')

        self.app.get('/logout', status=302)

        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'best@email.com',
                                       'password' : '123456',
                                      }, status=302 )

        res = self.app.get('/users', status=200)
        self.assertTrue(res.status_int, 200)

        res = self.app.get('/user/edit/1', status=404)

        self.app.get('/logout', status=302)

        # block user
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'user@email.com',
                                       'password' : '1234567',}
                           )
        res = self.app.get('/user/edit/2', status=200)
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/user/edit/2', {'id' : 2,
                                             'email' : 'best@email.com',
                                             'csrf_token' : token,
                                             'password' : '',
                                             'confirm' : '',
                                             'blocked' : 'y',
                                             })
        self.app.get('/logout', status=302)
        
        # test login with blocked user
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'best@email.com',
                                       'password' : '123456',}
                           , status=200)
        self.assertTrue('Login failed' in res.body)

        # test unblock user and login
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'user@email.com',
                                       'password' : '1234567',}
                           )
        res = self.app.get('/user/edit/2', status=200)
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/user/edit/2', {'id' : 2,
                                             'email' : 'best@email.com',
                                             'csrf_token' : token,
                                             'password' : '',
                                             'confirm' : '',
                                             })
        self.app.get('/logout', status=302)

        # log back in with unblocked user
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'best@email.com',
                                       'password' : '123456',}
                           , status=302)
        self.app.get('/logout', status=302)

        # log in and archive 
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'user@email.com',
                                       'password' : '1234567',}
                           )
        self.app.get('/user/archive/1', status=404)
        self.app.get('/user/archive/2', status=302)
        self.app.get('/logout', status=302)

        #try to log in with archived user
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'best@email.com',
                                       'password' : '123456',}
                           , status=200)
        self.assertTrue('Login failed' in res.body)

        # log back in with unblocked user
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'user@email.com',
                                       'password' : '1234567',}
                           , status=302)
        self.app.get('/user/restore/2', status=302)
        self.app.get('/logout', status=302)

        # log back in with unarchived user
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'best@email.com',
                                       'password' : '123456',}
                           , status=302)
        self.app.get('/logout', status=302)

    def test_user_404(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                           'csrf_token' : token,
                                           'email': 'user@email.com',
                                           'password' : '1234567',}
                               )
        self.app.get('/user/edit/100', status=404)
        self.app.get('/user/archive/100', status=404)
        self.app.get('/user/restore/100', status=404)

    def test_user_bogus_data(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                           'csrf_token' : token,
                                           'email': 'user@email.com',
                                           'password' : '1234567',}
                               )
        res = self.app.get('/user/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/user/new', {'email' : 'mustang@email.com',
                                          'givenname' : 'mustang',
                                          'surname' : 'mcmustang',
                                          'password' : '123456',
                                          'confirm' : '123456',
                                          'group' : 'horse',
                                          'csrf_token' : token},
                           status=200)
        res = self.app.post('/user/new', {'email' : 'mustang@email.com',
                                          'givenname' : 'mustang',
                                          'surname' : 'mcmustang',
                                          'password' : '123456',
                                          'confirm' : '123456',
                                          'group' : 'viewer',
                                          'csrf_token' : token},
                           status=302)
        res = self.app.get('/users')
        self.assertFalse('horse' in res.body)
        self.assertTrue('viewer' in res.body)
        self.assertTrue('mustang@email.com' in res.body)

        res = self.app.get('/user/edit/2', status=200)
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/user/edit/2', {'id' : 2,
                                             'email' : 'mustang@email.com',
                                             'group' : 'horse',
                                             'csrf_token' : token},
                           status=200)
        self.assertFalse('horse' in res.body)
        self.assertTrue('viewer' in res.body)
        res = self.app.get('/users')
        self.assertFalse('horse' in res.body)
        self.assertTrue('viewer' in res.body)
        self.assertTrue('mustang@email.com' in res.body)

        res = self.app.get('/user/edit/2', status=200)
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/user/edit/2', {'id' : 2,
                                             'email' : 'mustang@email.com',
                                             'group' : 'horse',
                                             'csrf_token' : token},
                           status=200)
        self.assertFalse('horse' in res.body)
        self.assertTrue('viewer' in res.body)

    def test_creditors(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'user@email.com',
                                       'password' : '1234567',}
                           )

        # create a new user
        res = self.app.get('/user/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/user/new', {'email' : 'test@email.com',
                                          'givenname' : 'testy',
                                          'surname' : 'mctest',
                                          'password' : '123456',
                                          'confirm' : '123456',
                                          'group' : 'admin',
                                          'csrf_token' : token})

        res = self.app.get('/creditors')
        self.assertTrue(res.status_int, 200)

        res = self.app.get('/creditor/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/creditor/new', {'title' : 'testbest',
                                              'csrf_token' : token}
                           )
        res = self.app.get('/creditors', status=200)
        self.assertTrue('testbest' in res.body)

        res = self.app.get('/creditor/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/creditor/edit/1', params={'id' : 1,
                                                        'title' : 'besttest',
                                                        'csrf_token' : token}
                           )
        res = self.app.get('/creditors', status=200)
        self.assertTrue('besttest' in res.body)

        res = self.app.get('/creditor/edit/1', status=200)
        self.assertTrue('besttest' in res.body)

        res = self.app.get('/creditor/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/creditor/edit/1', params={'id' : 1,
                                                        'title' : 'besttest',
                                                        'private' : 'y',
                                                        'csrf_token' : token}
                           )
        res = self.app.get('/creditors/private', status=200)
        self.assertTrue('besttest' in res.body)
        res = self.app.get('/creditors', status=200)
        self.assertFalse('besttest' in res.body)

        self.app.get('/creditor/archive/1', status=302)
        res = self.app.get('/creditors/archived', status=200)
        self.assertTrue('besttest' in res.body)

        self.app.get('/creditor/restore/1', status=302)
        res = self.app.get('/creditors', status=200)
        self.assertTrue('besttest' in res.body)

        self.app.get('/creditor/edit/100', status=404)
        self.app.get('/creditor/archive/100', status=404)
        self.app.get('/creditor/restore/100', status=404)

        # logout 
        self.app.get('/logout')

        # login with the previously created user
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'test@email.com',
                                       'password' : '123456',}
                           )

        # try to edit a creditor the user do not have permission to
        self.app.get('/creditor/edit/1', status=403)
        # try to archive a creditor the user do not have permission to
        self.app.get('/creditor/archive/1', status=403)
        # try to restore a creditor the user do not have permission to
        self.app.get('/creditor/restore/1', status=403)


    def test_incomes(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'user@email.com',
                                       'password' : '1234567',}
                           )
        res = self.app.get('/incomes')
        self.assertTrue(res.status_int, 200)

        res = self.app.get('/income/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/income/new', {'title' : 'testbest',
                                            'amount' : '12345',
                                            'user_id' : 1,
                                            'csrf_token' : token}
                           )
        res = self.app.get('/incomes', status=200)
        self.assertTrue('testbest' in res.body)

        res = self.app.get('/income/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/income/edit/1', params={'id' : 1,
                                                      'title' : 'besttest',
                                                      'amount' : '12345',
                                                      'user_id' : 1,
                                                      'csrf_token' : token}
                           )
        res = self.app.get('/incomes', status=200)
        self.assertTrue('besttest' in res.body)

        res = self.app.get('/income/edit/1', status=200)
        self.assertTrue('besttest' in res.body)
        res = self.app.get('/income/edit/100', status=404)

        self.app.get('/income/archive/1', status=302)
        res = self.app.get('/incomes/archived', status=200)
        self.assertTrue('besttest' in res.body)

        self.app.get('/income/restore/1', status=302)
        res = self.app.get('/incomes', status=200)
        self.assertTrue('besttest' in res.body)

        self.app.get('/income/edit/100', status=404)
        self.app.get('/income/archive/100', status=404)
        self.app.get('/income/restore/100', status=404)


    def test_expenditures(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'user@email.com',
                                       'password' : '1234567',}
                           )

        # create a new user
        res = self.app.get('/user/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/user/new', {'email' : 'test@email.com',
                                          'givenname' : 'testy',
                                          'surname' : 'mctest',
                                          'password' : '123456',
                                          'confirm' : '123456',
                                          'group' : 'admin',
                                          'csrf_token' : token})

        res = self.app.get('/expenditures')
        self.assertTrue(res.status_int, 200)

        res = self.app.get('/expenditures?private=1')
        self.assertTrue(res.status_int, 200)

        res = self.app.get('/expenditure/new', status=302)
        res = self.app.get('/expenditure/new?private=1', status=302)

        # new pub category
        res = self.app.get('/category/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/category/new', {'title' : 'testbest',
                                              'csrf_token' : token}
                           )

        # new priv category
        res = self.app.get('/category/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/category/new', {'title' : 'hestbest',
                                              'private' : 'y',
                                              'csrf_token' : token}
                           )
        
        # new pub expenditure
        res = self.app.get('/expenditure/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/expenditure/new', {'title' : 'testbest',
                                                 'amount' : '12345',
                                                 'category_id' : 1,
                                                 'csrf_token' : token}
                           )
        res = self.app.get('/expenditures', status=200)
        self.assertTrue('testbest' in res.body)

        # new priv expenditure
        res = self.app.get('/expenditure/new?private=1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/expenditure/new?private=1', {'title' : 'testbest',
                                                           'amount' : '12345',
                                                           'category_id' : 2,
                                                           'csrf_token' : token}
                                     )
        res = self.app.get('/expenditures?private=1', status=200)
        self.assertTrue('testbest' in res.body)

        # edit public expenditure
        res = self.app.get('/expenditure/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/expenditure/edit/1', params={'id' : 1,
                                                      'title' : 'besttest',
                                                      'amount' : '12345',
                                                      'category_id' : 1,
                                                      'csrf_token' : token}
                           )
        res = self.app.get('/expenditures', status=200)
        self.assertTrue('besttest' in res.body)
        
        # edit priv expenditure
        res = self.app.get('/expenditure/edit/2?private=1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/expenditure/edit/2?private=1', params={'id' : 2,
                                                                     'title' : 'testhest',
                                                                     'amount' : '12345',
                                                                     'category_id' : 2,
                                                                     'csrf_token' : token}
                           )
        res = self.app.get('/expenditures?private=1', status=200)
        self.assertTrue('testhest' in res.body)

        res = self.app.get('/expenditure/edit/1', status=200)
        self.assertTrue('besttest' in res.body)
        res = self.app.get('/expenditure/edit/100', status=404)

        # archive the public category
        self.app.get('/category/archive/1', status=302)
        # try to edit public the expenditure without public category
        self.app.get('/expenditure/edit/1', status=302)

        # archive the private category
        self.app.get('/category/archive/2', status=302)
        # try to edit the private expenditure without the private category
        self.app.get('/expenditure/edit/2?private=1', status=302)

        self.app.get('/expenditure/archive/1', status=302)
        res = self.app.get('/expenditures/archived', status=200)
        self.assertTrue('besttest' in res.body)

        self.app.get('/expenditure/restore/1', status=302)
        res = self.app.get('/expenditures', status=200)
        self.assertTrue('besttest' in res.body)

        self.app.get('/expenditure/edit/100', status=404)
        self.app.get('/expenditure/archive/100', status=404)
        self.app.get('/expenditure/restore/100', status=404)

        # logout 
        self.app.get('/logout')

        # login with the previously created user
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'test@email.com',
                                       'password' : '123456',}
                           )

        # try to edit an expenditure the user do not have permission to
        self.app.get('/expenditure/edit/2', status=403)
        # try to archive an expenditure the user do not have permission to
        self.app.get('/expenditure/archive/2', status=403)
        # try to restore an expenditure the user do not have permission to
        self.app.get('/expenditure/restore/2', status=403)

    def test_invoices(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'user@email.com',
                                       'password' : '1234567',}
                           )

        # create a new user
        res = self.app.get('/user/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/user/new', {'email' : 'test@email.com',
                                          'givenname' : 'testy',
                                          'surname' : 'mctest',
                                          'password' : '123456',
                                          'confirm' : '123456',
                                          'group' : 'admin',
                                          'csrf_token' : token})

        res = self.app.get('/invoices')
        self.assertTrue(res.status_int, 200)

        res = self.app.get('/invoices?private=1')
        self.assertTrue(res.status_int, 200)

        self.app.get('/invoice/new', status=302)
        self.app.get('/invoice/new?private=1', status=302)

        # new pub category
        res = self.app.get('/category/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/category/new', {'title' : 'testbest',
                                              'csrf_token' : token}
                           )

        self.app.get('/invoice/new', status=302)
        self.app.get('/invoice/new?private=1', status=302)

        # new pub creditor
        res = self.app.get('/creditor/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/creditor/new', {'title' : 'testbest',
                                              'csrf_token' : token}
                           )

        self.app.get('/invoice/new', status=200)
        self.app.get('/invoice/new?private=1', status=302)

        # new pub invoice
        res = self.app.get('/invoice/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/invoice/new', {'title' : 'testbest',
                                             'amount' : '12345',
                                             'category_id' : 1,
                                             'due' : '2013-07-07',
                                             'creditor_id' : 1,
                                             'csrf_token' : token}
                           )
        res = self.app.get('/invoices', status=200)
        self.assertTrue('testbest' in res.body)
        
        # edit public invoice
        res = self.app.get('/invoice/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/invoice/edit/1', params={'id' : 1,
                                                      'title' : 'besttest',
                                                      'amount' : '12345',
                                                      'paid' : '2013-07-07',
                                                      'category_id' : 1,
                                                      'creditor_id' : 1,
                                                      'csrf_token' : token}
                           )
        res = self.app.get('/invoices', status=200)
        self.assertTrue('besttest' in res.body)

        # try to convert public invoice to private without private catgory
        self.app.get('/invoice/edit/1?private=1', status=302)

        # new priv category
        res = self.app.get('/category/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/category/new', {'title' : 'hestbest',
                                              'private' : 'y',
                                              'csrf_token' : token}
                           )

        # try to convert public invoice to private without private creditor
        self.app.get('/invoice/edit/1?private=1', status=302)

        # try to create a private invoice without private creditor
        self.app.get('/invoice/new?private=1', status=302)

        # new priv creditor
        res = self.app.get('/creditor/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/creditor/new', {'title' : 'hestbest',
                                              'private' : 'y',
                                              'csrf_token' : token}
                           )

        # try to convert public invoice to private with private creditor and category
        self.app.get('/invoice/edit/1?private=1', status=200)

        # new priv invoice
        res = self.app.get('/invoice/new?private=1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/invoice/new?private=1', {'title' : 'testbest',
                                                       'amount' : '12345',
                                                       'category_id' : 2,
                                                       'due' : '2013-07-07',
                                                       'creditor_id' : 2,
                                                       'csrf_token' : token}
                           )
        res = self.app.get('/invoices?private=1', status=200)
        self.assertTrue('testbest' in res.body)

        
        # edit priv invoice
        res = self.app.get('/invoice/edit/2?private=1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/invoice/edit/2?private=1', params={'id' : 2,
                                                                 'title' : 'testhest',
                                                                 'amount' : '12345',
                                                                 'category_id' : 2,
                                                                 'creditor_id' : 2,
                                                                 'csrf_token' : token}
                           )
        res = self.app.get('/invoices?private=1', status=200)
        self.assertTrue('testhest' in res.body)

        res = self.app.get('/invoice/edit/1', status=200)
        self.assertTrue('besttest' in res.body)
        res = self.app.get('/invoice/edit/100', status=404)

        # archive the public category
        self.app.get('/category/archive/1', status=302)
        # try to edit public the invoice without public category
        self.app.get('/invoice/edit/1', status=302)
        # restore the public category
        self.app.get('/category/restore/1', status=302)
        # archive the public creditor
        self.app.get('/creditor/archive/1', status=302)
        # try to edit the public invoice without the public creditor
        self.app.get('/invoice/edit/1', status=302)

        # archive the private category
        self.app.get('/category/archive/2', status=302)
        # try to edit the private invoice without the private category
        self.app.get('/invoice/edit/2?private=1', status=302)
        # restore the private category
        self.app.get('/category/restore/2', status=302)
        # archive the private creditor
        self.app.get('/creditor/archive/2', status=302)
        # try to edit the private invoice without the private creditor
        self.app.get('/invoice/edit/2?private=1', status=302)
        # restore the private creditor
        self.app.get('/creditor/restore/2', status=302)

        # archive public invoice
        self.app.get('/invoice/archive/1', status=302)
        res = self.app.get('/invoices/archived', status=200)
        self.assertTrue('besttest' in res.body)
        
        # restore public invoice
        self.app.get('/invoice/restore/1', status=302)
        res = self.app.get('/invoices', status=200)
        self.assertTrue('besttest' in res.body)

        # edit public invoice
        self.app.get('/category/restore/1', status=302)
        self.app.get('/creditor/restore/1', status=302)
        res = self.app.get('/invoice/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/invoice/edit/1', params={'id' : 1,
                                                      'title' : 'besttest',
                                                      'amount' : '12345',
                                                      'category_id' : 1,
                                                      'creditor_id' : 1,
                                                      'csrf_token' : token}
                           )
        # try to quickpay the invoice
        self.app.get('/invoice/quickpay/1', status=302)

        # visit the query page
        res = self.app.get('/invoices/search', status=200)
        self.assertIn('Search', res.body)

        self.app.get('/invoice/edit/100', status=404)
        self.app.get('/invoice/archive/100', status=404)
        self.app.get('/invoice/restore/100', status=404)
        self.app.get('/invoice/quickpay/100', status=404)

        # logout
        self.app.get('/logout')

        # login with the previously created user
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'test@email.com',
                                       'password' : '123456',}
                           )

        # try to edit an invoice the user do not have permission to
        self.app.get('/invoice/edit/2', status=403)
        self.app.get('/invoice/quickpay/2', status=403)
        # try to archive an invoice the user do not have permission to
        self.app.get('/invoice/archive/2', status=403)
        # try to restore an invoice the user do not have permission to
        self.app.get('/invoice/restore/2', status=403)

        # logout
        self.app.get('/logout')

        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'user@email.com',
                                       'password' : '1234567',}
                           )

        # set private category shared
        res = self.app.get('/category/edit/2')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/category/edit/2', {'id' : 2,
                                                 'title' : 'hestbest',
                                                 'csrf_token' : token}
                           )

        # logout
        self.app.get('/logout')

        # login with the previously created user
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'test@email.com',
                                       'password' : '123456',}
                           )

        # try to edit an invoice the user do not have permission to
        self.app.get('/invoice/edit/2', status=403)
        self.app.get('/invoice/quickpay/2', status=403)
        # try to archive an invoice the user do not have permission to
        self.app.get('/invoice/archive/2', status=403)
        # try to restore an invoice the user do not have permission to
        self.app.get('/invoice/restore/2', status=403)
