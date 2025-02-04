#!/usr/bin/python
# encoding=utf-8

import sys
if sys.version_info[0] == 2:
    # Python2
    import core.AepSdkRequestSend as AepSdkRequestSend
else:
    # Python3
    from apis.core import AepSdkRequestSend



#参数MasterKey: 类型String, 参数不可以为空
#  描述:公共产品的MasterKey
#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def QueryDeviceToken(appKey, appSecret, MasterKey, body):
    path = '/aep_public_product_device/queryDeviceToken'
    head = {}
    param = {}
    version = '20230330172346'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, MasterKey, key, 'POST')
    if response is not None:
        return response.read()
    return None

