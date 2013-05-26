from django.test import TestCase
from models import Entry, CryptoEngine, Category
from datetime import datetime
import random
import base64


class ModelTest(TestCase):

    now = datetime.now().date()
    entry = None

    def setUp(self):
        e = Entry(title='Twitter', username='userName', url='twitter.com',
                  password='passssss', comment='no comment')
        c = Category(title='Internet', parent=None)
        e.category = c

        self.entry = e
        self.category = c

        c.save()
        e.save()

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


class CryptoEngineTest(TestCase):

    def setUp(self):

        self.engine = CryptoEngine(master_key='mykeyisawesome!')
        self.block_length = 8
        self.texts = generate_texts(100)

    def test_padding(self):
        for t in self.texts:
            padded_text = self.engine._pad_text(t)
            self.assertEquals(len(padded_text) % self.block_length, 0)

    def test_unpadding(self):
        for p, t in zip([t + '    ' for t in self.texts], self.texts):
            self.assertEquals(t, self.engine._unpad_text(p))

    def test_encryption(self):
        self.assertEquals(len(self.engine.key), self.block_length)

    def test_decryption(self):
        for t in self.texts:
            cipher_text = self.engine.encrypt(t)
            self.assertEquals(self.engine.decrypt(cipher_text), t)


class EncryptedPasswordsEntry(TestCase):

    def setUp(self):
        self.engine = CryptoEngine(master_key='mykeyisawesome!')
        self.texts = generate_texts(100)

    def test_save_entry_with_encrypted_key(self):

        for i, password in enumerate(self.texts):

            password_after_encryption = self.engine.encrypt(password)
            title = 'My Twitter Account: ' + str(i)
            e = Entry(title=title, username='userName',
                      url='twitter.com', password=password_after_encryption,
                      comment='no comment')
            e.save()

            # Fetched the saved entry
            f = Entry.objects.filter(title=title)[0]
            password_decrypted = self.engine.decrypt(f.password)
            # print password
            # print password_decrypted

            # self.assertEquals(password_after_encryption, f.password)
            self.assertEquals(password_after_encryption, f.password)
            self.assertEquals(password_decrypted, password)
            f.delete()


def generate_texts(limit):

        allowed_char = map(chr, range(97, 123))
        allowed_char += map(chr, range(65, 91))
        allowed_char += [str(i) for i in xrange(0, 10)]
        allowed_char += map(chr, range(33, 47))

        min_length = 1
        max_length = len(allowed_char) - 1

        texts = []

        for i in xrange(limit):
            length = random.randint(min_length, max_length)
            random.shuffle(allowed_char)
            texts += [''.join(allowed_char[:length])]

        return texts
