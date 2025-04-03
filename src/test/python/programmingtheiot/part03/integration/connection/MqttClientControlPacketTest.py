import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.data.DataUtil import DataUtil

class MqttClientControlPacketTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Executing the MqttClientControlPacketTest class...")

        self.cfg = ConfigUtil()

        # NOTE: Be sure to use a DIFFERENT clientID than that which is used
        # for your CDA when running separately from this test
        #
        # The clientID shown below is an example only - please use your own
        # unique value for this test
        self.mcc = MqttClientConnector(clientID = "MyTestControlPacket")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConnectAndDisconnect(self):
        # TODO: implement this test
        pass

    def testServerPing(self):
        # TODO: implement this test
        logging.info("Testing PINGREQ and PINGRESP control packets")

        self.mcc.connectClient()
        sleep(2)

        self.mcc.pingBroker()  # Genera PINGREQ y recibe PINGRESP
        sleep(2)

        self.mcc.disconnectClient()
        sleep(2)

    def testPubSub(self):
        # TODO: implement this test
        #
        # IMPORTANT: be sure to use QoS 1 and 2 to see ALL control packets
        logging.info("Testing SUBSCRIBE, PUBLISH, and QoS 1 & 2 packets")

        for qos in [1, 2]:
            self.mcc.connectClient()
            sleep(2)

            self.mcc.subscribeToTopic(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, qos=qos)
            sleep(2)

            self.mcc.publishMessage(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, msg="TEST: This is the CDA message payload.", qos=qos)
            sleep(2)

            self.mcc.unsubscribeFromTopic(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE)
            sleep(2)

            self.mcc.disconnectClient()
            sleep(2)

if __name__ == "__main__":
	unittest.main()