import redis as rd
import logging

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil

from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.DataUtil import DataUtil

logging.basicConfig(format = '%(asctime)s:%(name)s:%(levelname)s:%(message)s', level = logging.DEBUG)

class RedisPersistenceAdapter():
    """
    Adapter class for Redis persistence.
    """

    def __init__(self):
        """
        Constructor.

        @param host The host name or IP address of the Redis server.
        @param port The port number of the Redis server.
        @param enableCrypt True if SSL/TLS encryption should be used; False otherwise.
        """
        self.host = ConfigUtil().getProperty(ConfigConst.DATA_GATEWAY_SERVICE, ConfigConst.HOST_KEY)
        self.port = ConfigUtil().getInteger(ConfigConst.DATA_GATEWAY_SERVICE, ConfigConst.PORT_KEY)
        self.enableCrypt = ConfigUtil().getBoolean(ConfigConst.DATA_GATEWAY_SERVICE, ConfigConst.ENABLE_CRYPT_KEY)

        self.client = None
        self.is_connected = False
        self.dataUtil = DataUtil()

    def connectClient(self) -> bool:
        """
        Connects to the Redis server using configuration parameters
        specified by the sub-class.
        
        @return bool True on success; False otherwise.
        """
        #check if the connection is already established
        if self.is_connected:
            if self.client.ping():
                logging.info("Redis client is already connected.")
                return self.is_connected
            else:
                logging.info("Redis client is not connected. Reconnecting...")
                self.disconnectClient()
        try:
            self.client = rd.Redis(host=self.host, port=self.port, ssl=self.enableCrypt)
            self.client.ping()
            self.is_connected = True
            logging.info(f"Connected to Redis server: {self.host}:{self.port}")
            return True
        except Exception as e:
            logging.error("Failed to connect to Redis server. Exception: " + str(e))
            return False

    def disconnectClient(self) -> bool:
        """
        Disconnects from the Redis server if the client is already connected.
        If not, this call is ignored, but will return a True.
        
        @return bool True on success; False otherwise.
        """
        if self.is_connected:
            try:
                self.client.close()
                self.is_connected = False
                logging.info("Disconnected from Redis server.")
                return True
            except Exception as e:
                logging.error("Failed to disconnect from Redis server. Exception: " + str(e))
                return False
        else:
            logging.info("Redis client is not connected. Ignoring disconnect request.")
            return True
        
    def storeData(self, resource: ResourceNameEnum, data:SensorData) -> bool:
        if self.is_connected:
            try:
                jsonData = self.dataUtil.sensorDataToJson(data)
                self.client.publish(resource.value, jsonData)
                logging.info(f"Stored data from {data.getName()} : {jsonData} in Redis topic: {resource.value}")
                return True
            except Exception as e:
                logging.error("Failed to store data in Redis. Exception: " + str(e))
                return False
        else:
            logging.info("Redis client is not connected. Ignoring store request.")
            return False
        
    def getData(self, resource: ResourceNameEnum) -> SensorData:
        """
        Retrieves the data from the Redis server.
        (An extra function to test redis)
        
        @param resource The resource name to retrieve.
        @return SensorData
        """
        if self.is_connected:
            try:
                jsonData = self.client.get(resource.value)
                jsonData = jsonData.decode('utf-8')
                logging.info(f"Retrieved data from {resource.value} : {jsonData} from Redis")
                sd = self.dataUtil.jsonToSensorData(jsonData)
                return sd
            except Exception as e:
                logging.error("Failed to retrieve data from Redis. Exception: " + str(e))
                return None
        else:
            logging.info("Redis client is not connected. Ignoring get request.")
            return None


if __name__ == "__main__":
    redis = RedisPersistenceAdapter()
    redis.connectClient()
    redis.storeData(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, SensorData("test", ConfigConst.TEMP_SENSOR_TYPE, 0))
    data = redis.getData(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE)
    print("----------------prueba---------------")
    print(data)
    redis.disconnectClient()
        