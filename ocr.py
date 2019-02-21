# -*- coding: utf-8 -*-

from urllib import parse
import requests
import json
from PIL import Image
import time
import base64
import hashlib
from io import BytesIO
import urllib3


urllib3.disable_warnings()

app_id = 2111840508
app_key = 'zpw9pYdvHYjOhv3K'

def getSign(param):
    res = parse.urlencode([(k,param[k]) for k in sorted(param.keys())])
    res += "&app_key=%s"%app_key
    res = hashlib.md5(res.encode('utf8')).hexdigest()
    return res.upper()

local_res = None

def send(img):
    #print("ocr查询中")
    start_time = time.time()
    param = {}
    param['app_id'] = app_id
    
    buffered = BytesIO()
    img.save(buffered, format="png")
    param['image'] = base64.b64encode(buffered.getvalue())
    
    
    param['nonce_str'] = 'GAGAGAGAGA'
    param['time_stamp'] = time.time()
    param['sign'] = getSign(param)
    #url = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr'
    url = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_handwritingocr'
    headers = {
            'Connection': 'close',
            'Content-Type':'application/x-www-form-urlencoded'
    }
    response = None
    try :
        response = requests.post(url,data = param,headers = headers,verify=False,timeout = 3)
    except requests.exceptions.SSLError:
        print("请求出错!")
        time.sleep(5)
        return send(img)
    except requests.exceptions.ConnectionError:
        print("连接出错!")
        time.sleep(5)
        return send(img)
    except requests.exceptions.ReadTimeout:
        print("请求超时!")
        time.sleep(1)
        return send(img)
    #print("ocr耗时",time.time()-start_time)
    try:
        data = response.json()
        #print("请求成功")
        return data
    except:
        print(response.text)
        time.sleep(3)
        return send(img)
    

def send__(img):
    #print("ocr查询中")
    start_time = time.time()
    param = {}
    param['app_id'] = app_id
    
    buffered = BytesIO()
    img.save(buffered, format="png")
    param['image'] = base64.b64encode(buffered.getvalue())
    
    
    param['nonce_str'] = 'GAGAGAGAGA'
    param['time_stamp'] = time.time()
    param['id'] = "fgoocr"
    param['sign'] = hashlib.md5((param['id']+"galaxy").encode('utf8')).hexdigest()
    url = 'http://119.29.36.93/api/ocr.php'
    response = requests.post(url,data = param)
    print(response.status_code)
    return response
    data = response.json()
    #print("请求成功")
    return data

