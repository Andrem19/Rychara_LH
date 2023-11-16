# python
# from pymexc import spot, futures
# from mexc_sdk import Spot
# futures_client = futures.HTTP(api_key = api_key, api_secret = secret_key)
# spot = Spot(api_key='apiKey', apiSecret='apiSecret')
# res = futures_client.history_orders('SOLUSDT')
# price = futures_client.ticker('SOLUSDT')
# res1 = futures_client.order('SOLUSDT', 18.92, 1, 1, 5, 2)
# asset = futures_client.asset('USDT')

import time
import hmac
import hashlib
from urllib.parse import quote_plus
import json
import requests

api_key = 'YOUR_API_KEY'
secret_key = 'YOUR_SECRET_KEY'

class SignVo:
    def __init__(self):
        self.req_time = None
        self.access_key = None
        self.secret_key = None
        self.request_param = None

def get_request_param_string(data):
    params = []
    for key, value in data.items():
        params.append(f"{key}={value}")
    return '&'.join(params)

def sign(sign_vo):
    data = f"accessKey={sign_vo.access_key}&reqTime={sign_vo.req_time}&{sign_vo.request_param}".encode('utf-8')
    signature = hmac.new(sign_vo.secret_key.encode('utf-8'), data, hashlib.sha256).hexdigest()
    return signature

def place_order(payload):
    url = 'https://contract.mexc.com/api/v1/private/account/assets'
    # url = 'https://contract.mexc.com/api/v1/private/order/submit'
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': api_key,
        'Request-Time': str(int(time.time() * 1000)),
        'Signature': None
    }

    data = {
        'symbol': payload['symbol'],
        'price': payload['price'],
        'vol': payload['vol'],
        'side': payload['side'],
        'type': payload['type'],
        'openType': payload['openType']
    }
    
    sign_vo = SignVo()
    sign_vo.req_time = headers['Request-Time']
    sign_vo.access_key = api_key
    sign_vo.secret_key = secret_key
    sign_vo.request_param = get_request_param_string(data)
    
    signature = sign(sign_vo)
    
    headers['Signature'] = signature
    
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.text)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Usage
payload = {
      'symbol': 'SOLUSDT',
      'price': 18.95,
      'vol': 1,
      'side': 1,
      'type': 5,
      'openType': 2,
}

response = place_order(payload)
print(response)

