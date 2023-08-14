import time
from iotdb_helper import beijingts, ip, port_, username_, password_
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.Session import Session
import smbus as smbus
import RPi.GPIO as GPIO
from device_master import device_id

ADC = smbus.SMBus(1)

din = 22
in_raw = 0x10
GPIO.setmode(GPIO.BCM)
GPIO.setup(din, GPIO.IN)


def flame_sensor_worker():
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    device = device_id + ".flame_sensor"
    session.set_storage_group(device)
    series_config = {
        "measurements": ["flame_sensor_raw_10bit", "flame_sensor_alarm"],
        "datatypes": [TSDataType.INT32, TSDataType.BOOLEAN],
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
            sensor_raw = ADC.read_word_data(0x24, in_raw)
            alarm = not bool(GPIO.input(din))
            session.insert_aligned_record(
                device,
                beijingts(),
                series_config["measurements"],
                series_config["datatypes"],
                [sensor_raw, alarm],
            )
            print("sent: {}| {}".format(sensor_raw, alarm))
        except Exception as e:
            print("except: {}".format(type(e)))
            raise e
        finally:
            time.sleep(3)


if __name__ == "__main__":
    flame_sensor_worker()
