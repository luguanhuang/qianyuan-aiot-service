import random
import time
import json

from paho.mqtt import client as mqtt_client


broker = '127.0.0.1'
port = 1883
topic = "/python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    # client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

imei = "863659040514563"
def publish(client):
    msg_count = 0

    login_mqtt = {
    "command": "login_mqtt",
    "ClientId":"862167054996545",
    "password":"b7e8e300ba5949c4a5f6d1c962c92071",
    "imei":imei
    }

    authorize_mqtt = {
    "command": "authorize_mqtt",
    "imei": imei,
    "terminal_name": "液化气流量仪",
    "terminal_type": "gasflow",
    "utc": 1627897703,
    "utc_off": 1627897703,
    "lon": "126.041924",
    "lat": "42.957870",
    "local": "江苏无锡"
}

    dataupload_mqtt = {
    "command": "dataupload_mqtt",
    "imei": imei,
    "token_num":"12345678",
    "utc":1627897703,
    "data_mqtt": {
        "projectcode": "igc",
        "functioncode": "igasvcz",
        "data_type":"power",
        "no_data":"8636590405145631627897703",
        "voltage":"3.0",
        "battery_level":"100"
    }
}


    while True:
        
        msg = f"messages: {msg_count}"
        
        result = client.publish(topic, json.dumps(login_mqtt))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{login_mqtt}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

        time.sleep(2000)
        for i in range(1):
            result = client.publish(topic, json.dumps(authorize_mqtt))
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{authorize_mqtt}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")

        msg_count += 1
        time.sleep(1000)

def senddownres(client):
    data_mqttdownload_resp = {
        "command": "data_mqttdownload_resp",
        "imei": "863659040514563",
        "data_download_resp": {
            "no_data":"8636590405145631627897703"
        }
    }
   
    result = client.publish(topic, json.dumps(data_mqttdownload_resp))
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{data_mqttdownload_resp}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        data = json.loads(msg.payload.decode())
        command = data['command']
        if "data_mqttdownload_863659040514563" == command:
            senddownres(client)
        # dataupload_mqtt_863659040514563
    mqtttopic = "data_mqttdownload_"+imei
    client.subscribe(mqtttopic)
    client.on_message = on_message

def run():
    # client = connect_mqtt()
    # subscribe(client)
    # client.loop_forever()
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    publish(client)


# client_id = f'python-mqtt-{random.randint(0, 100)}'




# def run1():
#     client = connect_mqtt()
#     subscribe(client)
#     client.loop_forever()

if __name__ == '__main__':
    run()
