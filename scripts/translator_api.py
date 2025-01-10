import csv
from itertools import chain

import requests
import iam_token


def send_request_raw(texts):
    body = {
        "sourceLanguageCode": "en",
        "targetLanguageCode": "ru",
        "format": "HTML",
        "texts": texts,
        "folderId": "b1ggaq6jpqb36qfjg8k4",
        "glossaryConfig": {
            "glossaryData": {
                "glossaryPairs": [
                    {
                        "sourceText": a,
                        "translatedText": b,
                    }
                    for a, b in chain(
                        csv.reader(open("../glossaries/main.csv", encoding="utf-8"), delimiter=";"),
                        csv.reader(open("../glossaries/temp.csv", encoding="utf-8"), delimiter=";"),
                    )
                ]
            }
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {open("../credentials/token.txt").read().strip()}"
    }
    return requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                         json=body,
                         headers=headers
                         ).json()


def send_request(texts):
    response = send_request_raw(texts)
    if 'translations' in response:
        return response['translations'][0]['text']
    iam_token.renew()
    return send_request_raw(texts)['translations'][0]['text']
