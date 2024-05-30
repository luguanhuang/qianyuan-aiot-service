# -*- coding: utf-8 -*-

from fastapi import FastAPI,Request,Response
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from config import setting 
from services.http.public import app as public_api
from utils.log import logger
from utils.log import httplogger
import json
from utils.active_mq import activemq_client
import sys
sys.path.append('..')
import apis.aep_device_command

app = FastAPI()
app.include_router(public_api, prefix="/aiot")
# 这里配置支持跨域访问的前端地址
origins = [
    "*",     # 带端口的
]

# 将配置挂在到app上
app.add_middleware(
    CORSMiddleware,
    # 这里配置允许跨域访问的前端地址
    allow_origins=origins,
    # 跨域请求是否支持 cookie， 如果这里配置true，则allow_origins不能配置*
    allow_credentials=True,
    # 支持跨域的请求类型，可以单独配置get、post等，也可以直接使用通配符*表示支持所有
    allow_methods=["*"],
    allow_headers=["*"],
)

# # app.include_router(ctwing_api,prefix="",tags=['签名', '认证'])

# @app.middleware('http')
# async def sign(request:Request,call_next):
#     try:
#         pass
#         # 校验签名
#         # 
#     except BaseException as e:
#         logger.error(e)
#         response= Response(json.dumps({
#                     "errorcode":"9001",
#                     "message":"pwfailure"
#                 }),200,)
#         logger.info(f'【{request.method}】【{request.client.host}:{request.client.port}】【{response.status_code}】【{request.url}】')
#     return response

@app.post("/test")  
def nbdataMessage(data:dict): 
    httplogger.info(f"test data={data}")
    result = apis.aep_device_command.CreateCommand('HY0lo5y1pdf','qAtI0mOLLw', '08d4f9289d9a407993f255c0a67028d8', '{\"content\":{\"params\":{\"data_download\":\"345678\"},\"serviceIdentifier\":\"8001\"},\"deviceId\":\"e5459e56135f48bcabfe458a93931731\",\"operator\":\"lu\",\"productId\":17045165}')
    print('result='+str(result))
    
    return {
            "errorcode":"0000",
            "message":"success"
        }
@app.post("/nbdata")  
def nbdataMessage(data:dict): 
    httplogger.info(f"nbdataMessage data={data}")
    senddata = ""
    if "payload" in data:
        senddata = {
            "timestamp": data['timestamp'],
            "tenantId": data['tenantId'],
            "serviceId": data['serviceId'],
            "protocol": data['protocol'],
            "productId": data['productId'],
            "payload": data['payload'],
            "deviceId": data['deviceId'],
            "IMSI": data['IMSI'],
            "IMEI": data['IMEI']
        }

        activemq_client.send_to_nbiot_queue(senddata)
       
    elif "eventContent" in data:
        senddata = {
            "timestamp": data['timestamp'],
            "tenantId": data['tenantId'],
            "serviceId": data['serviceId'],
            "protocol": data['protocol'],
            "productId": data['productId'],
            "payload": data['eventContent'],
            "deviceId": data['deviceId'],
            "IMSI": data['IMSI'],
            "IMEI": data['IMEI']
        }

        activemq_client.send_to_nbiot_queue(senddata)
    else:
        activemq_client.send_to_nbiot_queue(data)

    return {
            "errorcode":"0000",
            "message":"success",
            "ClientID":"112",
            "token":"223",
            "ip_lan": "11.22.33.11",
            "expires_in":"86400"
        }

@app.post("/mqttdata")  
async def mqttdataMessage(data:dict): 
    httplogger.info(f"mqttdataMessage data={data}")
    activemq_client.send_to_mqtt_queue(data)
    return {
            "errorcode":"0000",
            "message":"success",
            "ClientID":"112",
            "token":"223",
            "ip_lan": "11.22.33.11",
            "expires_in":"86400"
        }


@app.post("/tcpdata")  
async def tcpdataMessage(data:dict): 
    activemq_client.send_to_tcp_queue(data)
    httplogger.info(f"tcpdataMessage data={data}")
    return {
            "errorcode":"0000",
            "message":"success",
            "ClientID":"112",
            "token":"223",
            "ip_lan": "11.22.33.11",
            "expires_in":"86400"
        }

@app.post("/aiotsign")  
async def aiotsignMessage(data:dict): 
    httplogger.info(f"aiotsign data={data}")
    
    return {
            "errorcode":"0000",
            "message":"success",
            "ClientID":"112",
            "token":"223",
            "ip_lan": "11.22.33.11",
            "expires_in":"86400"
        }




def htttp_start():
    print("listen httpport=", setting.httpport)
    uvicorn.run(app = 'services.http.server:app', workers=20, reload=True,host="0.0.0.0",port=setting.httpport)

def init_activemq():
    print("activemqrecvnbiotqueueid=", setting.activemqrecvnbiotqueueid)
    activemq_client.subscribenbiot(setting.activemqrecvnbiotqueueid, 1)
    activemq_client.subscribemqtt(setting.activemqrecvmqttqueueid, 2)  