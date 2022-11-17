import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json
import bs4

def get_html(url):
    '''
    封装请求
    '''
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'ContentType':
        'text/html; charset=utf-8',
        'Accept-Encoding':
        'gzip, deflate, sdch',
        'Accept-Language':
        'zh-CN,zh;q=0.8',
        'Connection':
        'keep-alive',
    }
    try:
        htmlcontet = requests.get(url, headers=headers, timeout=30)
        htmlcontet.raise_for_status()
        htmlcontet.encoding = 'utf-8'
        return htmlcontet.text
    except:
        return " 请求失败 "
 
def get_content(url):
    '''
    抓取页面天气数据
    '''
    weather_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    content_ul = soup.find('div', class_='t').find('ul', class_='clearfix').find_all('li')
    content= content_ul[0]

    weather = {}
    # '雨'， 'xx日', xx , x 
    weather['condition'] = str(content.find('p', class_='wea').text)
    weather['day'] = str(content.find('h1'))[4:-7]
    weather['temperature'] = int(content.find('p', class_='tem').span.text)
    weather['win'] = str(content.find('p', class_='win').span.text)
    weather_list.append(weather)
    #print(weather_list)
    return weather_list

def gen_message(wealist):
    mes = wealist[0]['day'] +'\n' + str(wealist[0]['temperature']) + '°C\n'
    rain = '雨' in wealist[0]['condition']
    
    if ('<' in wealist[0]['win'] or '>' in wealist[0]['win']):
        wealist[0]['win'] = wealist[0]['win'][1:]
        
    
    if( '0' in wealist[0]['win']) :
        mes += '无风' 
    elif( '1' in wealist[0]['win']) :
        mes += '软风' + wealist[0]['win']
    elif( '2' in wealist[0]['win']) :
        mes += '轻风' + wealist[0]['win']
    elif( '3' in wealist[0]['win']) :
        mes += '微风' + wealist[0]['win']
    elif( '4' in wealist[0]['win']) :
        mes += '和风' + wealist[0]['win']
    elif( '5' in wealist[0]['win']) :
        mes += '清风' + wealist[0]['win']
    else:
        mes += '大风起兮云飞扬,' + wealist[0]['win']
    mes += '\n'    
    if(rain):
        mes += wealist[0]['condition'] +','+'记得带伞\n'
    else:
        mes += wealist[0]['condition'] +'\n'
        
    return mes,rain
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
                   ''
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
send_message(15021752246, mes,rain)
