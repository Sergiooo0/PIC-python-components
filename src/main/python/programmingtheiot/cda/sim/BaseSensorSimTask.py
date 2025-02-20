#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import random

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.SensorData import SensorData

from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataSet

from abc import ABC

class BaseSensorSimTask(ABC):
	"""
	Shell representation of class for student implementation.
	
	"""

	DEFAULT_MIN_VAL = ConfigConst.DEFAULT_VAL
	DEFAULT_MAX_VAL = 1000.0
	
	def __init__(self, name:str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE,
			   dataSet:SensorDataSet = None, minVal: float = DEFAULT_MIN_VAL, maxVal: float = DEFAULT_MAX_VAL):
		self.dataSet = dataSet
		self.name = name
		self.typeID = typeID
		self.dataSetIndex = 0
		self.useRandomizer = False

		self.latestSensorData = None

		if not self.dataSet:
			self.useRandomizer = True
		
		self.minValue = minVal
		self.maxValue = maxVal
	
	def generateTelemetry(self) -> SensorData:
		"""
		Implement basic logging and SensorData creation. Sensor-specific functionality
		should be implemented by sub-class.
		
		A local reference to SensorData can be contained in this base class.
		"""
		sensorData = SensorData(typeID = self.typeID, name = self.name)
		sensorVal = ConfigConst.DEFAULT_VAL

		if self.useRandomizer:
			sensorVal = random.uniform(self.minValue, self.maxValue)
		else:
			sensorVal = self.dataSet.getDataEntry(self.dataSetIndex)
			self.dataSetIndex = (self.dataSetIndex + 1) % self.dataSet.getDataEntryCount()

		sensorData.setValue(sensorVal)
		self.latestSensorData = sensorData
		return self.latestSensorData
	
	def getTelemetryValue(self) -> float:
		"""
		If a local reference to SensorData is not None, simply return its current value.
		If SensorData hasn't yet been created, call self.generateTelemetry(), then return
		its current value.
		"""
		if not self.latestSensorData:
			self.generateTelemetry()

		return self.latestSensorData.getValue()
	
	def getLatestTelemetry(self) -> SensorData:
		"""
		This can return the current SensorData instance or a copy.
		"""
		return self.latestSensorData
	
	def getName(self) -> str:
		return self.name
	
	def getTypeID(self) -> int:
		return self.typeID
	