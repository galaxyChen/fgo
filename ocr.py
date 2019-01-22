# -*- coding: utf-8 -*-

from urllib import parse
import requests
import json
from PIL import Image
import time
import base64
import hashlib
from io import BytesIO

app_id = 2111335320
app_key = 'aL5mzBaGQ2XtY0ZR'

def getSign(param):
    res = parse.urlencode(param)
    res += "&app_key=%s"%app_key
    res = hashlib.md5(res.encode('utf8')).hexdigest()
    return res.upper()

def send(img):
    start_time = time.time()
    param = {}
    param['app_id'] = app_id
    
    buffered = BytesIO()
    img.save(buffered, format="png")
    param['image'] = base64.b64encode(buffered.getvalue())
    
    
    param['nonce_str'] = 'GAGAGAGAGA'
    param['time_stamp'] = time.time()
    param['sign'] = getSign(param)
    url = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr'
    response = requests.post(url,param)
    #print("ocr耗时",time.time()-start_time)
    return response.json()
    

    
