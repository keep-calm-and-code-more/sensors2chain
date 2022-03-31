# -*-coding:utf-8-*-
from . import peer_pb2 as peer
import time
from google.protobuf import timestamp_pb2
import uuid
from cryptography.hazmat.backends import default_backend
import cryptography.hazmat.primitives.serialization as serial
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
import requests
import json
import binascii
import os


class Client:
    # 主机名,pem文件路径,pem文件密码,别名,证书名,用户名
    def __init__(
        self,
        host="localhost:8081",
        pem_path=os.path.join(
            os.path.dirname(__file__), "certs", "121000005l35120456.node1.pem"
        ),
        password=None,
        credit_code="121000005l35120456",
        cert_name="node1",
    ):
        self.host = host
        self.pem_path = pem_path
        self.password = password
        self.credit_code = credit_code
        self.cert_name = cert_name

    # 指定唯一合约:名称+版本号
    def __get_cid(self, chaincode_name, chaincode_ver):
        cid = peer.ChaincodeId()
        cid.chaincodeName = chaincode_name
        cid.version = int(chaincode_ver)
        return cid

    # 指定用于签名的证书:证书名+用户名
    def __get_certid(self):
        certid = peer.CertId()
        certid.credit_code = self.credit_code
        certid.cert_name = self.cert_name
        return certid

    # 从pem文件中得到私钥
    def __get_pvkey(self):
        input_file = open(self.pem_path, 'rb')
        input = input_file.read()
        input_file.close()
        pvkey = serial.load_pem_private_key(input, self.password, default_backend())
        return pvkey

    # 得到对交易的签名signature
    def __get_sig(self, transaction):
        # 生成时间戳
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        # 证书标识,时间戳,对整个交易的签名
        sig = peer.Signature()
        sig.cert_id.CopyFrom(self.__get_certid())
        sig.tm_local.CopyFrom(timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos))
        sig_bytes = self.__get_pvkey().sign(
            transaction.SerializeToString(), ec.ECDSA(hashes.SHA1())
        )
        sig.signature = sig_bytes
        return sig

    ##从文件路径得到内容
    def __get_code(self, package_path):
        f = open(package_path, 'rb')
        return f.read()

    # 创建设置状态交易:交易标识string,合约名称string,合约版本int,更改状态bool
    def create_trans_set_state(self, trans_id, chaincode_name, chaincode_ver, state):
        # 创建交易:交易标识符(如未指定，则随机),交易类型,指定合约,指定状态
        trans = peer.Transaction()
        if "" == trans_id:
            trans.id = str(uuid.uuid4())
        else:
            trans.id = trans_id
        trans.type = peer.Transaction.CHAINCODE_SET_STATE
        trans.cid.CopyFrom(self.__get_cid(chaincode_name, chaincode_ver))
        trans.state = state
        trans.signature.CopyFrom(self.__get_sig(trans))
        return trans

    # 创建部署/升级合约交易:交易标识string,合约名称string,合约版本int,合约代码类型string,
    # 超时时间int,合约路径string,法律描述string
    def create_trans_deploy(
        self,
        trans_id,
        chaincode_name,
        chaincode_ver,
        chaincode_type,
        timeout=1000,
        package_path=os.path.dirname(__file__) + '\\contracts\\ConEvidence.scala',
        legalprose="",
    ):
        trans = peer.Transaction()
        if "" == trans_id:
            trans.id = str(uuid.uuid4())
        else:
            trans.id = trans_id
        ctype_dict = {
            "javascript": peer.ChaincodeDeploy.CODE_JAVASCRIPT,
            "scala": peer.ChaincodeDeploy.CODE_SCALA,
            "scalaparallel": peer.ChaincodeDeploy.CODE_SCALA_PARALLEL,
        }
        ctype = ctype_dict.get(chaincode_type)
        if None == ctype:
            ctype = peer.ChaincodeDeploy.CODE_UNDEFINED
        trans.type = peer.Transaction.CHAINCODE_DEPLOY
        trans.cid.CopyFrom(self.__get_cid(chaincode_name, chaincode_ver))
        spec = peer.ChaincodeDeploy()
        spec.timeout = timeout
        spec.code_package = self.__get_code(package_path)
        spec.legal_prose = legalprose
        spec.ctype = ctype
        trans.spec.CopyFrom(spec)
        trans.signature.CopyFrom(self.__get_sig(trans))
        return trans

    # 创建调用合约交易:交易标识string,合约名称string,合约版本int,合约方法string,方法参数string
    def create_trans_invoke(
        self, trans_id, chaincode_name, chaincode_ver, func, params
    ):
        trans = peer.Transaction()
        if "" == trans_id:
            trans.id = str(uuid.uuid4())
        else:
            trans.id = trans_id
        trans.type = peer.Transaction.CHAINCODE_INVOKE
        trans.cid.CopyFrom(self.__get_cid(chaincode_name, chaincode_ver))
        ipt = peer.ChaincodeInput()
        ipt.function = func
        print(params)
        ipt.args.append(params)
        trans.ipt.CopyFrom(ipt)
        trans.signature.CopyFrom(self.__get_sig(trans))
        return trans

    ## 进行http请求
    def doPost(self, url, data):
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url=url, headers=headers, data=json.dumps(data))
        except requests.exceptions.Timeout as e:
            print('TimeOut: ' + str(e.message))
        except requests.exceptions.HTTPError as e:
            print('HTTPError: ' + str(e.message))
        return response

    # 提交带签名的交易
    def postTranByString(self, data):
        url = "http://" + self.host + "/transaction/postTranByString"
        # data类型为byte(bin),先转换成byte(hex),再转换成string(hex)
        data = binascii.hexlify(data.SerializeToString())
        jsonObject = self.doPost(url, data.decode('utf-8'))
        return jsonObject

    # 从交易id得到交易内容
    def getTransById(self, tx_id):
        url = "http://" + self.host + "/transaction/" + tx_id
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.get(url=url, headers=headers)
        except requests.exceptions.Timeout as e:
            print('TimeOut: ' + str(e.message))
        except requests.exceptions.HTTPError as e:
            print('HTTPError: ' + str(e.message))
        return response
