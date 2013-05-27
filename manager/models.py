from Crypto.Cipher import AES
from Crypto.Hash import MD5
from base64 import encodestring, decodestring
from django.db import models
from Crypto import Random


class Entry(models.Model):

    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=False, blank=False)
    comment = models.TextField(null=True, blank=True)
    expires = models.DateField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey('Category')

    def __unicode__(self):
        return self.title


class Category(models.Model):

    title = models.CharField(max_length=200)
    parent = models.ForeignKey('Category', null=True, blank=True)

    def __unicode__(self):
        return self.title


class CryptoEngine:

    PADDING = '{'
    BLOCK_SIZE = 32
    # TODO: use the random bit string as salt
    IV = Random.new().read(AES.block_size)

    def __init__(self, master_key):

        self.master_key = master_key
        self.secret = self._get_secret(master_key)
        self.cipher = AES.new(self.secret)
        self.decipher = AES.new(self.secret)
        # self.cipher = AES.new(self.secret, AES.MODE_CBC, IV)
        # self.decipher = AES.new(self.secret, AES.MODE_CBC, IV)

    def _pad(self, msg, block_size=BLOCK_SIZE, padding=PADDING):
        return msg + ((block_size - len(msg) % block_size) * padding)

    def _depad(self, msg, padding=PADDING):
        return msg.rstrip(padding)

    def _get_secret(self, key):
        return MD5.new(key).hexdigest()[:self.BLOCK_SIZE]

    def encrypt(self, msg):
        return encodestring(self.cipher.encrypt(self._pad(msg)))

    def decrypt(self, msg):
        return self._depad((self.decipher.decrypt(decodestring(msg))))
