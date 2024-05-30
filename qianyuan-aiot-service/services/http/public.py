from fastapi import  APIRouter
from apis import aep_device_management
from config import setting
app = APIRouter()
import json

@app.post("/query_nbiot")
def query_nbiot(data:dict):
    
    try:
        res = aep_device_management.QueryDevice(setting.appKey, setting.appSecret,data.get("MasterKey"),data.get("deviceId"),data.get("productId"))
        res = json.loads(res.decode())
        return {"errorcode":"0000","message": "success","deviceId": data.get("deviceId"),"result":res.get("result")}
    except Exception as e:
        print(f"请求出错 {e}")
        return {"errorcode":"9999","message": "success","deviceId": data.get("deviceId"),"result":{}}


@app.post("/create_nbiot")
def query_nbiot(data:dict):
    try:
        res = aep_device_management.CreateDevice(setting.appKey, setting.appSecret,setting.MasterKey_NB,json.dumps(data))
        res = json.loads(res.decode())
        print(res)
        return {"errorcode":"0000","message": res.get("msg"),"deviceId": data.get("deviceId"),"result":res.get("result")}
    except Exception as e:
        print(f"请求出错 {e}")
        return {"errorcode":"9999","message": "success","imei": data.get("imei"),"result":{}}


@app.post("/delete_nbiot")
def query_nbiot(data:dict):
    return {"errorcode":"0000"}


@app.post("/query_mqtttcp")
def query_nbiot(data:dict):
    return {"errorcode":"0000"}


@app.post("/create_mqtttcp")
def query_nbiot(data:dict):
    return {"errorcode":"0000"}


@app.post("/delete_mqtttcp")
def query_nbiot(data:dict):
    return {"errorcode":"0000"}