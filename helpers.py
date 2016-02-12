import random
import hashlib
import os


class Auth:
    MESSAGE_OK = 'Authentication key is valid';
    MESSAGE_ERROR = 'Authentication key is invalid';

    @staticmethod
    def get_new_key():
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_'
        key = ''
        for x in range(10):
            key += random.choice(chars)
        return key


class Crypt:
    @staticmethod
    def salt():
        return os.environ.get('MINHAEIRO_SALT') or 'development_salt'

    @staticmethod
    def hash_sha256(text):
        return hashlib.sha256((Crypt.salt() + text).encode()).hexdigest()


if __name__ == '__main__':
    print(Auth.get_new_key())
    print(Crypt.hash_sha256('senha'))