import os
import hmac
import hashlib
import base64
import requests
from datetime import datetime
from email.utils import formatdate
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv('REMITANO_ACCESS_KEY')
SECRET_KEY = os.getenv('REMITANO_SECRET_KEY')
AUTHENTICATOR = os.getenv('REMITANO_AUTHENTICATOR')
BASE_URL = os.getenv('REMITANO_BASE_URL')

def compute_md5(data):
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return base64.b64encode(md5.digest()).decode('utf-8')

def compute_hmac(secret, data):
    hmac_obj = hmac.new(secret.encode('utf-8'), data.encode('utf-8'), hashlib.sha1)
    return base64.b64encode(hmac_obj.digest()).decode('utf-8')

def get_headers(method, request_path, body=''):
    content_md5 = compute_md5(body)
    date = formatdate(timeval=None, localtime=False, usegmt=True)
    request_string = f'{method},application/json,{content_md5},{request_path},{date}'
    signature = compute_hmac(SECRET_KEY, request_string)
    authorization = f'APIAuth {ACCESS_KEY}:{signature}'

    headers = {
        'Content-Type': 'application/json',
        'Content-MD5': content_md5,
        'Date': date,
        'Authorization': authorization
    }
    return headers



def get_coin_accounts(coin_currency, coin_layer):
    api_endpoint = 'https://api.remitano.com/api/v1/coin_accounts/me'
    method = 'GET'
    request_path = f'/api/v1/coin_accounts/me?coin_currency={coin_currency}&coin_layer={coin_layer}'

    headers = get_headers(method, request_path)

    response = requests.get(api_endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return None

# Example usage
# coin_accounts = get_coin_accounts('btc', '')
# if coin_accounts:
#     print(coin_accounts)

def get_currencies():
    api_endpoint = 'https://api.remitano.com/api/v1/currencies/info'
    method = 'GET'
    request_path = f'/api/v1/currencies/info'

    headers = get_headers(method, request_path)

    response = requests.get(api_endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return None
    


def api_request(method, endpoint, params=None, data=None):
    request_path = endpoint
    if params:
        query_string = '&'.join([f'{key}={value}' for key, value in params.items()])
        request_path = f'{endpoint}?{query_string}'
    url = f'{BASE_URL}{request_path}'
    body = data if data else ''
    headers = get_headers(method.upper(), request_path, body)

    response = requests.request(method, url, headers=headers, params=params, json=data)
    if response.status_code in range(200, 300):
        return response.json()
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return None

# Example usage
# Replace 'YOUR_ACCESS_KEY' and 'YOUR_SECRET_KEY' with your actual API credentials
# Example: GET request to fetch coin accounts
response = api_request('GET', '/api/v1/coin_accounts/me', params={'coin_currency': 'btc'})
# response = api_request('GET', '/api/v1/currencies/info')
# response = api_request('GET', '/api/v1/my_payment_methods/create', params={'fiat_currency': '', 'country_code': '', 'payment_method_id': ''})
if response:
    print(response)


# def testing(something: list[str]):
#     for l in something:
#         print(l.capitalize())

# testing(['abe', 'cat', 'dog'])