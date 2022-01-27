from . import peer_pb2 as peer
from cryptography.hazmat.backends import default_backend
import cryptography.hazmat.primitives.serialization as serial
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import ec


# 从pem文件中得到私钥
def __get_pvkey(fpath, password=None):
    input_file = open(fpath, 'rb')
    input = input_file.read()
    input_file.close()
    pvkey = serial.load_pem_private_key(input, password, default_backend())
    return pvkey


if __name__ == '__main__':
    trans = peer.Transaction()
