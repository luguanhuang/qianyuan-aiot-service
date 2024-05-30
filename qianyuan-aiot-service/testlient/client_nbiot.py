import requests

# data = {
#     "data": [
#         {
#             "dep_id": "T01",
#             "dep_name": "Test学院",
#             "master_name": "Test-Master",
#             "slogan": "Here is Slogan"
#         }
#     ]
# }

data = {
    "timestamp": 1716543996891,
    "tenantId": "10418623",
    "serviceId": 1001,
    "protocol": "lwm2m",
    "productId": "17045165",
    "messageType": "eventReport",
    "eventType": 1,
    "eventContent": {
        "utc": 1716543925000,
        "projectcode": "1000",
        "functioncode": "01",
        "event_nb": "1",
        "IMEI": "171643393155758"
    },
    "deviceSn": "",
    "deviceId": "7a09a66603b746f6a62a9f23e34be191",
    "IMSI": "undefined",
    "IMEI": "171643393155758"
}

# response = requests.post("http://127.0.0.1:5680/nbdata", json={'timestamp': 1716791341817, 'tenantId': '10418623', 'protocol': 'lwm2m', 'productId': '17045165', 'messageType': 'deviceOnlineOfflineReport', 'ipv4Address': '11.149.43.246', 'iccid': 'undefined', 'eventType': 1, 'deviceId': '2c330d43c8524a7bb3dfa84cc427146c', 'imei': '869768041574395', 'accessFlag': 0})
response = requests.post("http://127.0.0.1:5680/nbdata", json=data)
# response = requests.post("http://127.0.0.1:5680/nbdata", json={'upPacketSN': -1, 'upDataSN': -1, 'topic': 'v1/up/ad19', 'timestamp': 1716368806786, 'tenantId': '10418623', 'serviceId': 101, 'protocol': 'lwm2m', 'productId': '17045165', 'payload': {'utc': 0, 'projectcode': '1000', 'functioncode': '01', 'data_nb': 'f:0.000000;0.000000;5.0;13.1;0;0;3.56;1714784742', 'IMEI': '869768041574395'}, 'messageType': 'dataReport', 'deviceType': '', 'deviceId': '2c330d43c8524a7bb3dfa84cc427146c', 'assocAssetId': '', 'IMSI': 'undefined', 'IMEI': '869768041574395'})

# response = requests.post("http://127.0.0.1:5680/nbdata", json={'upPacketSN': -1, 'upDataSN': -1, 'topic': 'v1/up/ad19', 'timestamp': 1716368806786, 'tenantId': '10418623', 'serviceId': 101, 'protocol': 'lwm2m', 'productId': '17045165', 'payload': {'utc': 0, 'projectcode': '1000', 'functioncode': '01', 'data_nb': 'f:0.000000;0.000000;5.0;13.1;0;0;3.56;1714784742', 'IMEI': '869768041574395'}, 'messageType': 'dataReport', 'deviceType': '', 'deviceId': '2c330d43c8524a7bb3dfa84cc427146c', 'assocAssetId': '', 'IMSI': 'undefined', 'IMEI': '869768041574395'})
# response = requests.post("http://127.0.0.1:5680/mqttdata", json=data)
# response = requests.post("http://127.0.0.1:5680/tcpdata", json=data)
content = response.content
print("content1111111=", content);


# import socket
 
# # 创建一个TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# # 连接服务器
# server_address = ('localhost', 8990)  # 服务器地址和端口
# sock.connect(server_address)
 
# # 发送数据
# message = b'Hello, World!'  # 使用bytes对象发送消息
# sock.sendall(message)
 
# # # 接收服务器响应（如果有的话）
# # response = sock.recv(1024)
 
# # print('Received:', response)
 
# # 关闭连接
# sock.close()