import socket
import select
from config import setting
from utils.log import logger
import threading
import time
import stomp
import json
import random
from queue import Queue
from utils.active_mq import activemq_client
from paho.mqtt import client as mqtt_client
import binascii
# from utils import log
from utils.log import tcpserver
resndLock = threading.Lock()

client_id = f'python-mqtt-{random.randint(0, 10000)}'
devqueue = Queue()  # 用于线程间通信，比如存储接收到的消息  

def publish(client, topic, resdata):
    result = client.publish(topic, json.dumps(resdata))
    tcpserver.info(f"topic={topic}")
    status = result[0]
    if status == 0:
        tcpserver.info(f"Send `{resdata}` to topic `{topic}`")
    else:
        tcpserver.error(f"Failed to send message to topic {topic}")

class MyListener(stomp.ConnectionListener):
    def __init__(self, client):
        self.client = client
        
    def pad_with_zero(self, number):
        return str(number).zfill(4)

    def on_message(self, frame):
        tcpserver.info(f'Received a mqtt message: {frame.body}')
        data = json.loads(frame.body)
        deviceid = data['deviceid']
        address = data['address']
        sequence = data['sequence']
        datainfo = data['data']
        encodedatainfo = binascii.hexlify(datainfo.encode())
        datalen = int(len(encodedatainfo)/2);
        hex_datalen = hex(datalen)[2:]  # [2:]去除前缀'0x'

        tcpserver.info(f"deviceid={deviceid}, address={address}, sequence={sequence}, datainfo={datainfo}")
        tcpserver.info(f"deviceid={binascii.hexlify(deviceid.encode())}, address={binascii.hexlify(address.encode())}, datainfo={encodedatainfo}")
        resdata = "03"
        
        servicedata = "40400001"+binascii.hexlify(address.encode()).decode()+ \
            sequence.zfill(2) + self.pad_with_zero(hex_datalen) + \
            binascii.hexlify(datainfo.encode()).decode()+"232323"
        hex_datalen = hex(int(len(servicedata)/2))[2:]  # [2:]去除前缀'0x'
        
        totallen = self.pad_with_zero(hex_datalen)
        
        resdata = resdata + totallen + servicedata 
        tcpserver.info(f"resdata={resdata} totallen={totallen} len={len(servicedata)}")
        senddata = {
            "resdata":resdata,
            "deviceid":deviceid
        }
        devqueue.put(json.dumps(senddata));

