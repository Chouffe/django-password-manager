from django.test import TestCase
from django.test.client import Client
import json
import random
from manager.models import Entry, Category


class APITest(TestCase):

    USERNAME = 'admin'
    PASSWORD = 'admin'
    fixtures = ['admin_user.json', 'initial_data.json']
    API_pages = [{'page': '/api/entries.json', 'parameters': {}},
                 {'page': '/api/random_key.json', 'parameters':
                  {'length': 100}},
                 {'page': '/api/search.json', 'parameters': {'title': ''}}
                 ]

    def setUp(self):
        self.client = Client()
        self.category = Category(title='cat')
        self.category.save()
        self.entries = Entry.objects.all()
        self.categories = Category.objects.all()

    def test_authentification(self):
        # Without auth
        for p in self.API_pages:
            response = self.client.get(p['page'], p['parameters'])
            self.assertFalse(response.status_code == 200)

        # With auth
        self._authentificate()
        for p in self.API_pages:
            response = self.client.get(p['page'], p['parameters'])
            self.assertTrue(response.status_code == 200)

    def test_get_entry_title(self):
        self._authentificate()
        response = self.client.get('/api/entries.json')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertTrue(isinstance(data, list))
        self.assertEquals(len(data), len(self.entries))
        number_of_entries = 100
        entries = self._generate_entries(number_of_entries, self.category)

        for e in entries:
            e.save()

        response = self.client.get('/api/entries.json')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertTrue(isinstance(data, list))
        self.assertEquals(len(data), number_of_entries + len(self.entries))

    def test_get_random_key(self):

        self._authentificate()
        queries = self._generate_queries(100)
        for q in queries:
            response = self.client.get('/api/random_key.json', q)
            self.assertEquals(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEquals(len(data), q['length'])

    def test_get_entry_search(self):

        # test the search on the titles
        self._authentificate()
        for e in self.entries:
            s = {'title': e.title}
            response = self.client.get('/api/search.json', s)
            self.assertEquals(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEquals(len(data), 1)

        # Test the search on the categories
        for c in self.categories:
            s = {'category': c.title}
            response = self.client.get('/api/search.json', s)
            self.assertEquals(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEquals(len(data), len(c.entry_set.all()))


    def _generate_entries(self, number, category):
        entries = []
        for i in xrange(number):
            entries.append(Entry(title=str(i),
                                 password=str(i),
                                 category=category))
        return entries

    def _generate_queries(self, number):
        queries = []
        for i in xrange(number):
            queries.append({'length': random.randint(1, 100)})
        return queries

    def _authentificate(self):
        self.client.login(username=self.USERNAME, password=self.PASSWORD)
