from datetime import (
    datetime,
    timedelta,
    date,
)

from cryptacular.bcrypt import BCRYPTPasswordManager as BPM
from pyrtos.tests import BaseTestCase


class UserModelTests(BaseTestCase):

    def _getTargetClass(self):
        from pyrtos.models import User
        return User

    def _makeOne(self, email, password, group, id=False):
        m = BPM()
        hashed = m.encode(password)
        if id:
          return self._getTargetClass()(id=id,
                                        email=email,
                                        password=hashed,
                                        group=group)
        return self._getTargetClass()(
                                      email=email,
                                      password=hashed,
                                      group=group)

    def test_constructor(self):
        instance = self._makeOne(
                                 email='user1@email.com',
                                 password='1234',
                                 group='admin',
                                 )
        self.assertEqual(instance.email, 'user1@email.com')
        self.assertTrue(instance.verify_password('1234'))

    def test_by_email(self):
        instance = self._makeOne(
                                 email='user2@email.com',
                                 password='1234',
                                 group='admin')
        self.session.add(instance)
        q = self._getTargetClass().by_email('user2@email.com')
        self.assertEqual(q.email, 'user2@email.com')

    def test_by_id(self):
        instance = self._makeOne(id=1000,
                                 email='user3@email.com',
                                 password='1234',
                                 group='admin')
        self.session.add(instance)
        q = self._getTargetClass().by_id(instance.id)
        self.assertEqual(q.email, 'user3@email.com')


class CategoryModelTests(BaseTestCase):

    def _getTargetClass(self):
        from pyrtos.models import Category
        return Category

    def _makeOne(self, id, title):
        return self._getTargetClass()(id=id, title=title, user_id=1)

    def test_constructor(self):
        instance = self._makeOne(100, 'Test')
        self.session.add(instance)

        qi = self._getTargetClass().by_id(100)
        self.assertEqual(qi.title, 'Test')


class TagModelTests(BaseTestCase):

    def _getTargetClass(self):
        from pyrtos.models import Tag
        return Tag

    def _makeOne(self, id, name):
        return self._getTargetClass()(id=id, name=name)

    def test_constructor(self):
        instance = self._makeOne(100, 'Test')
        self.session.add(instance)

        qi = self._getTargetClass().by_id(100)
        self.assertEqual(qi.name, 'Test')


class CreditorModelTests(BaseTestCase):

    def _getTargetClass(self):
        from pyrtos.models import Creditor
        return Creditor

    def _makeOne(self, id, title):
        return self._getTargetClass()(id=id, title=title, user_id=1)

    def test_constructor(self):
        instance = self._makeOne(100, 'Test')
        self.session.add(instance)

        qi = self._getTargetClass().by_id(100)
        self.assertEqual(qi.title, 'Test')


class IncomeModelTests(BaseTestCase):

    def _getTargetClass(self):
        from pyrtos.models import Income
        return Income

    def _makeOne(self, id, title, amount):
        return self._getTargetClass()(id=id,\
                                      title=title,\
                                      user_id=1,\
                                      amount=amount)

    def test_constructor(self):
        instance = self._makeOne(100, 'Test', 1234)
        self.session.add(instance)

        qi = self._getTargetClass().by_id(100)
        self.assertEqual(qi.title, 'Test')
        self.assertEqual(qi.amount, 1234)


class ExpenditureModelTests(BaseTestCase):

    def _getTargetClass(self):
        from pyrtos.models import Expenditure
        return Expenditure

    def _makeOne(self, id, title, amount):
        return self._getTargetClass()(id=id,\
                                      title=title,\
                                      amount=amount,\
                                      category_id=1,\
                                      user_id=1)

    def test_constructor(self):
        instance = self._makeOne(100, 'Test', 1234)
        self.session.add(instance)

        qi = self._getTargetClass().by_id(100)
        self.assertEqual(qi.title, 'Test')
        self.assertEqual(qi.amount, 1234)


class InvoiceModelTests(BaseTestCase):
    
    def _getTargetClass(self):
        from pyrtos.models import Invoice
        return Invoice

    def _makeOne(self, id, title, amount):
        return self._getTargetClass()(id=id,\
                                      title=title,\
                                      amount=amount,\
                                      due=datetime.utcnow(),\
                                      category_id=1,\
                                      creditor_id=1,\
                                      user_id=1)

    def test_constructor(self):
        instance = self._makeOne(1, 'Test', 1234)
        self.session.add(instance)

        qi = self._getTargetClass().by_id(1)
        self.assertEqual(qi.title, 'Test')
        self.assertEqual(qi.amount, 1234)
        
        css_time = instance.css_class_for_time_distance()
        self.assertEqual(css_time, 'expired')

        time_to = instance.time_to_expires_in_words()
        self.assertIn('less', time_to)

        instance.due = datetime.utcnow()+timedelta(days=10)
        css_time = instance.css_class_for_time_distance()
        self.assertEqual(css_time, 'd10')
        
        time_to = instance.time_to_expires_in_words()
        self.assertIn('10 days', time_to)


class FileModelTests(BaseTestCase):
    
    def _getTargetClass(self):
        from pyrtos.models import File
        return File

    def _makeOne(self, id, title, filename):
        return self._getTargetClass()(id=id,
                                      title=title,
                                      filename=filename,
                                      user_id=1,)

    def test_constructur(self):
        instance = self._makeOne(1, 'test', 'test.jpg')
        self.session.add(instance)

        qi = self._getTargetClass().by_id(1)
        self.assertEqual(qi.title, 'test')
        self.assertEqual(qi.filename, 'test.jpg')
