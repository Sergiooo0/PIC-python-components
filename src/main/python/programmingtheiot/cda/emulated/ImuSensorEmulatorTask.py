#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
from pisense import SenseHAT
import math
import time

from programmingtheiot.data.SensorData import SensorData
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask

class ImuSensorEmulatorTask(BaseSensorSimTask):
    """
    Emulator task for IMU (Inertial Measurement Unit) sensor using SenseHAT.
    Calculates the total vibration magnitude from all three axes (x, y, z),
    which can be used for:
    - Machine vibration monitoring
    - Equipment stability monitoring
    - Structural health monitoring
    
    The magnitude represents the total acceleration force in G's (1G = 9.81 m/s^2)
    
    Typical G-force ranges:
    - ~1G: Normal (just gravity)
    - 1-2G: Light vibration
    - 2-5G: Moderate vibration
    - >5G: Severe vibration/potential equipment issue
    """

    def __init__(self):
        """
        Initialize the IMU sensor emulator using SenseHAT
        """
        super(ImuSensorEmulatorTask, self).__init__(
            name=ConfigConst.IMU_SENSOR_NAME,
            typeID=ConfigConst.IMU_SENSOR_TYPE
        )
        
        self.logger = logging.getLogger(__name__)
        
        try:
            enableEmulation = ConfigUtil().getBoolean(
                ConfigConst.CONSTRAINED_DEVICE, 
                ConfigConst.ENABLE_EMULATOR_KEY
            )
            
            self.sh = SenseHAT(emulate=enableEmulation)
            self.logger.info("IMU sensor emulator initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing IMU sensor emulator: {str(e)}")
            raise

    def generateTelemetry(self) -> SensorData:
        """
        Generates IMU sensor telemetry by calculating the total vibration magnitude
        from all three acceleration axes (x, y, z).
        
        The magnitude is calculated as: sqrt(x² + y² + z²)
        Values above 1G indicate additional forces beyond gravity.
        
        :return: SensorData containing the total vibration magnitude in G's
        """
        try:
            # Get acceleration data from all axes
            accel = self.sh.imu.accel
            
            # Wait briefly if accelerometer data isn't ready
            if accel is None:
                time.sleep(0.1)
                accel = self.sh.imu.accel
            
            # If we still don't have data, return 0
            if accel is None:
                raise ValueError("Unable to read accelerometer data")
            
            # Calculate total vibration magnitude using all three axes
            vibration_magnitude = math.sqrt(
                accel.x**2 + 
                accel.y**2 + 
                accel.z**2
            )
            
            # Create sensor data with vibration magnitude
            sensorData = SensorData(
                name=self.getName(),
                typeID=self.getTypeID()
            )
            
            # Set the vibration magnitude value
            sensorData.setValue(vibration_magnitude)
            self.latestSensorData = sensorData
            
            return sensorData
            
        except Exception as e:
            self.logger.error(f"Error generating IMU telemetry: {str(e)}")
            # Create a default sensor data with 0 value when there's an error
            sensorData = SensorData(
                name=self.getName(),
                typeID=self.getTypeID()
            )
            sensorData.setValue(0.0)
            return sensorData


if __name__ == '__main__':
    import time
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Create and test the IMU sensor emulator
    imuTask = ImuSensorEmulatorTask()
    
    print("\nTesting IMU sensor emulator with vibration readings...")
    print("Note: Values around 1.0G are normal (gravity)")
    print("      Values >1.0G indicate additional forces/vibration")
    print("      Values >5.0G indicate severe vibration\n")
    
    for i in range(5):
        data = imuTask.generateTelemetry()
        magnitude = data.getValue()
        
        status = "NORMAL"
        if magnitude > 5.0:
            status = "SEVERE"
        elif magnitude > 2.0:
            status = "MODERATE"
        elif magnitude > 1.2:
            status = "LIGHT"
            
        print(f"Reading {i + 1}: {magnitude:.3f}G - {status}")
        time.sleep(1)
