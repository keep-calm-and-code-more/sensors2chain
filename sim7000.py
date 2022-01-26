import serial
import time
class Modem(object):

    def __init__(self):
        self.ser = None

    def initSer(self, port='COM6'):
        self.ser = Modem.ser = serial.Serial(port=port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)

    def close(self):
        self.ser.close()


def send(cmd, timeout=10):
    modem = Modem()
    modem.initSer()
    modem.ser.write(cmd.encode('utf-8') + b"\r\n")
    t_start = time.time()
    while True:
        if modem.ser.in_waiting:
            lines = modem.ser.readlines()
            lines = [i.decode("utf-8").strip() for i in lines]
            print(lines)
            ate_command = lines[0]
            print(ate_command == cmd)
            echo = lines[-1]
            print(echo)
            break
        if (time.time() - t_start) > timeout:
            print("Timeout")
        time.sleep(0.05)
    modem.close()


if __name__ == '__main__':
    send("AT")
    send("AT+CGNAPN")
