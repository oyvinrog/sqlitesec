import sqlite3
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode

class SqliteSec:
    def __init__(self, key):
        self.key = key
        self.backend = default_backend()

    def _get_cipher(self, salt, iv):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        derived_key = kdf.derive(self.key)
        return Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=self.backend)

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        salt = os.urandom(16)
        iv = os.urandom(16)
        cipher = self._get_cipher(salt, iv)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        with open(file_path, 'wb') as f:
            f.write(salt + iv + encrypted_data)

    def decrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        salt = data[:16]
        iv = data[16:32]
        encrypted_data = data[32:]
        cipher = self._get_cipher(salt, iv)
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        with open(file_path, 'wb') as f:
            f.write(decrypted_data)

    def connect(self, db_path):
        if os.path.exists(db_path):
            print(f"Decrypting {db_path}...")
            self.decrypt_file(db_path)
        return sqlite3.connect(db_path)

    def close(self, conn, db_path):
        conn.close()
        print(f"Encrypting {db_path}...")
        self.encrypt_file(db_path)

