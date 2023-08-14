import Adafruit_DHT
import time
from iotdb_helper import beijingts, ip, port_, username_, password_
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.Session import Session
from device_master import device_id


def getHT():
    d = {}
    sensor = Adafruit_DHT.DHT11
    pin = 17
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        return round(humidity, 1), round(temperature, 1)
    else:
        raise Exception("DHT11 no response")


def dht11worker():
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    device = device_id + ".dht11"
    session.set_storage_group(device)
    series_config = {
        "measurements": [
            "dht11_humidity",
            "dht11_temperature",
        ],
        "datatypes": [TSDataType.FLOAT for i in range(2)],
    }
    session.create_aligned_time_series(
        device,
        series_config["measurements"],
        series_config["datatypes"],
        [TSEncoding.PLAIN for i in range(2)],
        [Compressor.SNAPPY for i in range(2)],
    )
    while True:
        try:
            ht = getHT()
            session.insert_aligned_record(
                device,
                beijingts(),
                series_config["measurements"],
                series_config["datatypes"],
                list(ht),
            )
            print("sent: {} | {}".format(*ht))
        except Exception as e:
            print("except: {}".format(type(e)))
            raise e
        finally:
            time.sleep(3)


if __name__ == "__main__":
    dht11worker()
