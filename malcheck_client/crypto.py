import os
import zlib
import string
import random
import base64

from io import BytesIO
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Random import get_random_bytes

KEY_PREFIX = "malcheck"


def string_random(n):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(n))


def generate(key_dir):
    new_key = RSA.generate(2048)
    private_key = new_key.exportKey()
    public_key = new_key.publickey().exportKey()
    with open(os.path.join(key_dir, 'key.pri'), 'wb') as f:
        f.write(private_key)
    with open(os.path.join(key_dir, 'key.pub'), 'wb') as f:
        f.write(public_key)


def get_rsa_cipher(key_dir, key_type):
    with open(os.path.join(key_dir, f'{KEY_PREFIX}.{key_type}')) as f:
        key = f.read()
    rsa_key = RSA.importKey(key)
    return PKCS1_OAEP.new(rsa_key), rsa_key.size_in_bytes()


def encrypt(key_dir, plaintext):
    compressed_text = zlib.compress(plaintext)
    session_key = get_random_bytes(16)
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(compressed_text)
    cipher_rsa, _ = get_rsa_cipher(key_dir, 'pub')
    encrypted_session_key = cipher_rsa.encrypt(session_key)
    msg_payload = encrypted_session_key + cipher_aes.nonce + tag + ciphertext
    encrypted = base64.encodebytes(msg_payload)
    return encrypted


def decrypt(key_dir, encrypted):
    encrypted_bytes = BytesIO(base64.decodebytes(encrypted))
    cipher_rsa, key_size_in_bytes = get_rsa_cipher(key_dir, 'pri')
    encrypted_session_key = encrypted_bytes.read(key_size_in_bytes)
    nonce = encrypted_bytes.read(16)
    tag = encrypted_bytes.read(16)
    ciphertext = encrypted_bytes.read()
    session_key = cipher_rsa.decrypt(encrypted_session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    decrypted = cipher_aes.decrypt_and_verify(ciphertext, tag)
    plaintext = zlib.decompress(decrypted)
    return plaintext

# >>> from malcheck_client.crypto import encrypt, decrypt
# >>> from malcheck_utils.config import RSA_KEY_DIR
# >>> plaintext = b"This is secret message!"
# >>> encrypted = encrypt(RSA_KEY_DIR, plaintext)
# >>> print(encrypted)
# >>> print(decrypt(RSA_KEY_DIR, encrypted))
