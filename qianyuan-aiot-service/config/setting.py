"""全局变量 配置文件"""
from utils.load_yaml import config

httpport = config.get("http",{}).get("port")
tcpport = config.get("tcp",{}).get("port")

activemqip = config.get("activemq",{}).get("connecionhost")
activemqport = config.get("activemq",{}).get("connecionport")
activemquser = config.get("activemq",{}).get("user")
activemqpasswd = config.get("activemq",{}).get("passwd")
activemqsendnbiotqueueid = config.get("activemq",{}).get("sendnbiotqueueid")
activemqsendmqttqueueid = config.get("activemq",{}).get("sendmqttqueueid")
activemqsendtcpqueueid = config.get("activemq",{}).get("sendtcpqueueid")
activemqrecvnbiotqueueid = config.get("activemq",{}).get("recvnbiotqueueid")
activemqrecvmqttqueueid = config.get("activemq",{}).get("recvmqttqueueid")
activemqrecvtcpqueueid = config.get("activemq",{}).get("recvtcpqueueid")

#mqtt
mqttport = config.get("mqttinfo",{}).get("port")
mqttbroker = config.get("mqttinfo",{}).get("broker")
mqtttopic = config.get("mqttinfo",{}).get("topic")
mqttclitopic = "data_mqttdownload_"

mysqlhost = "1.13.190.117"
mysqlport = 13306
mysqluser = "root"
mysqlpassword = "qyzn@mysql0212"
mysqldatabase = "aiot"

connection_timeout_time = 300
listen_queue=1000

appKey = "HY0lo5y1pdf"
appSecret = "qAtI0mOLLw"
MasterKey_NB = "08d4f9289d9a407993f255c0a67028d8"
deviceId = "2c330d43c8524a7bb3dfa84cc427146c"

login_timeout_time=300
max_snd_cnt = 30
lock_time=30
sndpackertimediff = 60
max_resnd_cnd = 3