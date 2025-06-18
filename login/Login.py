import base64
import json

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class Login:
    def __init__(self, secret_key, point, token):
        self.secretKey = secret_key
        self.point = point
        self.token = token
        self.cipher = AES.new(self.secretKey.encode("utf-8"), AES.MODE_ECB)
        self.captchaType = "blockPuzzle"

    def check_captcha(self):
        pointJson = json.dumps({"x": self.point,"y": 5}).replace(" ", "")
        srcs = pad(pointJson.encode("utf-8"), AES.block_size)
        encrypted = self.cipher.encrypt(srcs)
        url = "http://localhost:48080/admin-api/system/captcha/check"

        data = {
            "token": self.token,
            "captchaType": self.captchaType,
            "pointJson": base64.b64encode(encrypted).decode('utf-8'),
        }
        response = requests.post(url, json=data)
        return response.json()

    def get_captcha_verification(self):
        pointJson = json.dumps({"x": self.point,"y": 5}).replace(" ", "")
        captchaVerificationSource = self.token + '---' + pointJson
        srcs = pad(captchaVerificationSource.encode("utf-8"), AES.block_size)
        print(captchaVerificationSource)
        captchaVerification = self.cipher.encrypt(srcs)
        result = base64.b64encode(captchaVerification).decode('utf-8')
        print(result)
        return result

    def login(self, tenantName, username, password):
        url = "http://localhost:48080/admin-api/system/auth/login"
        captchaVerification = self.get_captcha_verification()
        response = requests.post(url, headers={"tenant-id": "1"}, json={
            "username": username,
            "password": password,
            "tenantName": tenantName,
            "captchaVerification": captchaVerification,
        })
        print(response)
        return response.json()
