from django.test import TestCase
from models import Entry, CryptoEngine
from datetime import datetime
import random


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


class CryptoEngineTest(TestCase):

    def setUp(self):

        self.engine = CryptoEngine(master_key='mykeyisawesome!')
        self.text = 'abcdefgh'
        self.block_length = 8
        self.texts = [self.text]

        allowed_char = map(chr, range(97, 123))
        allowed_char += map(chr, range(65, 91))
        allowed_char += [str(i) for i in xrange(0, 10)]
        allowed_char += map(chr, range(33, 47))

        # Creates a lot of texts to be tested on
        for i in xrange(100):
            index = random.randint(0, len(allowed_char) - 1)
            letter = allowed_char[index]
            for j in xrange(random.randint(1, 10)):
                self.texts += [self.texts[-1] +
                               ''.join([letter for k in xrange(j)])]

    def test_padding(self):
        for t in self.texts:
            padded_text = self.engine._pad_text(t)
            self.assertEquals(len(padded_text) % self.block_length, 0)

    def test_unpadding(self):
        self.assertEquals('abcd', self.engine._unpad_text('abcd     '))

    def test_encryption(self):
        self.assertEquals(len(self.engine.key), self.block_length)

    def test_decryption(self):
        for t in self.texts:
            cipher_text = self.engine.encrypt(t)
            self.assertEquals(self.engine.decrypt(cipher_text), t)
