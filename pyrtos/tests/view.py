from datetime import (
    datetime,
    timedelta,
    date,
)

from pyramid import testing
from webob import multidict

from pyrtos.tests import BaseTestCase

from pyrtos.views import (
    AuthViews,
    MainViews,
    CategoryViews,
    UserViews,
    TagViews,
    CreditorViews,
    IncomeViews,
    ExpenditureViews,
    InvoiceViews,
    FileViews,
    AlertSettingViews,
    ReminderViews,
    EventViews,
)


class BasicViewsTests(BaseTestCase):

    def test_index(self):
        request = testing.DummyRequest()
        m = MainViews(request)
        response = m.index()
        self.assertEqual(response['title'], 'Dashboard')

    def test_notfound(self):
        request = testing.DummyRequest()
        m = MainViews(request)
        response = m.notfound()
        self.assertEqual(response['title'], '404 - Page not found')

    def test_login(self):
        request = testing.DummyRequest()
        request.POST = multidict.MultiDict()
        a = AuthViews(request)
        response = a.login()
        self.assertEqual(response['title'], 'Login')


class CategoryViewsTests(BaseTestCase):

    def test_categories(self):
        request = testing.DummyRequest()
        c = CategoryViews(request)
        response = c.categories()
        self.assertEqual(response['title'], 'Categories')

    def test_archived_categories(self):
        request = testing.DummyRequest()
        c = CategoryViews(request)
        response = c.categories_archived()
        self.assertEqual(response['title'], 'Archived categories')

    def test_category_create(self):
        request = testing.DummyRequest()
        request.POST = multidict.MultiDict()
        request.matchdict = {'name': 'test'}
        c = CategoryViews(request)
        response = c.category_create()
        self.assertEqual(response['title'], 'New category')


class UserViewsTests(BaseTestCase):

    def test_users(self):
        request = testing.DummyRequest()
        u = UserViews(request)
        response = u.users()
        self.assertEqual(response['title'], 'Users')

    def test_new_user(self):
        request = testing.DummyRequest()
        request.POST = multidict.MultiDict()
        u = UserViews(request)
        response = u.user_create()
        self.assertEqual(response['title'], 'New user')

    def test_archived_users(self):
        request = testing.DummyRequest()
        u = UserViews(request)
        response = u.users_archived()
        self.assertEqual(response['title'], 'Archived users')


class TagViewsTests(BaseTestCase):

    def test_tags(self):
        request = testing.DummyRequest()
        t = TagViews(request)
        response = t.tags()
        self.assertEqual(response['title'], 'Tags')


class CreditorViewsTests(BaseTestCase):

    def test_creditor(self):
        request = testing.DummyRequest()
        c = CreditorViews(request)
        response = c.creditors()
        self.assertEqual(response['title'], 'Creditors')

    def test_archived_creditors(self):
        request = testing.DummyRequest()
        c = CreditorViews(request)
        response = c.creditors_archived()
        self.assertEqual(response['title'], 'Archived creditors')

    def test_creditor_new(self):
        request = testing.DummyRequest()
        request.POST = multidict.MultiDict()
        c = CreditorViews(request)
        response = c.creditor_create()
        self.assertEqual(response['title'], 'New creditor')


class IncomeViewsTests(BaseTestCase):

    def test_income(self):
        request = testing.DummyRequest()
        i = IncomeViews(request)
        response = i.incomes()
        self.assertEqual(response['title'], 'Monthly incomes')

    def test_income_archived(self):
        request = testing.DummyRequest()
        i = IncomeViews(request)
        response = i.incomes_archived()
        self.assertEqual(response['title'], 'Archived incomes')

    def test_income_new(self):
        request = testing.DummyRequest()
        request.POST = multidict.MultiDict()
        i = IncomeViews(request)
        response = i.income_create()
        self.assertEqual(response['title'], 'New income')


class ExpenditureViewsTests(BaseTestCase):

    def test_expenditures(self):
        request = testing.DummyRequest()
        e = ExpenditureViews(request)
        response = e.expenditures()
        self.assertEqual(response['title'], 'Shared expenditures')

    def test_expenditures_archived(self):
        request = testing.DummyRequest()
        e = ExpenditureViews(request)
        response = e.expenditures_archived()
        self.assertEqual(response['title'], 'Archived expenditures')


class InvoiceViewsTests(BaseTestCase):

    def test_invoice(self):
        request = testing.DummyRequest()
        i = InvoiceViews(request)
        response = i.invoices()
        self.assertEqual(response['title'], 'Invoices')

    def test_invoice_archived(self):
        request = testing.DummyRequest()
        i = InvoiceViews(request)
        response = i.invoices_archived()
        self.assertEqual(response['title'], 'Archived invoices')

    def test_invoice_search(self):
        request = testing.DummyRequest()
        request.GET = multidict.MultiDict()
        i = InvoiceViews(request)
        response = i.invoices_search()
        self.assertEqual(response['title'], 'Search')

    def test_invoice_month_switcher(self):
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


class FileViewsTests(BaseTestCase):

    def test_files(self):
        request = testing.DummyRequest()
        f = FileViews(request)
        r = f.files()
        self.assertEqual(r['title'], 'Files')

    def test_files_archived(self):
        request = testing.DummyRequest()
        f = FileViews(request)
        r = f.files_archived()
        self.assertEqual(r['title'], 'Archived files')


class AlertSettingViewsTest(BaseTestCase):

    def test_alertsettings(self):
        request = testing.DummyRequest()
        a = AlertSettingViews(request)
        r = a.alertsettings()
        self.assertEqual(r['title'], 'My alert settings')


class ReminderViewsTest(BaseTestCase):

    def test_reminders(self):
        request = testing.DummyRequest()
        r = ReminderViews(request)
        response = r.reminders()
        self.assertEqual(response['title'], 'Reminders')

    def test_reminders_inactive(self):
        request = testing.DummyRequest()
        r = ReminderViews(request)
        response = r.reminders_inactive()
        self.assertEqual(response['title'], 'Inactive reminders')


class EventViewsTest(BaseTestCase):

    def test_event(self):
        request = testing.DummyRequest()
        e = EventViews(request)
        r = e.events()
        self.assertEqual(r['title'], 'Events')

    def test_event_archived(self):
        request = testing.DummyRequest()
        e = EventViews(request)
        r = e.events_archived()
        self.assertEqual(r['title'], 'Archived events')
