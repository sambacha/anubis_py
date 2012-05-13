from .openssl.OpenSSL import openssl
from .openssl.OpenSSL_AES import OpenSSL_AES
from .python.Python_AES import Python_AES

class AES:

    @staticmethod
    def new(key, IV):
        if openssl.enabled:
            return OpenSSL_AES(key, IV)
        else:
            return Python_AES(key, IV)
