from webtest import TestApp
from pyrtos.tests.integration import IntegrationTestBase
from pyrtos.tests.integration import _initTestingDB

class IntegrationExpenditureViews(IntegrationTestBase):

    def setUp(self):
        self.app = TestApp(self.app)
        self.session = _initTestingDB(makeuser=True)

    def tearDown(self):
        del self.app
        self.session.remove()

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
