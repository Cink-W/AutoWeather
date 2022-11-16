# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 15:39:00 2022

@author: Wang
"""

import json
import requests
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
        mes += '大风起兮云飞扬' + wealist[0]['win']
    mes += '\n'    
    if(rain):
        mes += wealist[0]['condition'] +','+'记得带伞\n'
    else:
        mes += wealist[0]['condition'] +'\n'
        
    return mes,rain

    