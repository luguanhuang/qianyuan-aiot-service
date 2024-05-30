import requests

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

# response = requests.post("http://127.0.0.1:5680/aiot/query_nbiot", json=data)
# response = requests.post("http://127.0.0.1:5680/nbdata", json=data)
response = requests.post("http://127.0.0.1:5680/mqttdata", json=data)
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