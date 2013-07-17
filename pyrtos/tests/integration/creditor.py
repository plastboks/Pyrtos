from webtest import TestApp
from pyrtos.tests.integration import IntegrationTestBase
from pyrtos.tests.integration import _initTestingDB


class IntegrationCreditorViews(IntegrationTestBase):

    def setUp(self):
        self.app = TestApp(self.app)
        self.session = _initTestingDB(makeuser=True)

    def tearDown(self):
        del self.app
        self.session.remove()

    def test_creditors(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit': True,
                                       'csrf_token': token,
                                       'email': 'user@email.com',
                                       'password': '1234567'}
                            )

        # create a new user
        res = self.app.get('/user/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/user/new', {'email': 'test@email.com',
                                          'givenname': 'testy',
                                          'surname': 'mctest',
                                          'password': '123456',
                                          'confirm': '123456',
                                          'group': 'admin',
                                          'csrf_token': token})

        res = self.app.get('/creditors')
        self.assertTrue(res.status_int, 200)

        res = self.app.get('/creditor/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/creditor/new', {'title': 'testbest',
                                              'csrf_token': token}
                            )
        res = self.app.get('/creditors', status=200)
        self.assertTrue('testbest' in res.body)

        res = self.app.get('/creditor/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/creditor/edit/1', params={'id': 1,
                                                        'title': 'besttest',
                                                        'csrf_token': token}
                            )
        res = self.app.get('/creditors', status=200)
        self.assertTrue('besttest' in res.body)

        res = self.app.get('/creditor/edit/1', status=200)
        self.assertTrue('besttest' in res.body)

        res = self.app.get('/creditor/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/creditor/edit/1', params={'id': 1,
                                                        'title': 'besttest',
                                                        'private': 'y',
                                                        'csrf_token': token}
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
        res = self.app.post('/login', {'submit': True,
                                       'csrf_token': token,
                                       'email': 'test@email.com',
                                       'password': '123456'}
                            )

        # try to edit a creditor the user do not have permission to
        self.app.get('/creditor/edit/1', status=403)
        # try to archive a creditor the user do not have permission to
        self.app.get('/creditor/archive/1', status=403)
        # try to restore a creditor the user do not have permission to
        self.app.get('/creditor/restore/1', status=403)
