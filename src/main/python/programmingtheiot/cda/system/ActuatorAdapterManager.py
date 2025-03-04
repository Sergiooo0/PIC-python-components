#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

from importlib import import_module

class ActuatorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self, dataMsgListener: IDataMessageListener = None):
		self.configUtil = ConfigUtil()
		self.dataMsgListener = dataMsgListener
		self.useSimulator = self.configUtil.getBoolean(
			section = ConfigConst.CONSTRAINED_DEVICE, 
			key = ConfigConst.ENABLE_SIMULATOR_KEY)
		
		self.useEmulator = self.configUtil.getBoolean(
			section = ConfigConst.CONSTRAINED_DEVICE, 
			key = ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.deviceID = self.configUtil.getProperty(
			section = ConfigConst.CONSTRAINED_DEVICE, 
			key = ConfigConst.DEVICE_ID_KEY,
			defaultVal = ConfigConst.NOT_SET)
		
		self.locationID = self.configUtil.getProperty(
			section = ConfigConst.CONSTRAINED_DEVICE, 
			key = ConfigConst.DEVICE_LOCATION_ID_KEY,
			defaultVal = ConfigConst.NOT_SET)
		
		self.humidifierActuator = None
		self.hvacActuator = None
		self.ledDisplayActuator = None

		self._initEnvironmentalActuationTask()

	def _initEnvironmentalActuationTask(self):
		if self.useSimulator:
			logging.info("ActuatorAdapterManager using SIMULATED ActuatorData instance.")
			self.humidifierActuator = HumidifierActuatorSimTask()
			self.hvacActuator = HvacActuatorSimTask()
		elif self.useEmulator:
			logging.info("ActuatorAdapterManager using EMULATED ActuatorData instance.")
			# load the environmental tasks for simulated actuation
			hueModule=import_module('programmingtheiot.cda.emulated.HumidifierEmulatorTask','HumidiferEmulatorTask')
			hueClazz=getattr(hueModule,'HumidifierEmulatorTask')
			self.humidifierActuator=hueClazz()

			# create the HVAC actuator emulator
			hveModule=import_module('programmingtheiot.cda.emulated.HvacEmulatorTask','HvacEmulatorTask')
			hveClazz=getattr(hveModule,'HvacEmulatorTask')
			self.hvacActuator=hveClazz()

			# create the LED display actuator emulator
			leDisplayModule=import_module('programmingtheiot.cda.emulated.LedDisplayEmulatorTask','LedDisplayEmulatorTask')
			leClazz=getattr(leDisplayModule,'LedDisplayEmulatorTask')
			self.ledDisplayActuator=leClazz()

	def sendActuatorCommand(self, data: ActuatorData) -> ActuatorData:
		if data and not data.isResponseFlagEnabled():
			# first check if the actuation event is destined for this device
			if data.getLocationID() == self.locationID:
				logging.info(f"Actuator command received for location ID {str(data.getLocationID())}. Processing...")

				aType = data.getTypeID()
				responseData = None

				# TODO: implement appropriate logging and error handling
				if aType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and self.humidifierActuator:
					responseData = self.humidifierActuator.updateActuator(data)
				elif aType == ConfigConst.HVAC_ACTUATOR_TYPE and self.hvacActuator:
					responseData = self.hvacActuator.updateActuator(data)
				elif aType == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and self.ledDisplayActuator:
					responseData = self.ledDisplayActuator.updateActuator(data)
				else:
					logging.warning("No valid actuator type. Ignoring actuation for type: %s", data.getTypeID())

				# TODO: in a later lab module, the responseData instance will be
				# passed to a callback function implemented in DeviceDataManager
				# via IDataMessageListener

				return responseData
			else:
				logging.warning(f"Location ID doesn't match. Ignoring actuation: (me) {str(self.locationID)} != (you) {str(data.getLocationID())}")
		else:
			logging.warning("Actuator request received. Message is empty or response. Ignoring.")

		return None
	
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if listener:
			self.dataMsgListener = listener
			return True
		else:
			return False
