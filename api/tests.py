from django.test import TestCase
from django.test.client import Client
import json
import random
from manager.models import Entry, Category

# TODO: add fixture to test login_require
class APITest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category(title='cat')
        self.category.save()

    def test_get_entry_title(self):
        response = self.client.get('/api/entries.json')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertTrue(isinstance(data, list))
        self.assertEquals(len(data), 0)
        number_of_entries = 100
        entries = self._generate_entries(number_of_entries, self.category)

        for e in entries:
            e.save()

        response = self.client.get('/api/entries.json')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertTrue(isinstance(data, list))
        self.assertEquals(len(data), number_of_entries)

    def _generate_entries(self, number, category):
        entries = []
        for i in xrange(number):
            entries.append(Entry(title=str(i), password=str(i), category=category))
        return entries

    def test_get_random_key(self):

        queries = self._generate_queries(100)
        for q in queries:
            response = self.client.get('/api/random_key.json', q)
            self.assertEquals(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEquals(len(data), q['length'])

    def _generate_queries(self, number):
        queries = []
        for i in xrange(number):
            queries.append({'length': random.randint(1,100)})
        return queries
