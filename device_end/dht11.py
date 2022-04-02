import Adafruit_DHT
import time


def getHT():
    d = {}
    sensor = Adafruit_DHT.DHT11
    pin = 17
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        d["H"] = "{}%".format(humidity)
        d["T"] = "{}*C".format(temperature)
        d["ts"] = int(time.time() * 1000)
        return d
    else:
        return None
