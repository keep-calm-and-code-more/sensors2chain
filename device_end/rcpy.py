import peer_pb2 as peer
from google.protobuf import timestamp_pb2
import time
import uuid
import json
import binascii
import base64
import requests
import zlib
from cryptography.hazmat.backends import default_backend
import cryptography.hazmat.primitives.serialization as serial
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

default_config = {"credit_code": "121000005l35120456", "cert_name": "node1", "pvkey_path": "./somekey.pem"}


def __get_pvkey(fpath: str, password: str = None):
    """从pem文件中得到私钥

    Args:
        fpath (TYPE): Description
        password (None, optional): Description

    Returns:
        TYPE: Description
    """
    input_file = open(fpath, 'rb')
    input = input_file.read()
    input_file.close()
    pvkey = serial.load_pem_private_key(input, password, default_backend())
    return pvkey


def __get_sig(transaction, config: dict):
    # 生成时间戳
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    # 证书标识,时间戳,对整个交易的签名
    sig = peer.Signature()
    certid = peer.CertId()
    certid.credit_code = config["credit_code"]
    certid.cert_name = config["cert_name"]
    sig.cert_id.CopyFrom(certid)
    sig.tm_local.CopyFrom(timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos))
    sig_bytes = __get_pvkey(config["pvkey_path"]).sign(
        transaction.SerializeToString(), ec.ECDSA(hashes.SHA1())
    )
    sig.signature = sig_bytes
    return sig


def create_trans_invoke(chaincode_name: str, chaincode_ver: str, func: str, params: str, sign_config: dict, trans_id: str = None):
    """创建签名交易

    Args:
        chaincode_name (str): Description
        chaincode_ver (str): Description
        func (str): Description
        params (str): Description
        sign_config (dict): Description
        trans_id (str, optional): Description

    Returns:
        Transaction: 签名交易
    """
    trans = peer.Transaction()
    if trans_id is None:
        trans.id = str(uuid.uuid4())
    else:
        trans.id = trans_id
    trans.type = peer.Transaction.CHAINCODE_INVOKE
    cid = peer.ChaincodeId()
    cid.chaincodeName = chaincode_name
    cid.version = chaincode_ver
    trans.cid.CopyFrom(cid)
    ipt = peer.ChaincodeInput()
    ipt.function = func
    print(params)
    ipt.args.append(params)
    trans.ipt.CopyFrom(ipt)
    trans.signature.CopyFrom(__get_sig(trans, sign_config))
    return trans


def __doPost(url, data):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
    except requests.exceptions.Timeout as e:
        print('TimeOut: ' + str(e.message))
    except requests.exceptions.HTTPError as e:
        print('HTTPError: ' + str(e.message))
    return response


def postTranByString(host, data):
    url = "http://" + host + "/transaction/postTranByString"
    # data.SerializeToString()类型为byte(bin),先转换成byte(hex),再转换成string(hex)
    data = binascii.hexlify(data.SerializeToString())
    jsonObject = __doPost(url, data.decode('utf-8'))
    return jsonObject


def bytes2hexstr(obj: bytes):
    return binascii.hexlify(obj).decode('utf-8')


def bytes2base64str(obj: bytes):
    return base64.b64encode(obj).decode('utf-8')


# if __name__ == '__main__':
#     params = {"test": 1}
#     trans_signed = create_trans_invoke("ContractAssetsTPL", 1, "putProof", json.dumps(params), sign_config=default_config)
#     trans_signed_str = bytes2hexstr(trans_signed.SerializeToString())
#     print(trans_signed_str)
#     print(len(trans_signed_str))
#     trans_signed_str_compressed = bytes2hexstr(zlib.compress(trans_signed.SerializeToString()))

#     print(trans_signed_str_compressed)
#     print(len(trans_signed_str_compressed))
#     # print(postTranByString("localhost:9081", trans_signed).text)
