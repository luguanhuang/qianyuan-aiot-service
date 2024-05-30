import binascii

import socket
import time
import threading
#01
#000c
#313730343436
#323631323334002b4d4f75765f6758776a346e395749326d75516d51764e4a4e3374613046476d4f4d6179423138564b7144550003312e30

# message_type = message[0:2]
# print("message_type=", message_type)
# device_id_length = int(message[2:6], 16) * 2
# print("data=", device_id_length)
# device_id = message[6:6+device_id_length]
# print("device_id=", device_id)
# password_length_index = 6 + device_id_length
# password_length = int(message[password_length_index:password_length_index+4], 16)*2
# password_index = password_length_index + 4
# password = message[password_index:password_index+password_length]
# print("password=", password)
# # 解析版本信息长度和版本信息
# version_length_index = password_index + password_length
# version_length = int(message[version_length_index:version_length_index+4], 16)*2
# version_index = version_length_index + 4
# version = message[version_index:version_index+version_length]
# print("version=", version)
# 创建一个 TCP/IP socket

def recvmsg(client_socket):
    while True:
        try:
            recvdata = client_socket.recv(1024).decode()
            
            data_length = int(recvdata[2:6], 16) * 2
            print("recvdata=", recvdata, " data_length=", data_length, " data=", recvdata[2:6])

            command = recvdata[10:14]
            print("command=", command)
            # 解析地址
            address = recvdata[14:22]
            
            print("command=", command, " address1=", binascii.unhexlify(address).decode())

            # # 解析数据序号
            data_sequence = recvdata[22:24]
            
            data_field_length = int(recvdata[24:28], 16)*2
            print(data_field_length)
            data_field = recvdata[28:28+data_field_length]
            
            # 解析帧尾
            frame_tail = recvdata[-6:]
            
            print(command, address, data_sequence, binascii.unhexlify(data_field).decode())

            # ret = client_socket.send(b"070000")
            # print("ret=", ret)
            # device_id = message[6:6+device_id_length]
            # print("device_id=", device_id)
            # # 解析密码长度和密码
            # password_length_index = 6 + device_id_length
            # password_length = int(message[password_length_index:password_length_index+4], 16)*2
            # password_index = password_length_index + 4
            # password = message[password_index:password_index+password_length]
            # print("password=", password)
            # # 解析版本信息长度和版本信息
            # version_length_index = password_index + password_length
            # version_length = int(message[version_length_index:version_length_index+4], 16)*2
            # version_index = version_length_index + 4
            # version = message[version_index:version_index+version_length]
        except Exception as e:
            i=1

def sndheartbeatmsg(client_socket):
    while True:
        try:
            time.sleep(4)
            snddata = b'04'
            
            ret = client_socket.send(snddata)
            print("snddata=", snddata, " ret=", ret)
            resdata = client_socket.recv(2).decode()
            print("resdata=", resdata)
            
        except Exception as e:
            rint("e=", e)
            i=1

        time.sleep(2)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# # 连接服务器
server_address = ('localhost', 8990)
sock.connect(server_address)

# # 发送消息
# message = b'Hello, World!'
message = b"01000c313730343436323631323334002b4d4f75765f6758776a346e395749326d75516d51764e4a4e3374613046476d4f4d6179423138564b7144550003312e30"
# # message = b"0200184040000131323334FF000A31323334353637383930232323"
sock.send(message)
print("before recv")
message = sock.recv(1024).decode()
cmd = message[0:2]
status = message[2:6]
print("cmd=", cmd, " status=", status)
# sock.close()
# exit(0)
# 启动线程
# my_thread = threading.Thread(target=recvmsg, args=(sock, ), daemon=True)
# my_thread.start()
time.sleep(1)

#这个和recvmsg都是接收  会冲突  如果两个都启动
my_thread = threading.Thread(target=sndheartbeatmsg, args=(sock, ), daemon=True)
my_thread.start()

# time.sleep(2)

# message = b"0200184040000131323334FF000A31323334353637383930232323"
# sock.send(message)
# print("before recv")
# message = sock.recv(1024).decode()
# cmd = message[0:2]
# status = message[2:6]
# print("cmd=", cmd, " status=", status)


while True:
    time.sleep(3)
sock.close()
# # 关闭连接
# sock.shutdown(socket.SHUT_WR)  # 关闭发送
# sock.close()