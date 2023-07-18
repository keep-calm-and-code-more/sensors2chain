from SGP40 import SGP40
from sensirion_gas_index_algorithm.voc_algorithm import VocAlgorithm
import time
from iotdb_helper import beijingts, ip, port_, username_, password_
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.Session import Session



def sgp40worker():
    sgp = SGP40()
    voc_algorithm = VocAlgorithm()
    time.sleep(0.5)
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    device = "root.rciot.pi_01.sgp40"
    session.set_storage_group(device)
    series_config = {
        "measurements": [
            "sgp40_voc_raw",
            "sgp40_voc_index",
        ],
        "datatypes": [TSDataType.INT64, TSDataType.FLOAT],
    }

    while True:
        try:
            # print("Raw Gas: ", sgp.raw())
            s_voc_raw = sgp.measureRaw(27, 45)
            voc_index = voc_algorithm.process(s_voc_raw)
            session.insert_aligned_record(
                    device,
                    beijingts(),
                    series_config["measurements"],
                    series_config["datatypes"],
                    [s_voc_raw, voc_index],
                )
            print("sent: {} | {}".format(s_voc_raw, voc_index))
        except Exception as e:
            print("except: {}".format(type(e)))
        finally:
            time.sleep(1)  # voc算法明确要求1s

if __name__ == "__main__":
    sgp40worker()