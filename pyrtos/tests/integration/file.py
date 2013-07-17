from webtest import TestApp
from pyrtos.tests.integration import IntegrationTestBase
from pyrtos.tests.integration import _initTestingDB


class IntegrationFileViews(IntegrationTestBase):

    def setUp(self):
        self.app = TestApp(self.app)
        self.session = _initTestingDB(makeuser=True)

    def tearDown(self):
        del self.app
        self.session.remove()

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
