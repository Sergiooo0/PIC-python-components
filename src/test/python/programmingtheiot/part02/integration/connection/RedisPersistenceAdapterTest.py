import logging
import unittest

from programmingtheiot.cda.connection.RedisPersistenceAdapter import RedisPersistenceAdapter
from programmingtheiot.data.SensorData import SensorData
import programmingtheiot.common.ConfigConst as ConfigConst


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

    def test_01_ConnectClient(self):
        self.redis.connectClient()
        self.assertTrue(self.redis.is_connected)
        
        self.redis.disconnectClient()
        self.assertFalse(self.redis.is_connected)

    def test_02_StoreData(self):
        self.redis.connectClient()
        self.assertTrue(self.redis.is_connected)
        
        data = SensorData()
        data.setValue(1.0)
        
        resource = ConfigConst.TEMP_SENSOR_NAME
        self.assertTrue(self.redis.storeData(resource = resource, data = data))
        
        self.redis.disconnectClient()
        self.assertFalse(self.redis.is_connected)

    def test_03_GetData(self):
        self.redis.connectClient()
        self.assertTrue(self.redis.is_connected)
        
        resource = ConfigConst.TEMP_SENSOR_NAME
        data = self.redis.getData(resource)
        
        self.assertIsNotNone(data)
        self.assertEqual(data.getValue(), 1.0)
        
        self.redis.disconnectClient()
        self.assertFalse(self.redis.is_connected)

if __name__ == "__main__":
    unittest.main()
