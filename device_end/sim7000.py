import serial
import time
import json
from typing import Union
import binascii
from rcpy_wenwu import create_trans_invoke, default_config
import pdb


class Modem(object):
    def __init__(self):
        self.ser = None

    def initSer(self, port="COM5"):
        self.ser = Modem.ser = serial.Serial(
            port=port,
            baudrate=115200,
            bytesize=8,
            parity="N",
            stopbits=1,
            timeout=1,
            rtscts=True,
            dsrdtr=True,
        )

    def close(self):
        self.ser.close()


def sendCMD(cmd: Union[str, bytes], timeout=10, modem=None):
    if (modem is None) or (modem.ser is None):
        modem = Modem()
        modem.initSer()
    if isinstance(cmd, str):
        cmdenc = cmd.encode("utf-8")
    else:
        cmdenc = cmd
    modem.ser.write(cmdenc + b"\r\n")
    t_start = time.time()
    while True:
        if modem.ser.in_waiting:
            lines = modem.ser.readlines()
            try:
                lines = [i.decode("utf-8").strip() for i in lines]
                print(lines)
                ate_command = lines[0]
                print(ate_command == cmd)
                echo = lines[-1]
                print(echo)
            except UnicodeDecodeError:
                print(lines)
            break
        if (time.time() - t_start) > timeout:
            print("Timeout")
            break
        time.sleep(0.05)
    modem.close()


def configModem():
    sendCMD("AT+CNMP=38")
    sendCMD("AT+CMNB=2")
    sendCMD("AT+NBSC=1")
    sendCMD("AT+CIPSHUT")
    sendCMD("AT+CGNAPN")
    sendCMD('AT+CSTT="cmnbiot2"')
    sendCMD("AT+CIICR")
    sendCMD("AT+CIFSR")


def sendMsg(msg: str, ip: str, port: str):
    length = len(msg)
    sendCMD('AT+CIPSTART="TCP","{}",{}'.format(ip, port))
    time.sleep(2)
    sendCMD("AT+CIPSEND={}".format(length))
    sendCMD(msg)
    sendCMD("AT+CIPCLOSE=1")


def submitData(data: dict, ip: str, port: str):
    trans_signed = create_trans_invoke(
        "ContractAssetsTPL", 1, "putProof", json.dumps(data), sign_config=default_config
    )
    print(len(trans_signed.SerializeToString()))
    configModem()
    sendMsg(trans_signed.SerializeToString(), ip, port)


def sendPost(data: dict, url: str, scname: str, scversion: int, scmethod: str):
    databody = json.dumps(data, separators=(",", ":"))
    trans_signed_hex_str = json.dumps(
        binascii.hexlify(
            create_trans_invoke(
                scname, scversion, scmethod, databody, sign_config=default_config
            ).SerializeToString()
        ).decode("utf-8")
    )
    # pdb.set_trace()
    lendatabody = len(trans_signed_hex_str)
    sendCMD("AT+HTTPTERM")
    sendCMD("AT+SAPBR=0,1")
    sendCMD('AT+SAPBR=3,1,"APN","CMNBIOT2"')
    sendCMD("AT+SAPBR=1,1")
    sendCMD("AT+SAPBR=2,1")
    sendCMD("AT+HTTPINIT")
    sendCMD('AT+HTTPPARA="CID",1')
    sendCMD('AT+HTTPPARA="URL",{}'.format(url))
    sendCMD('AT+HTTPPARA="CONTENT","application/json"')
    time.sleep(3)
    sendCMD("AT+HTTPDATA={},10000".format(lendatabody))
    sendCMD(trans_signed_hex_str)
    sendCMD("AT+HTTPACTION=1")
    time.sleep(10)
    sendCMD("AT+HTTPREAD")
    time.sleep(10)


if __name__ == "__main__":
    params = {
        "id": "21749",
        "itemName": "someItem",
        "registerType": "拍行",
        "imgList": ["imgurl"],
        "ownerStr": "测试用户balabala",
        "ban": True,
    }
    sendPost(params, "http://124.16.137.94:19999/transaction/postTranByString")
    # submitData(params, "159.226.5.116", "23300")
    # print(len(bytes2hexstr(trans_signed.SerializeToString())))
    # print(len(bytes2base64str(trans_signed.SerializeToString())))
    # print(len(zlib.compress(trans_signed.SerializeToString(),0))) #  worse than raw
    # configModem()
    # sendMsg(trans_signed.SerializeToString())
    pass
