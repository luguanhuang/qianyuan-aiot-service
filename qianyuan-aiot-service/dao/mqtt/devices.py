from utils.sql_helper import sql_helper

def select_mqtt_aiot_by_imei(imei):
    sql = """
    select token_num,expires_in from mqtt_aiot where imei=%s
    """
    print("sql=", sql, " imei=", imei)
    resdata = sql_helper.fetch_one(sql, (imei))
    return resdata


def select_mqtt_aiot_by_id(clientid, imei, pw_mqtt):
    sql = """
    select token_num,expires_in from mqtt_aiot where imei=%s and clientid=%s and pw_mqtt=%s
    """
    print("sql=", sql, " imei=", imei, " clientid=", clientid, " pw_mqtt=", pw_mqtt)
    resdata = sql_helper.fetch_one(sql, (imei, clientid, pw_mqtt))
    return resdata