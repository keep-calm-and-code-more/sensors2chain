from dht11worker import getHT
from BMP388 import BMP388
from flame_sensor_worker import getFlame
from MLX90614 import MLX90614
from TSL2591 import TSL2591
from mpu6050 import mpu6050
from mq5_gas_sensor_worker import getMQ5
from SGP40 import SGP40
from sensirion_gas_index_algorithm.voc_algorithm import VocAlgorithm
from tilt_sensor_worker import getTile
import unittest
import logging


class TestSensors(unittest.TestCase):
    def setUp(self):
        # 配置日志记录器
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def testDHT11(self):
        ht = getHT()
        logging.info("DHT11输出: 温度{}℃ |湿度{}%".format(*ht))

    def testBMP388(self):
        bmp388 = BMP388()
        r = bmp388.get_temperature_and_pressure_and_altitude()
        r = [i / 100.0 for i in r]
        logging.info("BMP388输出: 温度{}℃ |气压{}Pa |高度{}m".format(*r))

    def testFlame(self):
        sensor_raw, alarm = getFlame()
        logging.info("Flame输出: 是否触发{} |10bit格式原始输出{}".format(alarm, sensor_raw))

    def testInfrared(self):
        sensor = MLX90614()
        amb_obj_temp = (
            round(sensor.get_amb_temp(), 2),
            round(sensor.get_obj_temp(), 2),
        )
        logging.info("Infrared输出: 环境温度{}℃ |目标温度{}℃".format(amb_obj_temp[0], amb_obj_temp[1]))

    def testLight(self):
        sensor = TSL2591()
        lux = sensor.Lux
        sensor.TSL2591_SET_LuxInterrupt(50, 200)
        infrared = sensor.Read_Infrared
        visible = sensor.Read_Visible
        full_spectrum = sensor.Read_FullSpectrum
        light_record = (lux, infrared, visible, full_spectrum)
        logging.info("Light输出:光照读数{} Lux |红外原始读数{} |可见光原始读数 {} |全光谱原始读数{}".format(*light_record))

    def testMPU6050(self):
        sensor = mpu6050(0x68)
        logging.info("read_accel_range: {},read_gyro_range: {}".format(sensor.read_accel_range(), sensor.read_gyro_range()))
        accelerometer_data = sensor.get_accel_data()
        gyro_data = sensor.get_gyro_data()
        temperature = sensor.get_temp()
        logging.info(
            "MPU6050输出:x、y、z轴加速度（m/s^2）{} |x、y、z轴角速度（°/s） {} |温度{}℃".format(
                accelerometer_data, gyro_data, temperature
            )
        )

    def testMQ5(self):
        sensor_raw, alarm = getMQ5()
        logging.info("MQ5输出: 是否触发{} |10bit格式原始输出{}".format(alarm, sensor_raw))

    def testSGP40(self):
        sgp = SGP40()
        voc_algorithm = VocAlgorithm()
        s_voc_raw = sgp.measureRaw(27, 45)
        voc_index = voc_algorithm.process(s_voc_raw)  # 1-500
        logging.info("SGP40输出:原始输出{} |VOC指数{}".format(s_voc_raw, voc_index))

    def testTilt(self):
        count_of_shift = getTile()
        logging.info("Tilt输出:最近15s内触发次数 {}".format(count_of_shift))


if __name__ == "__main__":
    unittest.main()
