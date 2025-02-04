#!/usr/bin/python
# encoding=utf-8

import sys
if sys.version_info[0] == 2:
    # Python2
    import core.AepSdkRequestSend as AepSdkRequestSend
else:
    # Python3
    from apis.core import AepSdkRequestSend



#参数MasterKey: 类型String, 参数可以为空
#  描述:
#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def CreateDeviceGroup(appKey, appSecret, MasterKey, body):
    path = '/aep_device_group_management/deviceGroup'
    head = {}
    param = {}
    version = '20190615001622'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, MasterKey, key, 'POST')
    if response is not None:
        return response.read()
    return None

#参数MasterKey: 类型String, 参数可以为空
#  描述:
#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def UpdateDeviceGroup(appKey, appSecret, MasterKey, body):
    path = '/aep_device_group_management/deviceGroup'
    head = {}
    param = {}
    version = '20190615001615'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, MasterKey, key, 'PUT')
    if response is not None:
        return response.read()
    return None

#参数productId: 类型long, 参数可以为空
#  描述:产品Id，单产品分组必填
#参数deviceGroupId: 类型long, 参数不可以为空
#  描述:分组Id
#参数MasterKey: 类型String, 参数可以为空
#  描述:
def DeleteDeviceGroup(appKey, appSecret, productId, deviceGroupId, MasterKey):
    path = '/aep_device_group_management/deviceGroup'
    head = {}
    param = {'productId':productId, 'deviceGroupId':deviceGroupId}
    version = '20190615001601'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, None, version, application, MasterKey, key, 'DELETE')
    if response is not None:
        return response.read()
    return None

#参数pageNow: 类型long, 参数不可以为空
#  描述:当前页数
#参数pageSize: 类型long, 参数不可以为空
#  描述:每页记录数
#参数productId: 类型long, 参数可以为空
#  描述:支持通过产品id查询单产品分组列表
#参数deviceGroupId: 类型long, 参数可以为空
#  描述:支持通过分组ID查询
#参数deviceGroupName: 类型String, 参数可以为空
#  描述:支持通过分组名称查询
#参数groupLevel: 类型long, 参数可以为空
#  描述:支持通过分组类别查询，0为单产品分组，1为多产品分组
def QueryDeviceGroupList(appKey, appSecret, pageNow, pageSize, productId, deviceGroupId, deviceGroupName, groupLevel):
    path = '/aep_device_group_management/deviceGroups'
    head = {}
    param = {'pageNow':pageNow, 'pageSize':pageSize, 'productId':productId, 'deviceGroupId':deviceGroupId, 'deviceGroupName':deviceGroupName, 'groupLevel':groupLevel}
    version = '20230218035819'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, None, version, application, None, key, 'GET')
    if response is not None:
        return response.read()
    return None

#参数MasterKey: 类型String, 参数可以为空
#  描述:
#参数productId: 类型long, 参数可以为空
#  描述:产品ID，查询单产品分组下已关联的设备列表或产品下未关联的设备列表时必填
#参数searchValue: 类型String, 参数可以为空
#  描述:可查询：设备ID，设备名称，设备编号或者IMEI号；仅支持单产品分组查询
#参数pageNow: 类型long, 参数不可以为空
#  描述:当前页数
#参数pageSize: 类型long, 参数不可以为空
#  描述:每页条数
#参数deviceGroupId: 类型long, 参数可以为空
#  描述:群组ID：1.有值则查询该群组已关联的设备信息列表。2.为空则查询该产品下未关联的设备信息列表
def QueryGroupDeviceList(appKey, appSecret, MasterKey, productId, searchValue, pageNow, pageSize, deviceGroupId):
    path = '/aep_device_group_management/groupDeviceList'
    head = {}
    param = {'productId':productId, 'searchValue':searchValue, 'pageNow':pageNow, 'pageSize':pageSize, 'deviceGroupId':deviceGroupId}
    version = '20190615001540'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, None, version, application, MasterKey, key, 'GET')
    if response is not None:
        return response.read()
    return None

#参数MasterKey: 类型String, 参数可以为空
#  描述:
#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def UpdateDeviceGroupRelation(appKey, appSecret, MasterKey, body):
    path = '/aep_device_group_management/deviceGroupRelation'
    head = {}
    param = {}
    version = '20190615001526'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, MasterKey, key, 'PUT')
    if response is not None:
        return response.read()
    return None

#参数productId: 类型long, 参数不可以为空
#  描述:
#参数deviceId: 类型String, 参数不可以为空
#  描述:
def getGroupDetailByDeviceId(appKey, appSecret, productId, deviceId):
    path = '/aep_device_group_management/groupOfDeviceId'
    head = {}
    param = {'productId':productId, 'deviceId':deviceId}
    version = '20211014095939'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, None, version, application, None, key, 'GET')
    if response is not None:
        return response.read()
    return None

