import unittest
import logging
import time

from programmingtheiot.cda.emulated.ImuSensorEmulatorTask import ImuSensorEmulatorTask
from programmingtheiot.data.SensorData import SensorData

class ImuTest(unittest.TestCase):
    """
    Test class for the IMU sensor emulator.
    Tests basic functionality, data ranges, and error conditions.
    """

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        cls.logger = logging.getLogger("ImuTest")
        
    def setUp(self):
        self.imuEmulator = ImuSensorEmulatorTask()
        # Take a few readings to ensure the emulator is stable
        self._warm_up_sensor()
        
    def tearDown(self):
        self.imuEmulator = None

    def _warm_up_sensor(self, readings=3, delay=0.5):
        """
        Take a few readings to ensure the sensor is stable
        """
        for _ in range(readings):
            self.imuEmulator.generateTelemetry()
            time.sleep(delay)

    def test_init_and_config(self):
        """
        Tests if the IMU sensor emulator initializes correctly
        """
        self.assertIsNotNone(self.imuEmulator)
        self.assertIsNotNone(self.imuEmulator.sh)

    def test_generate_telemetry(self):
        """
        Tests if the IMU sensor generates valid telemetry data
        """
        sensorData = self.imuEmulator.generateTelemetry()
        
        self.assertIsNotNone(sensorData)
        self.assertIsInstance(sensorData, SensorData)
        self.assertGreater(sensorData.getValue(), 0.0)
        
        # Log the actual value for verification
        self.logger.info(f"Generated telemetry value: {sensorData.getValue():.3f}G")

    def test_multiple_readings(self):
        """
        Tests multiple consecutive readings to ensure consistency
        """
        readings = []
        
        # Take 5 readings
        for i in range(5):
            data = self.imuEmulator.generateTelemetry()
            value = data.getValue()
            readings.append(value)
            self.logger.info(f"Reading {i + 1}: {value:.3f}G")
            time.sleep(0.5)  # Short delay between readings
            
        # Verify all readings are valid
        for reading in readings:
            self.assertGreater(reading, 0.0)
            # When stationary, readings should be close to 1G
            self.assertGreaterEqual(reading, 0.8)
            self.assertLessEqual(reading, 1.2)

    def test_reading_ranges(self):
        """
        Tests if readings fall within expected ranges when device is stationary.
        In stationary state, acceleration should be around 1G due to gravity.
        """
        readings = []
        for i in range(3):  # Take multiple readings to ensure stability
            data = self.imuEmulator.generateTelemetry()
            value = data.getValue()
            readings.append(value)
            self.logger.info(f"Range test reading {i + 1}: {value:.3f}G")
            time.sleep(0.5)
        
        # Use the average of readings for more stable results
        avg_value = sum(readings) / len(readings)
        
        # When stationary, should be close to 1G (allowing for some variation)
        self.assertGreaterEqual(avg_value, 0.9)
        self.assertLessEqual(avg_value, 1.1)
        
        self.logger.info(f"Average stationary reading: {avg_value:.3f}G")

    def test_continuous_monitoring(self):
        """
        Tests continuous monitoring over a short period
        """
        duration = 3  # seconds
        interval = 0.5  # seconds
        readings = []
        max_reading = 0
        min_reading = float('inf')
        
        start_time = time.time()
        while time.time() - start_time < duration:
            data = self.imuEmulator.generateTelemetry()
            value = data.getValue()
            
            readings.append(value)
            max_reading = max(max_reading, value)
            min_reading = min(min_reading, value)
            
            self.logger.info(f"Continuous reading: {value:.3f}G")
            time.sleep(interval)
        
        avg_reading = sum(readings) / len(readings)
        
        self.logger.info(f"Monitoring Results:")
        self.logger.info(f"  Samples: {len(readings)}")
        self.logger.info(f"  Average: {avg_reading:.3f}G")
        self.logger.info(f"  Min: {min_reading:.3f}G")
        self.logger.info(f"  Max: {max_reading:.3f}G")
        
        # Verify readings are within reasonable bounds
        self.assertGreater(len(readings), 3)  # Should have multiple readings
        self.assertGreater(avg_reading, 0.8)  # Average should be near 1G
        self.assertLess(avg_reading, 1.2)

if __name__ == '__main__':
    unittest.main()
