import logging
import psutil
import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask
from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask

class SystemDiskUtilTask(BaseSystemUtilTask):

	def __init__(self):
		super(SystemDiskUtilTask, self).__init__(
			name = ConfigConst.DISK_UTIL_NAME, 
			typeID = ConfigConst.DISK_UTIL_TYPE)
	
	def getTelemetryValue(self) -> float:
		return psutil.disk_usage("/home/sergio/Escritorio/PIC/PIC-python-components/src")[3]
	
if __name__ == "__main__":
	disk = SystemDiskUtilTask()
	print(disk.getTelemetryValue())