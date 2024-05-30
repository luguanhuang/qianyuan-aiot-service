pkill -f main_pserver_aiot_http.py
pkill -f main_pserver_aiot_mqtt.py
pkill -f main_pserver_aiot_tcp.py
nohup /root/project/pserver_aiot/qianyuan-aiot-service/venv/bin/python /root/project/pserver_aiot/qianyuan-aiot-service/main_pserver_aiot_http.py > /dev/null &
nohup /root/project/pserver_aiot/qianyuan-aiot-service/venv/bin/python /root/project/pserver_aiot/qianyuan-aiot-service/main_pserver_aiot_mqtt.py > /dev/null &
nohup /root/project/pserver_aiot/qianyuan-aiot-service/venv/bin/python /root/project/pserver_aiot/qianyuan-aiot-service/main_pserver_aiot_tcp.py > /dev/null &
# nohup python3 main_pserver_aiot_http.py > /dev/null &
# nohup python3 main_pserver_aiot_mqtt.py > /dev/null &
# nohup python3 main_pserver_aiot_tcp.py > /dev/null &