import time
from iotdb_helper import beijingts, ip, port_, username_, password_
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.Session import Session
import smbus as smbus
import RPi.GPIO as GPIO
from device_master import device_id
from iotdb_helper import suppress_err, restore_err

ADC = smbus.SMBus(1)

din = 23
in_raw = 0x11
GPIO.setmode(GPIO.BCM)
GPIO.setup(din, GPIO.IN)


def getMQ5():
    sensor_raw = ADC.read_word_data(0x24, in_raw)
    alarm = not bool(GPIO.input(din))
    return sensor_raw, alarm


def mq5_gas_sensor_worker():
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    device = device_id + ".mq5_gas_sensor"
    out = suppress_err()
    session.set_storage_group(device)
    series_config = {
        "measurements": ["mq5_gas_sensor_raw_10bit", "mq5_gas_sensor_alarm"],
        "datatypes": [TSDataType.INT32, TSDataType.BOOLEAN],
    }
    session.create_aligned_time_series(
        device,
        series_config["measurements"],
        series_config["datatypes"],
        [TSEncoding.PLAIN for i in range(2)],
        [Compressor.SNAPPY for i in range(2)],
    )
    restore_err(out)
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
            print("---MQ5传感器记录: {}| {}".format(sensor_raw, alarm))
        except Exception as e:
            print("except: {}".format(type(e)))
            raise e
        finally:
            time.sleep(3)


if __name__ == "__main__":
    mq5_gas_sensor_worker()
