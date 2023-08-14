from TSL2591 import TSL2591
import time
from iotdb_helper import beijingts, ip, port_, username_, password_
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.Session import Session
from device_master import device_id


def light_sensor_worker():
    sensor = TSL2591()
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    device = device_id + ".light_sensor"
    session.set_storage_group(device)
    series_config = {
        "measurements": [
            "light_sensor_lux",
            "light_sensor_infrared_light",
            "light_sensor_visible_light",
            "light_sensor_full_spectrum_light",
        ],
        "datatypes": [TSDataType.INT64 for i in range(4)],
    }
    session.create_aligned_time_series(
        device,
        series_config["measurements"],
        series_config["datatypes"],
        [TSEncoding.PLAIN for i in range(4)],
        [Compressor.SNAPPY for i in range(4)],
    )
    while True:
        try:
            lux = sensor.Lux
            sensor.TSL2591_SET_LuxInterrupt(50, 200)
            infrared = sensor.Read_Infrared
            visible = sensor.Read_Visible
            full_spectrum = sensor.Read_FullSpectrum
            light_record = (lux, infrared, visible, full_spectrum)
            session.insert_aligned_record(
                device,
                beijingts(),
                series_config["measurements"],
                series_config["datatypes"],
                list(light_record),
            )
            print("sent: {} | {} | {}".format(*light_record))
        except Exception as e:
            print("except: {}".format(type(e)))
        finally:
            time.sleep(3)


if __name__ == "__main__":
    light_sensor_worker()
