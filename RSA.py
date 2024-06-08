from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP


# Generate RSA key pair
def get_keys(size):
    if size < 1024:
        size = 1024
    private_key = RSA.generate(size)
    public_key = private_key.publickey()
    return public_key, private_key


# Encrypt data using RSA public key
def encrypt(public_key, msg):
    msg = msg.encode()
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted = encryptor.encrypt(msg)
    return encrypted


# Decrypt data using RSA private key
def decrypt(private_key, encrypted):
    decryptor = PKCS1_OAEP.new(private_key)
    decrypted = decryptor.decrypt(encrypted)
    return decrypted

