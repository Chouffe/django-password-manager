from django.test import TestCase
from models import Generator, GeneratorException


class ModelTest(TestCase):

    def setUp(self):
        self.generator = Generator(upper_letters=True,
                                   lower_letters=True,
                                   numbers=True,
                                   special_characters=True,
                                   length=25)

    def test_key_generation(self):

        password = self.generator.generate()
        self.assertEquals(len(password), 25)
        self.assertEquals(self.generator.last_password_generated, password)

        self.generator.length = 0
        self.assertEquals(self.generator.generate(), '')

        self.generator.upper_letters = False
        self.generator.lower_letters = False
        self.generator.numbers = False
        self.generator.special_characters = False

        try:
            password = self.generator.generate()
        except GeneratorException, e:
            pass
        else:
            self.fail('Exception not thrown')
