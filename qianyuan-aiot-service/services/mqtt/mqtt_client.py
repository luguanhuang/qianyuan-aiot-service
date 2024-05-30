"""
实现mqtt的业务逻辑
    初始化
    消息处理
    消息发布
"""
import random
import json
from paho.mqtt import client as mqtt_client
from config import setting 
import time
from dao.mqtt import devices
from utils.sql_helper import sql_helper
import stomp
import time
from utils.active_mq import activemq_client
from queue import Queue
import threading
import logging  
from utils.log import mqttserver


activemqconn = None

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
allconninfo = {}
clientinf = None
sndqueue = Queue()  # 用于线程间通信，比如存储接收到的消息  
queueLock = threading.Lock()
resndLock = threading.Lock()
arrresndpacket = {}

def publish(client, topic, resdata):
    result = client.publish(topic, json.dumps(resdata))
    mqttserver.info(f"topic={topic}")
    status = result[0]
    if status == 0:
        mqttserver.info(f"Send `{resdata}` to topic `{topic}`")
    else:
        mqttserver.error(f"Failed to send message to topic {topic}")

class MyListener(stomp.ConnectionListener):
    def __init__(self, client):
        self.client = client
        
    def on_message(self, frame):
        mqttserver.info(f"Received a mqtt message: {frame.body}")
        data = json.loads(frame.body)
        imei = data['imei']
        resdata = {
            "command": "data_mqttdownload_"+imei,
            "data_download": {
                "imei": imei,
                "no_data":"8636590405145631627897703",
                "data_mqtt": data['data_mqtt']
            }
        }

        if imei in allconninfo:
            mqttserver.info(f"imei={imei} res to dev")
            mqtttopic = setting.mqttclitopic+imei
            publish(self.client, mqtttopic, resdata)
            packetinfo = {
                            "mqtttopic":mqtttopic,
                            "client":self.client,
                            "resdata":resdata,
                            "resndcnt":0
                        }
            resndLock.acquire()
            arrresndpacket[imei] = packetinfo
            resndLock.release()
 
    def on_error(self, frame):
        mqttserver.error(f"Received an error: {frame.body}")

def send_to_queue(msg):
    global activemqconn
    mqttserver.info('---------消息发送--------------')
    # body=数据, destination=根据队列名传输数据,如果队列不存在,就创建一个
    activemqconn.send(body=json.dumps(msg), destination=setting.activemqsendmqttqueueid)
    mqttserver.info(msg)


def get_ip_address(url):
    try:
        ip_address = socket.gethostbyname(url)
        return ip_address
    except socket.gaierror:
        return None

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            mqttserver.info("Connected to MQTT Broker!")
        else:
            mqttserver.error(f"Failed to connect, return code {rc}\n")

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect

    client.connect(setting.mqttbroker, setting.mqttport)
    return client

def judgelogin(imei):
    current_timestamp = time.time()
    seconds_since_1970 = int(current_timestamp)
    if imei in allconninfo:
        timediff = seconds_since_1970 - allconninfo[imei]['conntime']
        if allconninfo[imei]['islock'] == 1:
            if timediff < setting.lock_time:
                return 2
            else:
                queueLock.acquire()
                allconninfo[imei]['islock'] = 0
                allconninfo[imei]['conncnt'] = 1
                allconninfo[imei]['conntime'] = seconds_since_1970
                queueLock.release()
                return 1
        else:
            allconninfo[imei]['conncnt'] = allconninfo[imei]['conncnt'] + 1
            conncnt = allconninfo[imei]['conncnt']
            mqttserver.info(f"cnt={conncnt}")
            if timediff < setting.sndpackertimediff and conncnt > setting.max_snd_cnt:
                queueLock.acquire()
                allconninfo[imei]['islock'] = 1
                queueLock.release()
                return 2
            else:
                queueLock.acquire()
                allconninfo[imei]['conntime'] = seconds_since_1970
                queueLock.release()
            return 1
    else:
        return 0

def procloginmsg(data, mqtttopic, client):
    ClientId = data['ClientId']
    password = data['password']
    imei = data['imei']
    resdata = devices.select_mqtt_aiot_by_id(ClientId, imei, password)
    errcode="9000"
    message = "login failure"
    token_num = ""
    expires_in = ""
    cnt = 0
    if resdata is not None and resdata != False:
        print("resdata=", resdata)
        cnt = len(resdata)
    if (cnt > 0):
        errcode="0000"
        message = "succeed"
        current_timestamp = time.time()
        seconds_since_1970 = int(current_timestamp)
        conninfo = {
            "conntime": seconds_since_1970,
            "conncnt": 1,
            "islock": 0
        }

        allconninfo[imei] = conninfo

    resdata = {
        "command": "login_mqtt_"+imei,
        "databack_mqtt": {
            "errcode":errcode,
            "message":message
        }
    }

    publish(client, mqtttopic, resdata)

