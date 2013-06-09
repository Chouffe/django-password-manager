from django.test import TestCase
from django.test.client import Client
import json
import random
from manager.models import Entry, Category
import datetime


class APITest(TestCase):

    USERNAME = 'admin'
    PASSWORD = 'admin'
    fixtures = ['admin_user.json', 'data.json']
    API_pages = [{'page': '/api/entries.json', 'method': 'get',
                  'parameters': {}},
                 {'page': '/api/random_key.json', 'method': 'get',
                  'parameters': {'length': 100}},
                 {'page': '/api/search.json', 'method': 'get',
                  'parameters': {'title': ''}},
                 {'page': '/api/entry/add', 'method': 'post',
                  'parameters': {'title': 'new entry', 'password': 'pass'}}
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

            if p['method'] == 'get':
                response = self.client.get(p['page'], p['parameters'])
            elif p['method'] == 'post':
                response = self.client.post(p['page'], p['parameters'])

            self.assertFalse(response.status_code == 200)

        # With auth
        self._authentificate()
        for p in self.API_pages:
            if p['method'] == 'get':
                response = self.client.get(p['page'], p['parameters'])
            elif p['method'] == 'post':
                response = self.client.post(p['page'], p['parameters'])

            self.assertTrue(response.status_code == 200)

    def test_get_entry_title(self):
        self._authentificate()
        response = self.client.get('/api/entries.json')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertTrue(isinstance(data, list))
        self.assertEquals(len(data), len(self.entries))
        number_of_entries = 20
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
        queries = self._generate_queries(20)
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

    def test_entry_add(self):

        self._authentificate()
        cat = Category(title='New cat')
        cat.save()
        entries = self._generate_entries(20, cat)

        # Test good insertions
        for e in entries:

            s = {'title': e.title, 'password': e.password, 'category': e.category.id}
            response = self.client.post('/api/entry/add', s)
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.content, '1')

            entry_from_db = Entry.objects.filter(title=e.title)
            e2 = entry_from_db[0]
            self.assertTrue(len(entry_from_db) >= 1)
            self.assertEquals(e2.title, s['title'])
            self.assertEquals(e2.password, s['password'])
            self.assertEquals(e2.category.id, s['category'])


        # Test bad insertions
        s = [{'title': 'test', 'category': self.category.id},
             {'password': 'pass', 'category': self.category.id},
             {'password': 'pass', 'title': 'test'},
             {'password': 'pass'},
             {'title': 't'},
             {'category': self.category.id},
             {'password': 'pass', 'title': 'test', 'category': self.category.id + 1000},
             ]

        for bad in s:
            response = self.client.post('/api/entry/add', bad)
            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.content, '0')

        # Test dates
        title = str(random.random())
        date = '06/14/2025'
        s = {'title': title,
             'password': 'pass',
             'category': e.category.id,
             'expires': date}
        response = self.client.post('/api/entry/add', s)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '1')
        entry_from_db = Entry.objects.filter(title=title)[0]
        self.assertEquals(entry_from_db.expires, datetime.datetime.strptime(date, "%m/%d/%Y").date())

    def _generate_entries(self, number, category):
        entries = []
        for i in xrange(number):
            entries.append(Entry(title=str(random.random()),
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
