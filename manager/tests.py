from django.test import TestCase
from models import Entry
from datetime import datetime


class ModelTest(TestCase):

    def test_create_key(self):

        now = datetime.now().date()
        e = Entry(title='Twitter', username='userName', url='twitter.com',
                  password='passssss', comment='no comment')
        e.save()

        self.assertEquals(e.expires, None)
        self.assertEquals(e.date, now)

        self.fail('TODO: finish test')