def procauthorizemsg(data, mqtttopic, client):
    imei = data['imei']
    print("procauthorizemsg message imei=", imei)
    errcode="9000"
    message = "data not exist"
    ret = judgelogin(imei)
    if ret == 0:
        resdata = {
        "command": "authorize_mqtt_"+imei,
        "databack_mqtt": {
            "token_num":"",
            "expires_in":"",
            "projectcode": "igc",
            "functioncode": "igasvcz",
            "dwid": "igasv3202c01",
            "errcode":errcode,
            "message":"please login first"
            }
        }

        publish(client, mqtttopic, resdata)
        return
    elif ret == 2:
        mqttserver.info("too much packet, will lock u")
        return
    resdata = devices.select_mqtt_aiot_by_imei(imei)
    
    token_num = ""
    expires_in = ""
    cnt = 0
    if resdata is not None and resdata != False:
        cnt = len(resdata)
    if (cnt > 0):
        errcode="0000"
        message = "succeed"
        token_num = resdata['token_num']
        expires_in = resdata['expires_in']

    resdata = {
        "command": "authorize_mqtt_"+imei,
        "databack_mqtt": {
            "token_num":token_num,
            "expires_in":expires_in,
            "projectcode": "igc",
            "functioncode": "igasvcz",
            "dwid": "igasv3202c01",
            "errcode":errcode,
            "message":message

        }
    }

    publish(client, mqtttopic, resdata)

def procdatauploadmsg(data, mqtttopic, client):
    imei = data['imei']
    ret = judgelogin(imei)
    if ret == 0:
        resdata = {
            "command": "dataupload_mqtt_"+imei,
            "token_num":"12345678",
            "no_data":"8636590405145631627897703",
            "databack_mqtt": {
                "errcode":"9000",
                "message":"please login first"
            }
        }

        publish(client, mqtttopic, resdata)
        return
    elif ret == 2:
        mqttserver.info("dataupload_mqtt: too much packet, will lock u")
        return

    resdata = {
            "command": "dataupload_mqtt_"+imei,
            "token_num":"12345678",
            "no_data":"8636590405145631627897703",
            "databack_mqtt": {
                "errcode":"0000",
                "message":"success"
            }
        }

    data_mqtt = data['data_mqtt']
    publish(client, mqtttopic, resdata)
    sndqueue.put(data_mqtt)
    mqttserver.info(f"procdatauploadmsg message imei={imei}")

def procdownloadresp(data, mqtttopic, client):
    imei = data['imei']
    resndLock.acquire()
    if imei in arrresndpacket:
        del arrresndpacket[imei] 
    resndLock.release()
    i=1

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        mqttserver.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
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

def checklogintimeout():
    while True:
        keys_to_remove = []
        for key in allconninfo:
            current_timestamp = time.time()
            seconds_since_1970 = int(current_timestamp)
            
            if seconds_since_1970 - allconninfo[key]['conntime'] > setting.login_timeout_time:
                keys_to_remove.append(key)
        queueLock.acquire()
        for key in keys_to_remove:
            mqttserver.info(f"key timeout will delete it={key}")
            if key in allconninfo:
                del allconninfo[key]
        queueLock.release()

        time.sleep(5);

def send_messages(activemqconn):  
    # 使用一个单独的线程从队列中取出消息并处理  
    while True:  
        try:  
            msg = sndqueue.get()  
            # 处理接收到的消息  
            mqttserver.info(f"send_messages message: {msg}")
            print(f"send_messages message: {msg}")  
            activemqconn.send(body=json.dumps(msg), destination=setting.activemqsendmqttqueueid)
            
        except Exception as e:  
            mqttserver.error(f"Error processing message: {e}") 

def resnddownthd():
    while True:
        keys_to_remove = []
        for key in arrresndpacket:
            mqttserver.info(f"cnt={arrresndpacket[key]['resndcnt']}")
            if arrresndpacket[key]['resndcnt'] <= setting.max_resnd_cnd:
                if arrresndpacket[key]['resndcnt'] > 0:
                    publish(arrresndpacket[key]['client'], arrresndpacket[key]['mqtttopic'], 
                        arrresndpacket[key]['resdata'])
                arrresndpacket[key]['resndcnt']=arrresndpacket[key]['resndcnt']+1
                
            if arrresndpacket[key]['resndcnt'] > setting.max_resnd_cnd:
                keys_to_remove.append(key)
        resndLock.acquire()
        for key in keys_to_remove:
            if key in arrresndpacket:
                del arrresndpacket[key]
        resndLock.release()
        time.sleep(3)

def run():
    my_thread = threading.Thread(target=checklogintimeout,daemon=True)
    # 启动线程
    my_thread.start()

    my_thread = threading.Thread(target=resnddownthd,daemon=True)
    # 启动线程
    my_thread.start()

    activemqconn = stomp.Connection([(setting.activemqip, setting.activemqport)])
    clientinf = connect_mqtt()
    subscribe(clientinf)

    activemqconn.set_listener('', MyListener(clientinf))
    activemqconn.connect(wait=True)
    activemqconn.subscribe(destination=setting.activemqrecvmqttqueueid, id=2, ack='auto')

    my_thread = threading.Thread(target=send_messages, args=(activemqconn, ),daemon=True)
        # 启动线程
    my_thread.start()

    clientinf.loop_forever()


if __name__ == '__main__':
    run()


