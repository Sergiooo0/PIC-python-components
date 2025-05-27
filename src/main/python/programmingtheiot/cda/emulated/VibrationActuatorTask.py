#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask
from programmingtheiot.data.ActuatorData import ActuatorData
from pisense import SenseHAT

class VibrationActuatorTask(BaseActuatorSimTask):
    """
    Actuator task for vibration alerts using SenseHAT LED matrix.
    Displays different messages based on vibration severity:
    - Normal (< 1.2G): - No display
    - Warning (1.2G - 5G): - "WARN"
    - Critical (> 5G): - "CRIT"
    """

    def __init__(self):
        super(VibrationActuatorTask, self).__init__(
            name=ConfigConst.VIBRATION_ACTUATOR_NAME,
            typeID=ConfigConst.VIBRATION_ACTUATOR_TYPE,
            simpleName="VIB"
        )
        
        self.logger = logging.getLogger(__name__)
        
        enableEmulation = ConfigUtil().getBoolean(
            ConfigConst.CONSTRAINED_DEVICE, 
            ConfigConst.ENABLE_EMULATOR_KEY
        )
        
        self.sh = SenseHAT(emulate=enableEmulation)
        self.current_state = "NORMAL"

    def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        """
        Activate the vibration alert display based on the severity level.
        
        @param val: The vibration magnitude in G's
        @param stateData: The severity state ("NORMAL", "WARNING", "CRITICAL")
        @return: 0 if successful, -1 if there's an error
        """
        if not self.sh.screen:
            self.logger.warning("No SenseHAT LED screen instance available.")
            return -1

        try:
            # Update state only if provided
            if stateData:
                self.current_state = stateData.upper()

            # Choose color and message based on state
            if self.current_state == "CRITICAL":
                msg = "CRIT: " + str(round(val, 2)) + "G"
            elif self.current_state == "WARNING":
                msg = "WARN: " + str(round(val, 2)) + "G"
            else:
                msg = "OK: " + str(round(val, 2)) + "G"
            
            # Scroll message
            self.sh.screen.scroll_text(msg)
            
            return 0

        except Exception as e:
            self.logger.error(f"Error activating vibration actuator: {str(e)}")
            return -1

    def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        """
        Deactivate the vibration alert display.
        
        @return: 0 if successful, -1 if there's an error
        """
        if not self.sh.screen:
            self.logger.warning("No SenseHAT LED screen instance to clear.")
            return -1

        try:
            # Clear any messages and turn off display
            self.sh.screen.clear()
            self.current_state = "NORMAL"
            return 0
            
        except Exception as e:
            self.logger.error(f"Error deactivating vibration actuator: {str(e)}")
            return -1

if __name__ == '__main__':
    # Simple test of the actuator
    actuator = VibrationActuatorTask()
    
    print("Testing Vibration Actuator...")
    
    # Create ActuatorData instance for testing
    def create_actuator_data(val: float, state: str) -> ActuatorData:
        data = ActuatorData(
            name=ConfigConst.VIBRATION_ACTUATOR_NAME,
            typeID=ConfigConst.VIBRATION_ACTUATOR_TYPE
        )
        data.setCommand(ConfigConst.COMMAND_ON)
        data.setValue(val)
        data.setStateData(state)
        return data
    
    # Test normal state
    print("\nTesting NORMAL state...")
    actuator.updateActuator(create_actuator_data(0.9, "NORMAL"))
    sleep(2)
    
    # Test warning state
    print("\nTesting WARNING state...")
    actuator.updateActuator(create_actuator_data(2.5, "WARNING"))
    sleep(2)
    
    # Test critical state
    print("\nTesting CRITICAL state...")
    actuator.updateActuator(create_actuator_data(5.5, "CRITICAL"))
    sleep(2)
    
    # Test deactivation
    print("\nTesting deactivation...")
    data = ActuatorData(
        name=ConfigConst.VIBRATION_ACTUATOR_NAME,
        typeID=ConfigConst.VIBRATION_ACTUATOR_TYPE
    )
    data.setCommand(ConfigConst.COMMAND_OFF)
    actuator.updateActuator(data)
    sleep(1) 