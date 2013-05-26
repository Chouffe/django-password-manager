from django.db import models
import hashlib
from Crypto.Cipher import DES
from Crypto import Random
import base64


class Entry(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=False, blank=False)
    comment = models.TextField(null=True, blank=True)
    expires = models.DateField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)


class CryptoEngine:

    padding = 0

    def __init__(self, master_key):
        self.master_key = master_key
        self.block_length = 8
        self.key = self._generate_key(master_key, 8)
        self.mode = DES.MODE_ECB
        self.iv = Random.new().read(8)
        self.encryptor = DES.new(self.key, self.mode)
        # TODO: uses AES instead of DES
        # self.encryptor = DES.new(self.key, self.mode, self.iv)
        # self.encryptor = AES.new(self.key, self.mode, self.iv)

    def _generate_key(self, master_key, length):
        m = hashlib.md5()
        m.update(master_key)
        return m.hexdigest()[:length]

    def encrypt(self, text):
        return base64.b64encode(self.encryptor.encrypt(self._pad_text(text)))

    def decrypt(self, text):
        return self._unpad_text(self.encryptor.decrypt(base64.b64decode(text)))

    def _pad_text(self, text):
        padding = len(text) % self.block_length
        if padding == 0:
            self.padding = 0
            return text
        else:
            self.padding = self.block_length - padding
            return text + ' '.join(['' for i in xrange(self.padding + 1)])

    def _unpad_text(self, text):
        return text.rstrip()
