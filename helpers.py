import random
import hashlib
import os


class Auth:
    @staticmethod
    def get_new_key():
        CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        key = ''
        for x in range(15):
            key += random.choice(CHARS)
        return key


class Crypt:
    @staticmethod
    def hash_sha256(text):
        SALT = os.environ.get('SALT', 'development_salt')
        return hashlib.sha256((SALT + text).encode()).hexdigest()


if __name__ == '__main__':
    print(Auth.get_new_key())
    print(Crypt.hash_sha256('senha'))
