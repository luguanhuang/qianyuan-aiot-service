# -*-coding:utf-8-*-
# import stomp
 
 
# # 队列名
# location_queue = "123456"
# conn = stomp.Connection([('127.0.0.1', 61613)])
# conn.connect(username='admin', passcode='admin', wait=True)
 
 
# class SampleListener(object):
    
#     def on_message(self, headers, message):
#         # print('headers: %s' % headers)
#         # print('message: %s' % message)
#         # print("headers: ", headers)
#         # print("message: ", message)
#         print("headers: ")
#         # print("message: ", message)
 
# def receive_from_queue():
#     # 如果接受数据,就调用这个类,里面的参数是类名和类,名称必须一致
#     conn.set_listener('SampleListener', SampleListener())
#     # 从选择的管道中区数据,管道名,id(随便写一个数字就行)
#     conn.subscribe(location_queue, 12)
#     # 不能让程序停止,负责每传一次数据都得接收一次
#     while True:
#         pass
 
 
 
# if __name__ == '__main__':
#     receive_from_queue()
#     conn.disconnect()



import stomp
import time

class MyListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print('Received a mqtt message: "{}"'.format(frame.body))
 
    def on_error(self, frame):
        print('Received an error "{}"'.format(frame.body))
 
# conn = stomp.Connection([('localhost', 61613)])  # 默认端口为61613
conn = stomp.Connection([('amq.hystudio.cn', 61613)])  # 默认端口为61613
conn.set_listener('', MyListener())
conn.connect('admin', 'admin', wait=True)
 
# conn.subscribe(destination='mqtt_upload_qyzn', id=2, ack='auto')
conn.subscribe(destination='/topic/tcp_upload_qyzn', id=2, ack='auto')
 
# 接收消息，需要运行一个循环
while True:
    time.sleep(12)
    # conn.iterate()