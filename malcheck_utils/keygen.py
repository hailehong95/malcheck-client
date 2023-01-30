from malcheck_utils.config import KEYS_DIR, RSA_KEY_DIR
from malcheck_utils.config import RSA_PRI_KEY, RSA_PUB_KEY

import os
import time
import shutil

from Cryptodome.PublicKey import RSA


# Ref: https://pycryptodome.readthedocs.io/en/latest/src/examples.html
def rsa_keys_gen(key_length):
    try:
        new_key = RSA.generate(int(key_length))
        private_key = new_key.exportKey()
        public_key = new_key.publickey().exportKey()
        with open(os.path.join(RSA_KEY_DIR, RSA_PRI_KEY), 'wb') as f:
            f.write(private_key)
        with open(os.path.join(RSA_KEY_DIR, RSA_PUB_KEY), 'wb') as f:
            f.write(public_key)
    except Exception as ex:
        print(ex)


# Keygen Task: Generate RSA keypair, save to rsa_keys dir
def malcheck_keygen():
    try:
        if not os.path.isdir(RSA_KEY_DIR):
            os.mkdir(RSA_KEY_DIR)
        print("[KEYGEN] Generating RSA keypair")
        rsa_keys_gen(2048)
        rsa_keys = os.listdir(RSA_KEY_DIR)
        print(f"[KEYGEN] Done! Total {len(rsa_keys)} keys: {rsa_keys}\n")
        time.sleep(0.5)
    except Exception as ex:
        print(ex)


# RSA Key Task: Adding RSA encryption key to bundle
def malcheck_copy_key():
    try:
        if not os.path.isdir(RSA_KEY_DIR):
            os.mkdir(RSA_KEY_DIR)
        rsa_keys = os.listdir(RSA_KEY_DIR)
        if RSA_PRI_KEY not in rsa_keys or RSA_PUB_KEY not in rsa_keys:
            malcheck_keygen()
        print("[KEYADD] Copy public key")
        if not os.path.isdir(KEYS_DIR):
            os.mkdir(KEYS_DIR)
        src_file = os.path.join(RSA_KEY_DIR, RSA_PUB_KEY)
        dst_file = os.path.join(KEYS_DIR, RSA_PUB_KEY)
        shutil.copyfile(src_file, dst_file)
        time.sleep(0.5)
        if os.path.exists(dst_file):
            print("[KEYADD] Done!\n")
        else:
            print("[KEYADD] Failed!\n")
    except Exception as ex:
        print(ex)
