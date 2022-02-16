import serial
import time
import json
from typing import Union
import zlib


class Modem(object):

    def __init__(self):
        self.ser = None

    def initSer(self, port='COM6'):
        self.ser = Modem.ser = serial.Serial(port=port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)

    def close(self):
        self.ser.close()


def sendCMD(cmd: Union[str, bytes], timeout=10, modem=None):
    if (modem is None) or (modem.ser is None):
        modem = Modem()
        modem.initSer()
    if type(cmd) is str:
        cmdenc = cmd.encode('utf-8')
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
    sendCMD('AT+CNMP=38')
    sendCMD('AT+CMNB=2')
    sendCMD('AT+NBSC=1')
    sendCMD('AT+CIPSHUT')
    sendCMD('AT+CGNAPN')
    sendCMD('AT+CSTT="cmnbiot"')
    sendCMD('AT+CIICR')
    sendCMD('AT+CIFSR')


def sendMsg(msg: str):
    length = len(msg)
    sendCMD('AT+CIPSTART="TCP","159.226.5.116",23300')
    time.sleep(2)
    sendCMD('AT+CIPSEND={}'.format(length))
    sendCMD(msg)
    sendCMD('AT+CIPCLOSE=1')


if __name__ == '__main__':
    from main import create_trans_invoke, default_config
    params = {"test": 1, "test2": 26.5, "test3": 99, "test4": 1087, "test5": False}
    trans_signed = create_trans_invoke("ContractAssetsTPL", 1, "putProof", json.dumps(params), sign_config=default_config)
    # print(len(bytes2hexstr(trans_signed.SerializeToString())))
    # print(len(bytes2base64str(trans_signed.SerializeToString())))
    print(len(trans_signed.SerializeToString()))
    # print(len(zlib.compress(trans_signed.SerializeToString(),0))) #  worse than raw
    # configModem()
    # sendMsg(trans_signed.SerializeToString())
