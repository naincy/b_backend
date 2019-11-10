from Crypto import Random
from Crypto.Cipher import AES
from django.conf import settings

"""
Encryptor Util Class
"""
class Encryptor:

    def pad(s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
    
    @staticmethod
    def encrypt(message):
        key = settings.ENCRYPT_KEY
        message = message.encode('ascii')
        message = Encryptor.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    @staticmethod
    def decrypt(ciphertext):
        key = settings.ENCRYPT_KEY
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0").decode("utf-8")

