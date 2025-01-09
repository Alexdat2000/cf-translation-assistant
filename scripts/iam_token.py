import time
import jwt
import json

import requests

def renew():
    with open('../credentials/key.json', 'r') as f:
        obj = f.read()
        obj = json.loads(obj)
        private_key = obj['private_key']
        key_id = obj['id']
        service_account_id = obj['service_account_id']

    now = int(time.time())
    payload = {
        'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
        'iss': service_account_id,
        'iat': now,
        'exp': now + 3600
    }

    # JWT generation.
    encoded_token = jwt.encode(
        payload,
        private_key,
        algorithm='PS256',
        headers={'kid': key_id}
    )

    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'jwt': encoded_token,
    }

    response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', headers=headers, json=json_data)
    print(response.json()["iamToken"], file=open("../credentials/token.txt", "w"))
