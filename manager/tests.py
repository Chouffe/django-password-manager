from django.test import TestCase
from models import Entry
from datetime import datetime


class ModelTest(TestCase):

    now = datetime.now().date()
    entry = None

    def setUp(self):
        e = Entry(title='Twitter', username='userName', url='twitter.com',
                  password='passssss', comment='no comment')
        e.save()
        self.entry = e

    def test_create_entry(self):

        e = Entry.objects.filter(id=1)
        e = e[0]
        self.assertEquals(e.expires, None)
        self.assertEquals(e.date, self.now)

    def test_change_entry(self):

        new_title = 'Facebook'
        self.entry.title = new_title
        self.entry.save()
        e = Entry.objects.filter(id=1)
        e = e[0]
        self.assertEquals(e.title, new_title)

    def test_delete_entry(self):

        self.entry.delete()
        self.assertEquals(len(Entry.objects.all()), 0)
