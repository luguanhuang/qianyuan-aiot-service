
# testdata = {}

# tee={
#     "lu":"12321",
#     "guan":"456",
#     "huang":"789"
# }

# tee1={
#     "lu":"12355",
#     "guan":"456",
#     "huang":"789"
# }

# testdata['11'] = tee
# testdata['12'] = tee1

# keys_to_remove = []
# for key in testdata:
#     print("key=", key, " lu=", testdata[key]['lu'])
#     keys_to_remove.append(key)

# for key in keys_to_remove:
#     del testdata[key]

# for key in testdata:
#     print("key=", key, " lu=", testdata[key]['lu'])


# testdata['11'] = 
# {
#     "lu":"123"
# }

# print("lu=", testdata['11']['lu'])
# print("guan=", testdata['11']['guan'])
# print("huang=", testdata['11']['huang'])


# import stomp
 
# class MyListener(stomp.ConnectionListener):
#     def on_message(self, frame):
#         print('Received a message: "{}"'.format(frame.body))
 
#     def on_error(self, frame):
#         print('Received an error "{}"'.format(frame.body))
 
# conn = stomp.Connection([('localhost', 61613)])  # ActiveMQ默认端口61613
# conn.set_listener('', MyListener())
# conn.connect('admin', 'password', wait=True)  # 使用正确的用户名和密码
 
# conn.send(body='Hello, STOMP', destination='/queue/test', content_type='text/plain')
 
# # 接收消息
# conn.subscribe(destination='/queue/test', id=1, ack='auto')
 
# # 做一些其他处理...
 
# # 断开连接
# conn.disconnect()


# -*-coding:utf-8-*-
 
import stomp
import time
 
# 队列名(接收方可以根据管道名来选择接受那个队列数据)
location_queue = "nbiot_download_qyzn"
# 服务器ip,端口固定用这个
conn = stomp.Connection([('127.0.0.1', 61613)])
# 账号密码
conn.connect(username='admin', passcode='admin', wait=True)
# conn.connect(wait=True)
 
 
def send_to_queue(msg):
    print('---------消息发送--------------')
    # body=数据, destination=根据队列名传输数据,如果队列不存在,就创建一个
    conn.send(body=str(msg), destination=location_queue)
    print(msg)
 
if __name__ == '__main__':
    send_to_queue('len 123')
    # receive_from_queue()
    conn.disconnect()
 
 