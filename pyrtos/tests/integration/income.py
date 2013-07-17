from webtest import TestApp
from pyrtos.tests.integration import IntegrationTestBase
from pyrtos.tests.integration import _initTestingDB


class IntegrationIncomeViews(IntegrationTestBase):

    def setUp(self):
        self.app = TestApp(self.app)
        self.session = _initTestingDB(makeuser=True)

    def tearDown(self):
        del self.app
        self.session.remove()

    def test_incomes(self):
        res = self.app.get('/login')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/login', {'submit': True,
                                       'csrf_token': token,
                                       'email': 'user@email.com',
                                       'password': '1234567',
                                       }
                            )

        res = self.app.get('/incomes')
        self.assertTrue(res.status_int, 200)

        res = self.app.get('/income/new')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/income/new', {'title': 'testbest',
                                            'amount': '12345',
                                            'user_id': 1,
                                            'csrf_token': token,
                                            }
                            )
        res = self.app.get('/incomes', status=200)
        self.assertTrue('testbest' in res.body)

        res = self.app.get('/income/edit/1')
        token = res.form.fields['csrf_token'][0].value
        res = self.app.post('/income/edit/1', params={'id': 1,
                                                      'title': 'besttest',
                                                      'amount': '12345',
                                                      'user_id': 1,
                                                      'csrf_token': token,
                                                      }
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
