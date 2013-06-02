from django.test import TestCase
from manager.models import Entry, CryptoEngine, Category
from datetime import datetime
import random


class ModelTest(TestCase):

    now = datetime.now().date()

    def setUp(self):
        e = Entry(title='Twitter', username='userName', url='twitter.com',
                  password='passssss', comment='no comment')
        c = Category(title='Internet', parent=None)

        self.entry = e
        self.category = c

        c.save()
        e.category = c
        e.save()

    def test_create_entry(self):

        e = Entry.objects.filter(title=self.entry.title)
        e = e[0]
        self.assertEquals(e.expires, None)
        self.assertEquals(e.date, self.now)

        # Entry without category
        e2 = Entry(title='Test', password='password')
        try:
            e2.save()
        except:
            pass
        else:
            self.fail('Should not save an entry without category...')

    def test_change_entry(self):

        new_title = 'Facebook powaa'
        self.entry.title = new_title
        self.entry.save()
        e = Entry.objects.filter(title=new_title)
        e = e[0]
        self.assertEquals(e.title, new_title)

    def test_delete_entry(self):

        id = self.entry.id
        self.entry.delete()
        self.assertEquals(len(Entry.objects.filter(id=id)), 0)

    def test_create_category(self):
        t = 'uniqTitle'
        c1 = Category(title=t)
        c2 = Category(title=t)
        c1.save()
        try:
            c2.save()
        except:
            pass
        else:
            self.fail('Should not have two categories with same title')


    def test_delete_category(self):

        category = Category(title='Cat')
        category.save()
        entries = self._generate_entries(50)
        self._assign_category(entries, category)
        for e in entries:
            e.save()
            f = Entry.objects.filter(category=category)[0]
            self.assertEquals(f.category_id, category.id)
        id = category.id
        category.delete()
        self.assertEquals(len(Entry.objects.filter(category_id=id)), 0)

    def _generate_entries(self, number):

        entries = []
        for i in xrange(number):
            entries.append(Entry(title=str(i), password=str(i)))
        return entries

    def _assign_category(self, entries, category):

        for e in entries:
            e.category = category
