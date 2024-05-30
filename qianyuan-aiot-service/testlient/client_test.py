import requests
from services.http.public import app as public_api
import apis.aep_device_command
import json

data = {
    "data": [
        {
            "dep_id": "T01",
            "dep_name": "Test学院",
            "master_name": "Test-Master",
            "slogan": "Here is Slogan"
        }
    ]
}

#!/usr/bin/python
# encoding=utf-8
# import sys
# sys.path.append('..')
# import apis.aep_device_command

# if __name__ == '__main__':
#     result = apis.aep_device_command.CreateCommand('HY0lo5y1pdf','qAtI0mOLLw', '08d4f9289d9a407993f255c0a67028d8', '{\"content\":{\"params\":{\"data_download\":\"345678\"},\"serviceIdentifier\":\"8001\"},\"deviceId\":\"e5459e56135f48bcabfe458a93931731\",\"operator\":\"lu\",\"productId\":17045165}')
#     print('result='+str(result))

# response = requests.post("http://127.0.0.1:5680/aiot/query_nbiot", json=data)
# response = requests.post("http://127.0.0.1:5680/nbdata", json=data)
# response = requests.post("http://localhost:5680/test", json=data)
# # # response = requests.post("http://127.0.0.1:5680/tcpdata", json=data)
# content = response.content
# print("content1111111=", content);

# import sys
# sys.path.append('..')
# import apis.aep_device_management

# if __name__ == '__main__':
#     # result = apis.aep_device_management.QueryDevice('HY0lo5y1pdf','qAtI0mOLLw', '08d4f9289d9a407993f255c0a67028d8', 'e5459e56135f48bcabfe458a93931731', 17045165)
#     result = apis.aep_device_management.QueryDevice('HY0lo5y1pdf','qAtI0mOLLw', '08d4f9289d9a407993f255c0a67028d8', 'e5459e56135f48bcabfe458a93931731', 17045165)
#     print('result='+str(result))

# result = apis.aep_device_command.CreateCommand('HY0lo5y1pdf','qAtI0mOLLw', '08d4f9289d9a407993f255c0a67028d8', '{\"content\":{\"params\":{\"rsrp\":123,\"sinr\":123,\"pci\":123,\"ecl\":123,\"cell_id\":123},\"serviceIdentifier\":\"2\"},\"deviceId\":\"e5459e56135f48bcabfe458a93931731\",\"operator\":\"lu\",\"productId\":17045165}')
# result = apis.aep_device_command.CreateCommand('HY0lo5y1pdf','qAtI0mOLLw', '08d4f9289d9a407993f255c0a67028d8', '{\"content\":{\"params\":{\"rsrp\":123,\"sinr\":123,\"pci\":123,\"ecl\":123,\"cell_id\":123},\"serviceIdentifier\":\"3\"},\"deviceId\":\"e5459e56135f48bcabfe458a93931731\",\"operator\":\"lu\",\"productId\":17045165}')

snddata="112"

data={
  "content": {
        "params":{"data_download":snddata},
    "serviceIdentifier": "8001"
    },
  "deviceId": "e5459e56135f48bcabfe458a93931731",
  "operator": "lu",
  "productId": 17045165
}
result = apis.aep_device_command.CreateCommand('HY0lo5y1pdf','qAtI0mOLLw', '08d4f9289d9a407993f255c0a67028d8', json.dumps(data))
# result = apis.aep_device_command.CreateCommand('HY0lo5y1pdf','qAtI0mOLLw', '08d4f9289d9a407993f255c0a67028d8', '{\"content\":{\"params\":{\"data_download_resp\":\"345678\"},\"serviceIdentifier\":\"9001\"},\"deviceId\":\"e5459e56135f48bcabfe458a93931731\",\"operator\":\"lu\",\"productId\":17045165}')
# result = apis.aep_device_command.CreateCommand('HY0lo5y1pdf','qAtI0mOLLw', '08d4f9289d9a407993f255c0a67028d8', '{\"content\":{\"params\":{\"signalPower\":11, \"snr\":32, \"txPower\":54, \"cellld\":32},\"serviceIdentifier\":\"10001\"},\"deviceId\":\"e5459e56135f48bcabfe458a93931731\",\"operator\":\"lu\",\"productId\":17045165}')
print('result='+str(result))

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