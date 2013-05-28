from django.test import TestCase
from django.test.client import Client
import json
from manager.models import Entry, Category


class APITest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category(title='cat')
        self.category.save()

    def test_get_entry_title(self):
        response = self.client.get('/api/entries.json')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        print data
        self.assertTrue(isinstance(data, list))
        self.assertEquals(len(data), 0)
        number_of_entries = 100
        entries = self._generate_entries(number_of_entries, self.category)

        for e in entries:
            e.save()

        response = self.client.get('/api/entries.json')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        print data
        self.assertTrue(isinstance(data, list))
        self.assertEquals(len(data), number_of_entries)

    def _generate_entries(self, number, category):
        entries = []
        for i in xrange(number):
            entries.append(Entry(title=str(i), password=str(i), category=category))
        return entries
