#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import paho.mqtt.client as mqttClient

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient

class MqttClientConnector(IPubSubClient):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, clientID: str = None):
		"""
		Default constructor. This will set remote broker information and client connection
		information based on the default configuration file contents.
		
		@param clientID Defaults to None. Can be set by caller. If this is used, it's
		critically important that a unique, non-conflicting name be used so to avoid
		causing the MQTT broker to disconnect any client using the same name. With
		auto-reconnect enabled, this can cause a race condition where each client with
		the same clientID continuously attempts to re-connect, causing the broker to
		disconnect the previous instance.
		"""
		self.config = ConfigUtil()
		self.dataMsgListener = None
		self.host = self.config.getProperty(
			ConfigConst.MQTT_GATEWAY_SERVICE, 
			ConfigConst.HOST_KEY,
			ConfigConst.DEFAULT_HOST
		)
		self.port =self.config.getInteger(
			ConfigConst.MQTT_GATEWAY_SERVICE, 
			ConfigConst.PORT_KEY, 
			ConfigConst.DEFAULT_MQTT_PORT)
		
		self.keepAlive = self.config.getInteger(
			ConfigConst.MQTT_GATEWAY_SERVICE, 
			ConfigConst.KEEP_ALIVE_KEY, 
			ConfigConst.DEFAULT_KEEP_ALIVE
			)
		
		self.defaultQoS = self.config.getInteger(
			ConfigConst.MQTT_GATEWAY_SERVICE, 
			ConfigConst.DEFAULT_QOS_KEY, 
			ConfigConst.DEFAULT_QOS
		)

		self.mqttClient = None

		if clientID is None:
			self.clientID = self.config.getProperty(
				ConfigConst.CONSTRAINED_DEVICE, 
				ConfigConst.DEVICE_LOCATION_ID_KEY
			)
		else:
			self.clientID = clientID
		
		logging.info('\tMQTT Client ID:   ' + self.clientID)
		logging.info('\tMQTT Broker Host: ' + self.host)
		logging.info('\tMQTT Broker Port: ' + str(self.port))
		logging.info('\tMQTT Keep Alive:  ' + str(self.keepAlive))

	def connectClient(self, cleanSession: bool = True) -> bool:
		if not self.mqttClient:
			self.mqttClient = mqttClient.Client(
				client_id = self.clientID, clean_session = cleanSession)

			self.mqttClient.on_connect = self.onConnect
			self.mqttClient.on_disconnect = self.onDisconnect
			self.mqttClient.on_message = self.onMessage
			self.mqttClient.on_publish = self.onPublish
			self.mqttClient.on_subscribe = self.onSubscribe

		if not self.mqttClient.is_connected():
			logging.info('MQTT client connecting to broker at host: ' + self.host)
			self.mqttClient.connect(self.host, self.port, self.keepAlive)
			self.mqttClient.loop_start()

			return True
		else:
			logging.warning('MQTT client is already connected. Ignoring connect request.')

			return False
		
	def disconnectClient(self) -> bool:
		if self.mqsttClient.is_connected():
			logging.info('Disconnecting MQTT client from broker: ' + self.host)
			self.mqttClient.loop_stop()
			self.mqttClient.disconnect()

			return True
		else:
			logging.warning('MQTT client already disconnected. Ignoring.')

			return False
		
	def onConnect(self, client, userdata, flags, rc):
		pass
		
	def onDisconnect(self, client, userdata, rc):
		pass
		
	def onMessage(self, client, userdata, msg):
		pass
			
	def onPublish(self, client, userdata, mid):
		pass
	
	def onSubscribe(self, client, userdata, mid, granted_qos):
		pass
	
	def onActuatorCommandMessage(self, client, userdata, msg):
		"""
		This callback is defined as a convenience, but does not
		need to be used and can be ignored.
		
		It's simply an example for how you can create your own
		custom callback for incoming messages from a specific
		topic subscription (such as for actuator commands).
		
		@param client The client reference context.
		@param userdata The user reference context.
		@param msg The message context, including the embedded payload.
		"""
		pass
	
	def publishMessage(self, resource: ResourceNameEnum = None, msg: str = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
		logging.info('Publishing message to topic: ' + str(resource))
		return False
	
	def subscribeToTopic(self, resource: ResourceNameEnum = None, callback = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
		logging.info('Subscribing to topic: ' + str(resource))
		return False
	
	def unsubscribeFromTopic(self, resource: ResourceNameEnum = None):
		logging.info("Unsuscribing from topic: " + str(resource))
		return False

	def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
		if listener:
			self.dataMessageListener = listener
			return True
		else:
			return False
