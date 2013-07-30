from webtest import TestApp
from pyrtos.tests.integration import IntegrationTestBase
from pyrtos.tests.integration import _initTestingDB


class IntegrationTagViews(IntegrationTestBase):

    def setUp(self):
        self.app = TestApp(self.app)
        self.session = _initTestingDB(makeuser=True)

    def tearDown(self):
        del self.app
        self.session.remove()

    def test_tags(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit': True,
                                       'csrf_token': token,
                                       'email': 'user@email.com',
                                       'password': '1234567'}
                            )

        """
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

        """
        res = self.app.get('/tags')
        self.assertTrue(res.status_int, 200)
        """
        res = self.app.get('/tag/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/tag/new', {'title': 'testbest',
                                              'csrf_token': token}
                            )
        res = self.app.get('/tags', status=200)
        self.assertTrue('testbest' in res.body)

        res = self.app.get('/tag/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/tag/edit/1', params={'id': 1,
                                                        'title': 'besttest',
                                                        'csrf_token': token}
                            )
        res = self.app.get('/tags', status=200)
        self.assertTrue('besttest' in res.body)

        res = self.app.get('/tag/edit/1', status=200)
        self.assertTrue('besttest' in res.body)

        res = self.app.get('/tag/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/tag/edit/1', params={'id': 1,
                                                        'title': 'besttest',
                                                        'private': 'y',
                                                        'csrf_token': token}
                            )

        self.app.get('/tag/archive/1', status=302)
        res = self.app.get('/tags/archived', status=200)
        self.assertTrue('besttest' in res.body)

        self.app.get('/tag/restore/1', status=302)
        res = self.app.get('/tags', status=200)
        self.assertTrue('besttest' in res.body)

        self.app.get('/tag/edit/100', status=404)
        self.app.get('/tag/archive/100', status=404)
        self.app.get('/tag/restore/100', status=404)

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

        # try to edit a tag the user do not have permission to
        self.app.get('/tag/edit/1', status=403)
        # try to archive a tag the user do not have permission to
        self.app.get('/tag/archive/1', status=403)
        # try to restore a tag the user do not have permission to
        self.app.get('/tag/restore/1', status=403)
        """
