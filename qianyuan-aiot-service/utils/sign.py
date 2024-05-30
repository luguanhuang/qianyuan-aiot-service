import time
import hmac
import hashlib
import base64
import uuid

class SignUtils:
    def __init__(self) -> None:
        self.ACCESS_KEY_ID = "LTAIzko9W17q0001sensor"
        self.ACCESS_KEY_SECRET = "8R2qDryesgBo777MsIRpW7R7ZAsensipwater"

    def SignToQueryString(self):
        data = {
            "action": "i.ipwater.cc.sign",
            "accessKeyId": self.ACCESS_KEY_ID,
            "algorithm": "hmac-sha256",
            "timestamp": str(int(round(time.time() * 1000))),
            "nonce": "".join(str(uuid.uuid4()).split("-")),
        }
        sorted_data = sorted(data.items(), key=lambda x: x[0])
        strToSign = self.queryStringify(sorted_data)
        data["signature"] = self.getSignature(
            strToSign, self.ACCESS_KEY_SECRET)
        data = sorted(data.items(), key=lambda x: x[0])
        res = self.queryStringify(data)

        if res[0] == "&":
            res = res[1:]
        return res.replace("+", "%2B")

    def getSignature(self, message, secretKey):
        if message[0] == "&":
            message = message[1:]
        _sign = base64.b64encode(hmac.new(bytes(secretKey.encode("utf-8")), bytes(
            message.encode("utf-8")), digestmod=hashlib.sha256).digest()).decode("ascii")
        return _sign

    def queryStringify(self, data):
        res = ""
        for k, v in data:
            res += '&' + k + '=' + v
        return res
