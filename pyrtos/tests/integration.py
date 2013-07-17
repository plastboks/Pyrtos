import transaction

from pyramid import testing
from webtest import TestApp
from sqlalchemy import create_engine
from cryptacular.bcrypt import BCRYPTPasswordManager as BPM
from pyrtos import main
from pyrtos.models.meta import DBSession, Base
from pyrtos.tests import BaseTestCase

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


class IntegrationTestBase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        settings = {'sqlalchemy.url' : 'sqlite://'}
        cls.app = main({}, **settings)
        super(IntegrationTestBase, cls).setUpClass()
   
    """
    def setUp(self):
        self.app = TestApp(self.app)
        self.config = testing.setUp()
        super(IntegrationTestBase, self).setUp()
    """


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

        self.app.get('/category/archive/1', status=302)
        res = self.app.get('/categories/archived', status=200)
        self.assertTrue('besttest' in res.body)

        self.app.get('/category/restore/1', status=302)

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
        self.assertIn('No paid invoices', res.body)
        
        # try to create a new invoice without categories and creditors
        self.app.get('/invoice/new', status=302)
        self.app.get('/invoice/new?private=1', status=302)

        # new pub category
        res = self.app.get('/category/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/category/new', {'title' : 'testbest',
                                              'csrf_token' : token}
                           )

        # try to create a new invoice without creditors
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
                                             'due' : '2013-07-07',
                                             'category_id' : 1,
                                             'creditor_id' : 1,
                                             'csrf_token' : token},
                            upload_files=[('attachment', 'foo.pdf', b'foo')],
                            status=302)

        #res = self.app.get('/invoices', status=200)
        #self.assertTrue('testbest' in res.body)
        
        # edit public invoice
        res = self.app.get('/invoice/edit/1')
        self.assertIn('testbest', res.body)
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/invoice/edit/1', params={'id' : 1,
                                                      'title' : 'besttest',
                                                      'amount' : '12345',
                                                      'paid' : '2013-07-07',
                                                      'files-0' : 1,
                                                      'category_id' : 1,
                                                      'creditor_id' : 1,
                                                      'csrf_token' : token},
                            upload_files=[('attachment', 'boo.pdf', b'boo')],
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
        self.assertIn('hestbest', res.body)
        self.assertFalse('testbest' in res.body)
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/invoice/new?private=1', {'title' : 'testbest',
                                                       'amount' : '12345',
                                                       'due' : '2013-07-07',
                                                       'category_id' : 2,
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
                                                                 'csrf_token' : token},
                            upload_files=[('attachment', 'coo.pdf', b'coo')],
                           )
        res = self.app.get('/invoices?private=1', status=200)
        self.assertTrue('testhest' in res.body)

        res = self.app.get('/invoice/edit/1', status=200)
        self.assertTrue('besttest' in res.body)
        res = self.app.get('/invoice/edit/100', status=404)

        # new priv invoice
        res = self.app.get('/invoice/new?private=1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/invoice/new?private=1', {'title' : 'testpriv',
                                                       'amount' : '12345',
                                                       'due' : '2013-07-07',
                                                       'category_id' : 2,
                                                       'creditor_id' : 2,
                                                       'csrf_token' : token},
                            upload_files=[('attachment', 'doo.pdf', b'doo')],
                           )

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
        # to a testsearch
        token = res.form.fields['csrf_token'][0].value
        res = self.app.get('/invoices/search', {'submit': True,
                                                 'csrf_token' : token,
                                                 'categories' : 1,
                                                 'fromdate' : '2013-07-07',
                                                 'todate' : '2013-07-07',
                                                 'creditors' : 1,
                                                 'query' : 'test'}
                          )

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


    def test_files(self):
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


        res = self.app.get('/files')
        self.assertIn('Files', res.body)

        res = self.app.get('/file/new')
        self.assertIn('New file', res.body)
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/file/new',
                            {'submit' : True,
                             'csrf_token' : token,
                             'title' : 'foo',
                             'private' : 'y',
                            },
                            upload_files=[('file', 'foo.pdf', b'foo')],
                            status=302)

        res = self.app.get('/files')
        self.assertIn('foo', res.body)

        res = self.app.get('/file/download/1', status=200)

        # create one without a file...
        res = self.app.get('/file/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/file/new',
                            {'submit' : True,
                             'csrf_token' : token,
                             'title' : 'foo',
                             'private' : 'y',
                            },
                            status=302)

        res = self.app.get('/file/download/2', status=404)


        # try to get nonexisting file
        res = self.app.get('/file/download/100', status=404)

        # logout
        self.app.get('/logout')

        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit' : True,
                                       'csrf_token' : token,
                                       'email': 'test@email.com',
                                       'password' : '123456',}
                            , status=302)

        self.app.get('/file/download/1', status=403)
