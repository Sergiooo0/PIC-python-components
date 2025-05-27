#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# You may find it more helpful to your design to adjust the
# functionality, constants and interfaces (if there are any)
# provided within in order to meet the needs of your specific
# Programming the Internet of Things project.
# 

import argparse
import logging

from time import sleep

from programmingtheiot.common.ConfigUtil import ConfigUtil
import programmingtheiot.common.ConfigConst as ConfigConst


from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager
from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager

logging.basicConfig(format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s', level = logging.DEBUG)

class ConstrainedDeviceApp():
	"""
	Definition of the ConstrainedDeviceApp class.
	
	"""
	
	def __init__(self, device_id: int = None):
		"""
		Initialization of class.
		
		@param path The name of the resource to apply to the URI.
		"""
		logging.info("Initializing CDA...")
		
		self.device_id = device_id
		if self.device_id is not None:
			self.location_id = ConfigUtil().getProperty(
				ConfigConst.CONSTRAINED_DEVICE, 
				ConfigConst.DEVICE_STANDARD_LOCATION_ID_KEY
			)
			self.location_id += str(self.device_id)
			ConfigUtil().setLocationID(self.location_id)
			logging.info(f"Device location ID set to: {self.location_id}")
		else:
			logging.info("Initializing CDA with no specific ID.")

		#self.sysPerfMgr = SystemPerformanceManager()
		self.dataMgr = DeviceDataManager()

	def startApp(self):
		"""
		Start the CDA. Calls startManager() on the device data manager instance.
		
		"""
		logging.info("Starting CDA...")

		#self.sysPerfMgr.startManager() #deviceDataManager already starts the system performance manager
		self.dataMgr.startManager()
		
		logging.info("CDA started.")

	def stopApp(self, code: int):
		"""
		Stop the CDA. Calls stopManager() on the device data manager instance.
		
		"""
		logging.info("CDA stopping...")
		
		#self.sysPerfMgr.stopManager()
		self.dataMgr.stopManager()
		
		logging.info("CDA stopped with exit code %s.", str(code))
		
	def parseArgs(self, args):
		"""
		Parse command line args.
		
		@param args The arguments to parse.
		"""
		logging.info("Parsing command line args...")

def parseArgs():
	"""
	Parse command line args and return them.
	"""
	parser = argparse.ArgumentParser(description='Constrained Device App')
	parser.add_argument('--id', type=int, help='Optional device ID (e.g., 1, 2, 3...)')
	return parser.parse_args()

def main():
	"""
	Main function definition for running client as application.
	
	Current implementation runs forever.
	"""
	args = parseArgs()
	device_id = args.id if args.id is not None else None

	cda = ConstrainedDeviceApp(device_id=device_id)
	cda.startApp()

	runForever = ConfigUtil().getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.RUN_FOREVER_KEY)
	if runForever:
		while True:
			sleep(5)
	else:
	
		# run for 4 minutos - this can be changed as needed
		sleep(240)
		
		# optionally stop the app - this can be removed if needed
		cda.stopApp(0)

if __name__ == '__main__':
	"""
	Attribute definition for when invoking as app via command line
	"""
	main()
	