import stomp  
import threading  
from concurrent.futures import ThreadPoolExecutor  
from queue import Queue  
import logging  
from config import setting
import apis.aep_device_command
import json
from utils.log import httplogger

class NbiotListener(stomp.ConnectionListener):
    def on_message(self, frame):
        data={
  "content": {
    "params": {
      "data_download": frame.body
    },
    "serviceIdentifier": "8001"
  },
  "deviceId": setting.deviceId,
  "operator": "deng",
  "productId": 17045165,
  "ttl": 7200,
  "level": 1
}

        httplogger.info('NbiotListener senddata="{}"'.format(data))
        result = apis.aep_device_command.CreateCommand(setting.appKey,setting.appSecret, 
            setting.MasterKey_NB,  json.dumps(data))    
        httplogger.info('result='+str(result))
 
    def on_error(self, frame):
        print('NbiotListener Received an error "{}"'.format(frame.body))

class MqttListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print('MqttListener Received a message: "{}"'.format(frame.body))
 
    def on_error(self, frame):
        print('MqttListener Received an error "{}"'.format(frame.body))

class TcpListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print('TcpListener Received a message: "{}"'.format(frame.body))
 
    def on_error(self, frame):
        print('TcpListener Received an error "{}"'.format(frame.body))

class ActiveMQClient:  
    def __init__(self, ip, port, username='guest', password='guest'):  
        self.ip = ip  
        self.port = port
        self.username = username  
        self.password = password  
        self.nbiotconn = None 
        self.mqttconn = None
        self.tcpconn = None
        self.thread_pool = ThreadPoolExecutor(max_workers=10)  # 假设最大并发数为10  
        self.queue = Queue()  # 用于线程间通信，比如存储接收到的消息  
        self.nbiotsndqueue = Queue()  # 用于线程间通信，比如存储接收到的消息  
        self.mqttsndqueue = Queue()  # 用于线程间通信，比如存储接收到的消息  
        self.tcpsndqueue = Queue()  # 用于线程间通信，比如存储接收到的消息  
        self.error_queue = Queue()  # 用于存储错误信息  
        self.my_thread = threading.Thread(target=self.send_nbiot_messages,daemon=True)
        # 启动线程
        self.my_thread.start()

        self.my_thread = threading.Thread(target=self.send_mqtt_messages,daemon=True)
        # 启动线程
        self.my_thread.start()

        self.my_thread = threading.Thread(target=self.send_tcp_messages,daemon=True)
        # 启动线程
        self.my_thread.start()
  
    def connect1(self, conn, classname):  
        if conn is None or not conn.is_connected():  
            
            print("ip=", self.ip, " port=", self.port)
            conn = stomp.Connection([(self.ip, self.port)])
            
            tmplisten = classname()
            conn.set_listener('', tmplisten) 
            conn.connect(wait=True)  
        return conn
    def disconnect(self):  
        if self.nbiotconn and self.nbiotconn.is_connected():  
            self.nbiotconn.disconnect()  
  
    def _on_disconnected(self):  
        # 处理断开连接的情况，比如重新连接等  
        logging.error('Disconnected from ActiveMQ')  
  
    def subscribenbiot(self, destination, id=None, ack='auto'):  
        print("subscribenbiot:1")
        self.nbiotconn = self.connect1(self.nbiotconn, NbiotListener)  
        self.nbiotconn.subscribe(destination=destination, id=id, ack=ack)  
  
    def subscribemqtt(self, destination, id=None, ack='auto'):  
        print("subscribemqtt:1")
        self.mqttconn = self.connect1(self.mqttconn, MqttListener)  
        self.mqttconn.subscribe(destination=destination, id=id, ack=ack) 

    def subscribetcp(self, destination, id=None, ack='auto'):  
        print("subscribetcp:1")
        self.tcpconn = self.connect1(self.tcpconn, TcpListener)  
        self.tcpconn.subscribe(destination=destination, id=id, ack=ack) 

    def send_nbiot_messages(self):  
        # 使用一个单独的线程从队列中取出消息并处理  
        while True:  
            try:  
                message = self.nbiotsndqueue.get()  
                # 处理接收到的消息  
                httplogger.info(f"send_nbiot_messages message: {message}")  
                self.nbiotconn.send(body=json.dumps(message), destination=setting.activemqsendnbiotqueueid)
               
            except Exception as e:  
                httplogger.error(f"Error processing message: {e}") 

    def send_mqtt_messages(self):  
        # 使用一个单独的线程从队列中取出消息并处理  
        while True:  
            try:  
                message = self.mqttsndqueue.get()  
                # 处理接收到的消息  
                print(f"send_mqtt_messages message: {message}")  
                self.mqttconn.send(body=json.dumps(message), destination=setting.activemqsendmqttqueueid)
               
            except Exception as e:  
                logging.error(f"Error processing message: {e}") 

    def send_tcp_messages(self):  
        # 使用一个单独的线程从队列中取出消息并处理  
        while True:  
            try:  
                message = self.tcpsndqueue.get()  
                # 处理接收到的消息  
                print(f"send_tcp_messages message: {message}")  
                self.tcpconn.send(body=json.dumps(message), destination=setting.activemqsendtcpqueueid)
               
            except Exception as e:  
                logging.error(f"Error processing message: {e}") 

    def send_to_nbiot_queue(self, msg):
        print('---------消息发送--------------')
        self.nbiotconn = self.connect1(self.nbiotconn, NbiotListener)
        self.nbiotsndqueue.put(msg)

    def send_to_mqtt_queue(self, msg):
        print('---------消息发送--------------')
        self.mqttconn = self.connect1(self.mqttconn, MqttListener)
        self.mqttsndqueue.put(msg)

    def send_to_tcp_queue(self, msg):
        print('---------消息发送--------------')
        self.tcpconn = self.connect1(self.tcpconn, TcpListener)
        self.tcpsndqueue.put(msg)

activemq_client = ActiveMQClient(setting.activemqip, setting.activemqport, 
    setting.activemquser, setting.activemqpasswd)  
print("activemqip=", setting.activemqip, " activemqport=", setting.activemqport)
  