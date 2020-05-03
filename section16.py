# 暗号化
# 文字コードの説明を最初にしてた（ASCIIコード、Shift-JIS、Unicode、UTF-8など）

# pycryptoの暗号化と復号化
# $ pip install pycrypto
import string
import random

from Crypto.Cipher import AES

print(string.ascii_letters)
print(AES.block_size)
key = ''.join(
    random.choice(string.ascii_letters) for _ in range(AES.block_size)
)
print(key)

iv = ''.join(
    random.choice(string.ascii_letters) for _ in range(AES.block_size)
)
print(iv)

plaintext = 'rogerfederer'
cipher = AES.new(key, AES.MODE_CBC, iv)

padding_length = AES.block_size - len(plaintext) % AES.block_size
plaintext += chr(padding_length) * padding_length
cipher_text = cipher.encrypt(plaintext)
print(cipher_text)

cipher2 = AES.new(key, AES.MODE_CBC, iv)
decrypted_text = cipher2.decrypt(cipher_text)
print(decrypted_text)
print(decrypted_text[-1])
print(decrypted_text[:-decrypted_text[-1]])

with open('test.txt', 'r') as f, open('dist/enc.dat', 'wb') as e:
    plaintext = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padding_length = AES.block_size - len(plaintext) % AES.block_size
    plaintext += chr(padding_length) * padding_length
    cipher_text = cipher.encrypt(plaintext)
    e.write(cipher_text)

with open('dist/enc.dat', 'r') as f:
    cipher2 = AES.new(key, AES.MODE_CBC, iv)
    decrypted_text = cipher2.decrypt(cipher_text)
    print(decrypted_text[:-decrypted_text[-1]].decode('utf-8'))

# hashlibのハッシュ
import base64
import os
import hashlib


# print(hashlib.sha256(b'passw').hexdigest())

user_name = 'user1'
user_pass = 'pass'
db = {}

# ハッシュのときの強化1: saltを加える
salt = base64.b64encode(os.urandom(32))


def get_digest(user_pass):
    passw = bytes(user_pass, 'utf-8')
    digest = hashlib.sha256(salt + passw).hexdigest()
    # ハッシュの時の強化2: stretch
    for _ in range(10000):
        digest = hashlib.sha256(bytes(digest, 'utf-8')).hexdigest()
    return digest


# 上記メソッドを下記でやってくれる！
hashlib.pbkdf2_hmac(
    'sha256', bytes(user_pass, 'utf-8'), salt, 10000
)

db[user_name] = get_digest(user_pass)
print(db)


def is_login(user_name, user_pass):
    return get_digest(user_pass) == db[user_name]


print(is_login(user_name, user_pass))
