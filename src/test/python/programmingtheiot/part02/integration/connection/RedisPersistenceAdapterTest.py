import logging
import unittest

from programmingtheiot.cda.connection.RedisPersistenceAdapter import RedisPersistenceAdapter
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

class RedisPersistenceAdapterTest(unittest.TestCase):
	
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing RedisPersistenceAdapter class...")
        self.redis = RedisPersistenceAdapter()
        
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConnectClient(self):
        self.redis.connectClient()
        self.assertTrue(self.redis.is_connected)
        
        self.redis.disconnectClient()
        self.assertFalse(self.redis.is_connected)

    def testStoreData(self):
        self.redis.connectClient()
        self.assertTrue(self.redis.is_connected)
        
        data = SensorData()
        data.setValue(1.0)
        
        resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE
        self.assertTrue(self.redis.storeData(resource = resource, data = data))
        
        self.redis.disconnectClient()
        self.assertFalse(self.redis.is_connected)

if __name__ == "__main__":
    unittest.main()
