import unittest
import os
import sys
from pathlib import Path

# Useful constants for the test
KEYLIME_DIR = Path(__file__).parents[1]

# Custom imports
sys.path.insert(0, KEYLIME_DIR)
from keylime.crypto import *


class Crypto_Test(unittest.TestCase):

    def test_rsa(self):
        message = b"a secret message!"
        private = rsa_generate(2048)
        pubkeypem = rsa_export_pubkey(private)
        pubkey = rsa_import_pubkey(pubkeypem)
        keypem = rsa_export_privkey(private)
        key = rsa_import_privkey(keypem)
        ciphertext = rsa_encrypt(pubkey, message)
        plain = rsa_decrypt(key, ciphertext)
        self.assertEqual(plain, message)

    def test_aes(self):
        message = b"a secret message!"
        aeskey = get_random_bytes(32)
        ciphertext = encrypt(message,aeskey)
        plaintext = decrypt(ciphertext,aeskey)
        self.assertEqual(plaintext, message)

    def test_hmac(self):
        message = "a secret message!"
        aeskey=kdf(message,'salty-McSaltface')
        digest = do_hmac(aeskey,message)
        aeskey2 = kdf(message,'salty-McSaltface')
        self.assertEqual(do_hmac(aeskey2,message), digest)

    def test_xor(self):
        k = get_random_bytes(32)
        s1 = generate_random_key(32)
        s2 = strbitxor(s1, k)
        self.assertEqual(strbitxor(s1,s2), k)

    def test_errors(self):
        encrypt(None,get_random_bytes(32))

        with self.assertRaises(Exception):
            decrypt("",None)

        invalid = base64.b64encode(get_random_bytes(45))
        with self.assertRaises(Exception):
            decrypt(invalid,None)

    def test_rsa_sign(self):
        message = b"a secret message!"
        private = rsa_generate(2048)
        public_key = get_public_key(private)
        signature = rsa_sign(private, message)
        self.assertTrue(rsa_verify(public_key, message,signature))

        message = b"another message!"
        self.assertFalse(rsa_verify(public_key, message,signature))


if __name__ == '__main__':
    unittest.main()
