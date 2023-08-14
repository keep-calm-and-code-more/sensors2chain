import time
from iotdb_helper import beijingts, ip, port_, username_, password_
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.Session import Session
import smbus as smbus
import RPi.GPIO as GPIO
from device_master import device_id

ADC = smbus.SMBus(1)

flame_ain_raw = 0x14
flame_ain_v = 0x24
flame_ain_p = 0x34


def uv_sensor_worker():
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    device = device_id + ".uv_sensor"
    session.set_storage_group(device)
    series_config = {
        "measurements": [
            "uv_sensor_raw_10bit",
        ],
        "datatypes": [TSDataType.INT32 for i in range(1)],
    }
    session.create_aligned_time_series(
        device,
        series_config["measurements"],
        series_config["datatypes"],
        [TSEncoding.PLAIN for i in range(1)],
        [Compressor.SNAPPY for i in range(1)],
    )
    while True:
        try:
            uv_sensor_raw = ADC.read_word_data(0x24, flame_ain_raw)
            session.insert_aligned_record(
                device,
                beijingts(),
                series_config["measurements"],
                series_config["datatypes"],
                [uv_sensor_raw],
            )
            print("sent: {}".format(uv_sensor_raw))
        except Exception as e:
            print("except: {}".format(type(e)))
            raise e
        finally:
            time.sleep(3)


if __name__ == "__main__":
    uv_sensor_worker()
