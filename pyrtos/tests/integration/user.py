from webtest import TestApp
from pyrtos.tests.integration import IntegrationTestBase
from pyrtos.tests.integration import _initTestingDB


class IntegrationUserViews(IntegrationTestBase):

    def setUp(self):
        self.app = TestApp(self.app)
        self.session = _initTestingDB(makeuser=True)

    def tearDown(self):
        del self.app
        self.session.remove()

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


class IntegrationUserNotFoundViews(IntegrationTestBase):

    def setUp(self):
        self.app = TestApp(self.app)
        self.session = _initTestingDB(makeuser=True)

    def tearDown(self):
        del self.app
        self.session.remove()

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
