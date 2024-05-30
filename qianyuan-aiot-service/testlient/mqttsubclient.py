import random
import json
from paho.mqtt import client as mqtt_client

broker = '127.0.0.1'
# broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt"
topic = "data_mqttdownload_863659040514563"

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

allconninfo = {}


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # client = mqtt_client.Client(client_id)
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    data_mqttdownload_resp = {
    "command": "data_mqttdownload_resp",
    "data_download_resp": {
        "imei": "863659040514563",
        "no_data":"8636590405145631627897703",
        }
    }

    while True:
        result = client.publish(topic, json.dumps(data_mqttdownload_resp))
        status = result[0]
        if status == 0:
            print(f"Send `{data_mqttdownload_resp}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    
        time.sleep(1000)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        data = json.loads(msg.payload.decode())
        publish(client)
        
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()