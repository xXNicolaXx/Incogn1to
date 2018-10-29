from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import pyaes
import base64
import random
import string


def gen_key():

    global aes_key

    # 256 bit key AES generation
    gen = string.ascii_letters + string.digits + string.punctuation
    aes_key = ''.join(random.sample(gen, 32))
    # Convert key in bytes
    aes_key = aes_key.encode('utf-8')


def aes_encryption_sender(plaintext):

    aes = pyaes.AESModeOfOperationCTR(aes_key)
    # Encrypt the plaintext with the AES key
    cipher_text = aes.encrypt(plaintext)
    base64text = base64.b64encode(cipher_text)

    return base64text


def rsa_encryption(public_key_list):

    # Encrypt the AES key with the public RSA key
    dest_public_key = RSA.import_key(public_key_list)
    chypher_rsa = PKCS1_OAEP.new(dest_public_key)
    enc_session_key = chypher_rsa.encrypt(aes_key)

    return enc_session_key


def decrypt_message(rec_mess):

    aes = pyaes.AESModeOfOperationCTR(aes_key)
    # Decrypt base64 encrypted message
    d_base64 = base64.b64decode(rec_mess)
    # Decrypt the message with the AES key
    decrypted = aes.decrypt(d_base64).decode('ISO-8859-1')

    return decrypted


if __name__ == "__main__":
    print("[*] Run incogn1to.py!")
