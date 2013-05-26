from Crypto.Cipher import AES
from Crypto.Hash import MD5
from base64 import encodestring, decodestring
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
    category = models.ForeignKey('Category', null=True, blank=True)

    def __unicode__(self):
        return self.title


class Category(models.Model):

    title = models.CharField(max_length=200)
    parent = models.ForeignKey('Category', null=True, blank=True)

    def __unicode__(self):
        return self.title


# class CryptoEngine:
#
#     padding = 0
#
#     def __init__(self, master_key):
#         self.master_key = master_key
#         self._block_length = 8
#         self.key = self._generate_key(master_key, 8)
#         self.mode = DES.MODE_ECB
#         self.iv = Random.new().read(8)
#         self.encryptor = DES.new(self.key, self.mode)
#         # TODO: uses AES instead of DES
#         # self.encryptor = DES.new(self.key, self.mode, self.iv)
#         # self.encryptor = AES.new(self.key, self.mode, self.iv)
#
#     def _generate_key(self, master_key, length):
#         m = hashlib.md5()
#         m.update(master_key)
#         return m.hexdigest()[:length]
#
#     def encrypt(self, text):
#         return base64.b64encode(self.encryptor.encrypt(self._pad_text(text)))
#
#     def decrypt(self, text):
#         return self._unpad_text(self.encryptor.decrypt(base64.b64decode(text)))
#
#     def _pad_text(self, text):
#         padding = len(text) % self._block_length
#         if padding == 0:
#             self.padding = 0
#             return text
#         else:
#             self.padding = self._block_length - padding
#             return text + ' '.join(['' for i in xrange(self.padding + 1)])
#
#     def _unpad_text(self, text):
#         return text.rstrip()

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
        """
        *pad the text to be encrypted*
        - appends a padding character to the end of the String
        - until the string has block_size length

        """
        return msg + ((block_size - len(msg) % block_size) * padding)

    def _depad(self, msg, padding=PADDING):
        """depad the decrypted message"""
        return msg.rstrip(padding)

    def _get_secret(self, key):
        """hases the key to MD5"""
        return MD5.new(key).hexdigest()

    def encrypt(self, msg):
        """encrypts the message"""
        return encodestring(self.cipher.encrypt(self._pad(msg)))

    def decrypt(self, msg):
        """decrypts the message"""
        return self._depad((self.decipher.decrypt(decodestring(msg))))
