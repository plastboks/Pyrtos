from webtest import TestApp
from pyrtos.tests.integration import IntegrationTestBase
from pyrtos.tests.integration import _initTestingDB


class IntegrationInvoiceViews(IntegrationTestBase):

    def setUp(self):
        self.app = TestApp(self.app)
        self.session = _initTestingDB(makeuser=True)

    def tearDown(self):
        del self.app
        self.session.remove()

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
