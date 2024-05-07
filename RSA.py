from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP


def get_keys(size):
    if size < 1024:
        size = 1024
    private_key = RSA.generate(size)
    public_key = private_key.publickey()
    return public_key, private_key


def encrypt(public_key, msg):
    msg = msg.encode()
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted = encryptor.encrypt(msg)
    return encrypted


def decrypt(private_key, encrypted):
    decryptor = PKCS1_OAEP.new(private_key)
    decrypted = decryptor.decrypt(encrypted)
    return decrypted


if __name__ == '__main__':
    public_Key, privet_Key = get_keys()
    """enc_aeskey = encrypt(pubKey, 'Hello World!')
    print('Encrypted:', enc_aeskey)
    dec_aeskey = decrypt(priKey, enc_aeskey)
    print('Decrypted:', dec_aeskey)"""
