from datetime import (
    datetime,
    timedelta,
    date,
)

from pyramid import testing
from webob import multidict

from pyrtos.tests import BaseTestCase

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
        self.assertEqual(response['title'], 'Categories')

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
        self.assertEqual(response['title'], 'Creditors')

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
        self.assertEqual(response['title'], 'Invoices')

    def test_invoice_archived(self):
        from pyrtos.views import InvoiceViews
        request = testing.DummyRequest()
        i = InvoiceViews(request)
        response = i.invoices_archived()
        self.assertEqual(response['title'], 'Archived invoices')

    def test_invoice_search(self):
        from pyrtos.views import InvoiceViews
        request = testing.DummyRequest()
        request.GET = multidict.MultiDict()
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

    def test_files(self):
        from pyrtos.views import FileViews
        request = testing.DummyRequest()
        f = FileViews(request)
        r = f.files()
        self.assertEqual(r['title'], 'Files')

    def test_files_archived(self):
        from pyrtos.views import FileViews
        request = testing.DummyRequest()
        f = FileViews(request)
        r = f.files_archived()
        self.assertEqual(r['title'], 'Archived files')
