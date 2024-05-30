#!/usr/bin/python
# encoding=utf-8

import sys
if sys.version_info[0] == 2:
    # Python2
    import core.AepSdkRequestSend as AepSdkRequestSend
else:
    # Python3
    from apis.core import AepSdkRequestSend



#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def DeleteArchivesInfo(appKey, appSecret, body):
    path = '/device_archives/deleteArchivesInfo'
    head = {}
    param = {}
    version = '20231117042743'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, None, key, 'POST')
    if response is not None:
        return response.read()
    return None

#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def GetArchivesAttribute(appKey, appSecret, body):
    path = '/device_archives/getArchivesAttr'
    head = {}
    param = {}
    version = '20231117042748'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, None, key, 'POST')
    if response is not None:
        return response.read()
    return None

#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def UpdateArchivesInfo(appKey, appSecret, body):
    path = '/device_archives/updateArchivesInfo'
    head = {}
    param = {}
    version = '20231117042738'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, None, key, 'POST')
    if response is not None:
        return response.read()
    return None

#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def AddArchivesInfo(appKey, appSecret, body):
    path = '/device_archives/addArchivesInfo'
    head = {}
    param = {}
    version = '20231215034317'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, None, key, 'POST')
    if response is not None:
        return response.read()
    return None

#参数searchValueType: 类型long, 参数可以为空
#  描述:1：按设备id查询，2：按设备类型查询
#参数searchValue: 类型String, 参数可以为空
#  描述:
#参数pageNow: 类型long, 参数不可以为空
#  描述:
#参数pageSize: 类型long, 参数不可以为空
#  描述:
def GetArchivesInfo(appKey, appSecret, searchValueType, searchValue, pageNow, pageSize):
    path = '/device_archives/getArchivesInfo'
    head = {}
    param = {'searchValueType':searchValueType, 'searchValue':searchValue, 'pageNow':pageNow, 'pageSize':pageSize}
    version = '20231215034340'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, None, version, application, None, key, 'GET')
    if response is not None:
        return response.read()
    return None

#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def GetDeviceType(appKey, appSecret, body):
    path = '/device_archives/getDeviceType'
    head = {}
    param = {}
    version = '20231215034248'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, None, key, 'POST')
    if response is not None:
        return response.read()
    return None

