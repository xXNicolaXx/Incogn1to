from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import pyaes
import base64
import listener
import sys


def rsa_key():

    global gen_rsa
    global private_key
    global public_key

    # Pair key generation
    gen_rsa = RSA.generate(2048)
    private_key = gen_rsa.export_key()
    public_key = gen_rsa.publickey().export_key()


def aes_encryption(plaintext):

    aes = pyaes.AESModeOfOperationCTR(listener.get_dec_aes())
    # Encrypt the plaintext with the AES key
    cipher_text = aes.encrypt(plaintext)
    base64text = base64.b64encode(cipher_text)

    return base64text


def decrypt_aes_key(dec_key):
    try:
        my_private_key = RSA.import_key(private_key)
        de_cypher_rsa = PKCS1_OAEP.new(my_private_key)
        # Obtain the AES key
        dec_session_key = de_cypher_rsa.decrypt(dec_key)
        return dec_session_key
    except ValueError:
        print("Incorrect decryption")
        sys.exit()


def decrypt_message(rec_mess):
    aes = pyaes.AESModeOfOperationCTR(listener.get_dec_aes())
    # Decrypt base64 encrypted message
    d_base64 = base64.b64decode(rec_mess)
    # Decrypt the message with the AES key
    decrypted = aes.decrypt(d_base64).decode('ISO-8859-1')

    return decrypted


# Public key to send
def get_public_key():
    return public_key


if __name__ == "__main__":
    print("[*] Run incogn1to.py!")
