import datetime
import pytz
from iotdb.Session import Session
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor


def beijingts():
    # 获取当前时间的 datetime 对象
    now = datetime.datetime.now()

    # 创建一个表示 +0800 时区的对象
    tz = pytz.timezone("Asia/Shanghai")

    # 将当前时间转换为 +0800 时区的时间
    local_now = tz.localize(now)

    # 将 +0800 时区的时间转换为 UTC 时间
    utc_now = local_now.astimezone(pytz.utc)

    # 获取 UTC 时间的时间戳（整数类型）
    timestamp = int(utc_now.timestamp() * 1000)
    return timestamp


class IOTDBhelper(object):
    def __init__(self):
        ip = "127.0.0.1"
        port_ = "6667"
        username_ = "root"
        password_ = "root"
        self.device_id = "root.rciot.pi_01"
        self.session = Session(
            ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8"
        )
        self.session.open(False)
        self.session.set_storage_group(self.device_id)

    def checkSeries(self, sensorName):
        sensorFullName = "root.rciot.pi_01.{}".format(sensorName)
        r = self.session.check_time_series_exists(sensorFullName)
        print("{} expecting True, checking result: {}".format(sensorFullName, r))

    def __del__(self):
        self.session.close()


if __name__ == "__main__":
    ip = "127.0.0.1"
    port_ = "6667"
    username_ = "root"
    password_ = "root"
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    session.set_storage_group("root.rciot.pi_01")
    session.create_time_series(
        "root.rciot.pi_01.s_DHT22",
        TSDataType.FLOAT,
        TSEncoding.PLAIN,
        Compressor.SNAPPY,
    )
    print(
        "root.rciot.pi_01.s_DHT22 expecting True, checking result: ",
        session.check_time_series_exists("root.rciot.pi_01.s_DHT22"),
    )

    session.insert_record(
        "root.rciot.pi_01", beijingts(), ["s_DHT22"], [TSDataType.FLOAT], [28.6]
    )

    # session.close()
