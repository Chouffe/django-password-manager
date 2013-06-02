from django.test import TestCase
from manager.models import Entry, CryptoEngine, Category
import random


class CryptoEngineTest(TestCase):

    def setUp(self):

        self.engine = CryptoEngine(master_key='mykeyisawesome!')
        self.block_length = 32
        self.texts = CryptoEngineTest._generate_texts(100)

    def test_padding(self):
        for t in self.texts:
            padded_text = self.engine._pad(t)
            self.assertEquals(len(padded_text) % self.block_length, 0)

    def test_depadding(self):
        for p, t in zip([t + ''.join([self.engine.PADDING
                                      for i in xrange(random.randint(1, 10))])
                         for t in self.texts], self.texts):
            self.assertEquals(t, self.engine._depad(p))

    def test_decryption(self):
        for t in self.texts:
            cipher_text = self.engine.encrypt(t)
            self.assertEquals(self.engine.decrypt(cipher_text), t)

    @classmethod
    def _generate_texts(cls, limit):

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


class EncryptedPasswordsEntry(TestCase):

    def setUp(self):
        self.engine = CryptoEngine(master_key='mykeyisawesome!')
        self.texts = CryptoEngineTest._generate_texts(100)

    def test_save_entry_with_encrypted_key(self):

        c = Category(title='Internet')
        c.save()

        for i, password in enumerate(self.texts):

            password_after_encryption = self.engine.encrypt(password)
            title = 'My Twitter Account: ' + str(i)
            e = Entry(title=title, username='userName',
                      url='twitter.com', password=password_after_encryption,
                      comment='no comment')
            e.category = c
            e.save()

            # Fetches the saved entry
            f = Entry.objects.filter(title=title)[0]
            password_decrypted = self.engine.decrypt(f.password)

            self.assertEquals(password_after_encryption, f.password)
            self.assertEquals(password_decrypted, password)
            f.delete()