class tcp_server:
    def __init__(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(('0.0.0.0', setting.tcpport))
        self.serversocket.listen(setting.listen_queue)
        self.serversocket.setblocking(0)
        self.queueLock = threading.Lock()
        self.connections = {}
        self.arrresndpacket = {}
        self.epoll = select.epoll()
        self.sndqueue = Queue()  # 用于线程间通信，比如存储接收到的消息  
        self.epoll.register(self.serversocket.fileno(), select.EPOLLIN)
        self.activemqconn = stomp.Connection([(setting.activemqip, setting.activemqport)])
        self.clientinf = self.connect_mqtt()
        self.subscribe(self.clientinf)
        self.activemqconn.set_listener('', MyListener(self.clientinf))
        self.activemqconn.connect(wait=True)
        self.activemqconn.subscribe(destination=setting.activemqrecvtcpqueueid, id=50, ack='auto')
        my_thread = threading.Thread(target=self.send_messagesto_activemq, args=(self.activemqconn, ),daemon=True)
        my_thread.start()
        my_thread = threading.Thread(target=self.send_messagesto_dev, daemon=True)
        my_thread.start()

        my_thread = threading.Thread(target=self.resnddownthd, daemon=True)
        my_thread.start()

        my_thread = threading.Thread(target=self.connection_timeout_thd, daemon=True)
        my_thread.start()

    def send_messagesto_dev(self):  
        # 使用一个单独的线程从队列中取出消息并处理  
        global devqueue
        while True:  
            try:  
                msg = devqueue.get()  
                # 处理接收到的消息  
                data = json.loads(msg)
                tcpserver.info(f"send_messagesto_activemq message: deviceid={data['deviceid']}, resdata={data['resdata']}")
                self.queueLock.acquire()
                for key in self.connections:
                    if self.connections[key]['deviceId'] == data['deviceid']:
                        self.connections[key]["connection"].send(data['resdata'].encode())
                        tcpserver.info(f"i find 1={data['deviceid']} 2={self.connections[key]['deviceId']}")
                        packetinfo = {
                            "deviceid":data['deviceid'],
                            "resdata":data['resdata'],
                            "resndcnt":0
                        }

                        resndLock.acquire()
                        self.arrresndpacket[key] = packetinfo
                        resndLock.release()
                        break
                self.queueLock.release()
                
            except Exception as e:  
                logging.error(f"Error processing message: {e}") 

    def send_messagesto_activemq(self, activemqconn):  
        # 使用一个单独的线程从队列中取出消息并处理  
        while True:  
            try:  
                msg = self.sndqueue.get()  
                # 处理接收到的消息  
                tcpserver.info(f"send_messagesto_activemq message: {msg}")  
                self.activemqconn.send(body=json.dumps(msg), destination=setting.activemqsendtcpqueueid)
                
            except Exception as e:  
                tcpserver.error(f"Error processing message: {e}") 

    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            tcpserver.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            data = json.loads(msg.payload.decode())
            command = data['command']
            imei = data['imei']
            mqtttopic = setting.mqttclitopic+imei
            if command == 'login_mqtt':
                procloginmsg(data, mqtttopic, client)
            
            elif command == 'authorize_mqtt':
                procauthorizemsg(data, mqtttopic, client)
            elif command == 'dataupload_mqtt':
                procdatauploadmsg(data, mqtttopic, client)
            elif command == 'data_mqttdownload_resp':
                procdownloadresp(data, mqtttopic, client)
        client.subscribe(setting.mqtttopic)
        client.on_message = on_message

    def ReleaseSockUnlock(self, fd):
        try:           
            if fd in self.connections:    
                self.epoll.unregister(fd)
                self.connections[fd]["connection"].close()
                del self.connections[fd]

        except Exception as e:
            i=1

    def ReleaseSock(self, fd):
        try:
            self.queueLock.acquire()
            if fd in self.connections:
                
                self.epoll.unregister(fd)
                self.connections[fd]["connection"].close()
                del self.connections[fd]
            self.queueLock.release()
        except Exception as e:
            self.queueLock.release()

    # 定义线程将要执行的函数
    def connection_timeout_thd(self):
        while True:
            self.queueLock.acquire()
            keys_to_remove = []
            current_timestamp = time.time()
            seconds_since_1970 = int(current_timestamp)
            for key in self.connections:
                timediff = seconds_since_1970 - self.connections[key]['time']
                if timediff >= setting.connection_timeout_time:
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                self.ReleaseSockUnlock(key);
                # print("will dele fd=", key)
                # del self.connections[key]
            self.queueLock.release()
            time.sleep(5)

    def procuploadmsg(self, message, fd, client_socket):
        # 解析消息类型
        tcpserver.info("proc procuploadmsg msg")
         # 解析数据长度和数据
        data_length = int(message[2:6], 16)*2
        tcpserver.info(f"data_length={data_length}")
        data = message[6:6 + data_length]   
        tcpserver.info(f"data={data}")
        tcpserver.info(message[10:14])
        command = message[10:14]
        tcpserver.info(f"command={command}")
        address = message[14:22]
        tcpserver.info(f"command={command} address={address}")
        # # 解析数据序号
        data_sequence = message[22:24]
        
        data_field_length = int(message[24:28], 16)*2
        tcpserver.info(data_field_length)
        data_field = message[28:28+data_field_length]
        
        # 解析帧尾
        frame_tail = message[-6:]
        tcpserver.info(f"{command}, {address}, {data_field}")
        tcpserver.info(f"command={command} address={address} data_sequence={data_sequence} data_field={data_field} frame_tail={frame_tail}")

        self.queueLock.acquire()
        if fd in self.connections:
            current_timestamp = time.time()
            seconds_since_1970 = int(current_timestamp)
            self.connections[fd]["time"] = seconds_since_1970
        self.queueLock.release()

        if fd in self.connections and self.connections[fd]["deviceId"] != "":
            data_mqtt = {
                "command": "dataupload",
                "deviceid": self.connections[fd]["deviceId"],
                "password": self.connections[fd]["password"],
                "version": self.connections[fd]["version"],
                "databack_mqtt": {
                    "errcode":"0000",
                    "message":"success",
                    "address":binascii.unhexlify(address).decode(),
                    "data":binascii.unhexlify(data_field).decode()
                }
            }

            self.sndqueue.put(data_mqtt)
            resdata = '050000'
            client_socket.send(resdata.encode())
        else:
            resdata = '050005'
            client_socket.send(resdata.encode())
        

    def procheartbeatmsg(self, fd):
        # 解析消息类型
        tcpserver.info("procheartbeatmsg msg")
        current_timestamp = time.time()
        seconds_since_1970 = int(current_timestamp)
        self.queueLock.acquire()
        if fd in self.connections:
            ret = self.connections[fd]["connection"].send(b'06')
            self.connections[fd]["time"] = seconds_since_1970
        
        self.queueLock.release()
        

    def procloginmsg(self, message, fd, client_socket):
        # 解析消息类型
        # 解析设备ID长度和设备ID
        device_id_length = int(message[2:6], 16) * 2
        device_id = message[6:6+device_id_length]
        tcpserver.info(f"device_id={device_id}")
        # 解析密码长度和密码
        password_length_index = 6 + device_id_length
        password_length = int(message[password_length_index:password_length_index+4], 16)*2
        password_index = password_length_index + 4
        password = message[password_index:password_index+password_length]
        tcpserver.info("password={password}")
        # 解析版本信息长度和版本信息
        version_length_index = password_index + password_length
        version_length = int(message[version_length_index:version_length_index+4], 16)*2
        version_index = version_length_index + 4
        version = message[version_index:version_index+version_length]
        self.queueLock.acquire()
        if fd in self.connections:
            self.connections[fd]["deviceId"] = binascii.unhexlify(device_id).decode()
            self.connections[fd]["password"] = binascii.unhexlify(password).decode()
            self.connections[fd]["version"] = binascii.unhexlify(version).decode()
            current_timestamp = time.time()
            seconds_since_1970 = int(current_timestamp)
            self.connections[fd]["time"] = seconds_since_1970
        self.queueLock.release()

        tcpserver.info(f"version={version} deviceid={device_id}")
        resdata = '050000'
        client_socket.send(resdata.encode())

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                tcpserver.info(f"Connected to MQTT Broker!")
            else:
                tcpserver.info(f"Failed to connect, return code {rc}\n")

        client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
        client.on_connect = on_connect

        client.connect(setting.mqttbroker, setting.mqttport)
        return client

    def tcpdownloadresp(self, recvdata, fd):
        resndLock.acquire()
        tcpserver.info("tcpdownloadresp: begin")
        if fd in self.arrresndpacket:
            tcpserver.info("tcpdownloadresp: begin 1")
            del self.arrresndpacket[fd] 
        resndLock.release()

    def resnddownthd(self):
        while True:
            keys_to_remove = []
            for key in self.arrresndpacket:
                print(f"cnt={self.arrresndpacket[key]['resndcnt']}")
                if self.arrresndpacket[key]['resndcnt'] <= setting.max_resnd_cnd:
                    if self.arrresndpacket[key]['resndcnt'] > 0:
                        self.connections[key]["connection"].send(self.arrresndpacket[key]['resdata'].encode())
                    self.arrresndpacket[key]['resndcnt']=self.arrresndpacket[key]['resndcnt']+1
                    
                if self.arrresndpacket[key]['resndcnt'] > setting.max_resnd_cnd:
                    keys_to_remove.append(key)
            resndLock.acquire()
            for key in keys_to_remove:
                if key in self.arrresndpacket:
                    del self.arrresndpacket[key]
            resndLock.release()
            time.sleep(3)

    def handle_client(self, fd):
        # 接收客户端发送的信息
        try:
            if fd in self.connections:
                client_socket = self.connections[fd]["connection"]
                recvdata = client_socket.recv(1024).decode()
                print(f"recvdata={recvdata} len={len(recvdata)}")
                tmplen = len(recvdata)
                if tmplen <= 0:
                    self.ReleaseSock(fd)
                else:
                    # 为每个客户端创建一个新线程
                    message_type = recvdata[0:2]
                    tcpserver.info(f"message_type={message_type}")
                    if message_type == '01':
                        self.procloginmsg(recvdata, fd, client_socket)
                    elif message_type == '02':
                        self.procuploadmsg(recvdata, fd, client_socket)
                    elif message_type == '04':
                        self.procheartbeatmsg(fd)
                    elif message_type == '07':
                        self.tcpdownloadresp(recvdata, fd)
        except Exception as e:
            self.ReleaseSock(fd)

    def run(self):
        response = "接收成功，返回数据: connecting status: 200 \n"
        response += "haody,client !"
        
        try:
            requests = {}
            responses = {}

            while True:
                events = self.epoll.poll(1)
                for fid, event in events:
                    if fid == self.serversocket.fileno():
                        tcpserver.info(f"fid111={fid}")
                        connection, address = self.serversocket.accept()
                        self.epoll.register(connection.fileno(), select.EPOLLIN)
                        self.queueLock.acquire()
                        current_timestamp = time.time()
                        seconds_since_1970 = int(current_timestamp)
                        conninfo = {
                            "connection":connection,
                            "time":seconds_since_1970,
                            "deviceId":"",
                            "password":"",
                            "version":""
                        }

                        self.connections[connection.fileno()] = conninfo
                        self.queueLock.release()

                    elif event & select.EPOLLIN:
                        client_thread = threading.Thread(target=self.handle_client, args=(fid,))
                        client_thread.start()

        except:
            tcpserver.info("server excepted ...")
            self.epoll.unregister(self.serversocket.fileno())

        finally:
            tcpserver.info("server closed ...")