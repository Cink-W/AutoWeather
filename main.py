import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import wea
def send_message(mobile,text,rain):
    timestamp = str(round(time.time() * 1000))
    #加签
    secret = 'SEC3c031bc19603a045a37cb72e81daa14f06120e979d2133d8250aad239a27fc00'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    #Webhook
    Webhook = "https://oapi.dingtalk.com/robot/send?access_token=ef05453dd83d8a42c9cf72314c6f77e2e9b7ec7ef13483b098655d888448a28a"
    #加上签之后网址后面要加上 一段签名计算代买后的sign以及时间，不加签的应该不需要后面跟的。
    url =  Webhook + "&timestamp={}&sign={}".format(timestamp, sign)
    headers = {
        'Content-Type': 'application/json'
    }
    if rain:
        json ={
            "at": {
                "atMobiles":[
                    mobile
                ],
                "atUserIds":[
                    ""
                ],
                "isAtAll": "false"
            },
            "text": {
                "content": text
            },
            "msgtype":"text"
        }
    else:
        json ={
            # "at": {
            #     "atMobiles":[
            #         mobile
            #     ],
            #     "atUserIds":[
            #         ""
            #     ],
            #     "isAtAll": "false"
            # },
            "text": {
                "content": text
            },
            "msgtype":"text"}
    requests.post(url=url , headers= headers,json=json)
    
url = 'http://www.weather.com.cn/weather1d/101210113.shtml'
wealist = get_content(url)
mes,rain = gen_message(wealist)
send_message(18368320156, mes,rain)