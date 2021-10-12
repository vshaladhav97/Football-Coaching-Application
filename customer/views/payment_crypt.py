from Crypto.Cipher import AES
import binascii
from ..config import payments_variables

password_key = payments_variables.password_key
payment_server_url = payments_variables.payment_server_url

BS = 16
def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
def unpad(s): return s[0:-ord(s[-1])]


class SagepayCrypt:

    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)

        cipher = AES.new(self.key, AES.MODE_CBC, self.key)
        encrypted_text = binascii.hexlify(cipher.encrypt(raw))
        return encrypted_text.decode('utf-8').upper()

    def decrypt(self, enc):
        """
        Requires hex encoded param to decrypt
        """
        enc = binascii.unhexlify(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.key)
        decrypt = cipher.decrypt(enc)
        decrypted_text = decrypt.decode('utf8')
        unpadded = unpad(decrypted_text)
        return unpadded


def encrypted_data_url(data):
    """Encrypt payment gateway request data"""

    basket_data = data

    # Encypt the basket data using our key and padding
    result = SagepayCrypt(password_key).encrypt(basket_data)

    # print(result)
    # Post to the url
    url = payment_server_url + result
    # print(url)
  
    return url


def decrypted_data(data):
    """Decrypt payment gateway response"""
    decrypt = SagepayCrypt(password_key).decrypt(data)
    # print(decrypt)
    return decrypt
