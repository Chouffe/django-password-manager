import random


# Create your models here.
class Generator():

    last_password_generated = None

    def __init__(self, upper_letters=True, lower_letters=True,
                 numbers=True, special_characters=True, length=10):
        self.upper_letters = upper_letters
        self.lower_letters = lower_letters
        self.numbers = numbers
        self.special_characters = special_characters
        self.length = length

    def generate(self):

        allowed_char = []
        password = []

        if self.lower_letters:
            allowed_char += map(chr, range(97, 123))
        if self.upper_letters:
            allowed_char += map(chr, range(65, 91))
        if self.numbers:
            allowed_char += [str(i) for i in xrange(0, 10)]
        if self.special_characters:
            allowed_char += map(chr, range(33, 47))
        random.shuffle(allowed_char)

        n = len(allowed_char)
        if n == 0:
            raise GeneratorException
        else:
            for _ in xrange(self.length):
                index = random.randint(0, n-1)
                password.append(allowed_char[index])

            self.last_password_generated = ''.join(password)
            return self.last_password_generated


class GeneratorException(Exception):

    def __init__(self):
        self.error = 'Can not generate a Key'

    def __str__(self):
        return self.error
