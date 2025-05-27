import unittest
import logging
import time

from programmingtheiot.cda.emulated.VibrationActuatorTask import VibrationActuatorTask
from programmingtheiot.data.ActuatorData import ActuatorData
import programmingtheiot.common.ConfigConst as ConfigConst

class VibrationActuatorTaskTest(unittest.TestCase):
    """
    Test class for VibrationActuatorTask class.
    It verifies the proper functioning of the vibration alert system.
    """

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        cls.logger = logging.getLogger(__name__)

    def setUp(self):
        self.actuator = VibrationActuatorTask()

    def tearDown(self):
        self.actuator = None

    def create_actuator_data(self, val: float, state: str) -> ActuatorData:
        """
        Helper method to create ActuatorData instances for testing.
        
        @param val: The vibration value in G's
        @param state: The state string (NORMAL, WARNING, CRITICAL)
        @return: Configured ActuatorData instance
        """
        data = ActuatorData(
            name=ConfigConst.VIBRATION_ACTUATOR_NAME,
            typeID=ConfigConst.VIBRATION_ACTUATOR_TYPE
        )
        data.setCommand(ConfigConst.COMMAND_ON)
        data.setValue(val)
        data.setStateData(state)
        return data

    def test_init(self):
        """
        Test proper initialization of the actuator
        """
        self.assertIsNotNone(self.actuator)
        self.assertIsNotNone(self.actuator.sh)

    def test_normal_state(self):
        """
        Test actuator behavior with normal vibration levels
        """
        data = self.create_actuator_data(0.9, "NORMAL")
        response = self.actuator.updateActuator(data)
        
        self.assertIsNotNone(response)
        self.assertEqual(response.getStatusCode(), 0)
        self.logger.info("Normal state test complete")

    def test_warning_state(self):
        """
        Test actuator behavior with warning vibration levels
        """
        data = self.create_actuator_data(2.5, "WARNING")
        response = self.actuator.updateActuator(data)
        
        self.assertIsNotNone(response)
        self.assertEqual(response.getStatusCode(), 0)
        self.logger.info("Warning state test complete")

    def test_critical_state(self):
        """
        Test actuator behavior with critical vibration levels
        """
        data = self.create_actuator_data(5.5, "CRITICAL")
        response = self.actuator.updateActuator(data)
        
        self.assertIsNotNone(response)
        self.assertEqual(response.getStatusCode(), 0)
        self.logger.info("Critical state test complete")

    def test_state_transition(self):
        """
        Test actuator behavior through different states
        """
        # Test progression from normal to critical
        states = [
            (0.9, "NORMAL"),
            (2.5, "WARNING"),
            (5.5, "CRITICAL")
        ]
        
        for val, state in states:
            data = self.create_actuator_data(val, state)
            response = self.actuator.updateActuator(data)
            
            self.assertIsNotNone(response)
            self.assertEqual(response.getStatusCode(), 0)
            self.logger.info(f"State transition test - {state} complete")
            time.sleep(1)  # Give time for message to display

    def test_deactivation(self):
        """
        Test proper deactivation of the actuator
        """
        # First activate with some state
        data = self.create_actuator_data(2.5, "WARNING")
        self.actuator.updateActuator(data)
        
        # Then deactivate
        data = ActuatorData(
            name=ConfigConst.VIBRATION_ACTUATOR_NAME,
            typeID=ConfigConst.VIBRATION_ACTUATOR_TYPE
        )
        data.setCommand(ConfigConst.COMMAND_OFF)
        response = self.actuator.updateActuator(data)
        
        self.assertIsNotNone(response)
        self.assertEqual(response.getStatusCode(), 0)
        self.logger.info("Deactivation test complete")

if __name__ == '__main__':
    unittest.main() 