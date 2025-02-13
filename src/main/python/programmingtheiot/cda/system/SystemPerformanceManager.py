#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask

from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class SystemPerformanceManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		configUtil = ConfigUtil()
		self.pollRate = configUtil.getInteger(
			ConfigConst.CONSTRAINED_DEVICE, 
			key = ConfigConst.POLL_CYCLES_KEY, 
			defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
		
		self.localitionID = configUtil.getProperty(
			section = ConfigConst.CONSTRAINED_DEVICE, 
			key = ConfigConst.DEVICE_LOCATION_ID_KEY,
			defaultVal = ConfigConst.NOT_SET)
		
		if self.pollRate <= 0:
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES

		self.dataMsgListener = None

		#Note: The next four definitions are for different sub-task
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job(self.handleTelemetry, 
							   'interval', 
							   seconds = self.pollRate,
							   misfire_grace_time=10)
		
		self.cpuUtilTask = SystemCpuUtilTask()
		self.memUtilTask = SystemMemUtilTask()

	def handleTelemetry(self):
		cpuUtilPct=self.cpuUtilTask.getTelemetryValue()
		memUtilPct=self.memUtilTask.getTelemetryValue()

		logging.debug(f"CPU utilization is {str(cpuUtilPct)}%. Memory utilization is {str(memUtilPct)}%.")
		
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		pass
	
	def startManager(self):
		logging.info("Started SystemPerformanceManager.")

		if not self.scheduler.running:
			self.scheduler.start()
			logging.info("SystemPerformanceManager started.")
		else:
			logging.warning("SystemPerformanceManager scheduler is already running.")

	def stopManager(self):
		logging.info("Stopped SystemPerformanceManager.")

		try:
			self.scheduler.shutdown()
			logging.info("SystemPerformanceManager stopped.")
		except:
			logging.warning("SystemPerformanceManager scheduler already stopped.")
