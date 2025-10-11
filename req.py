import requests
import json

# 送信先URL
url = 'http://localhost:8080/api/v1/convert' # <url>の部分を実際のエンドポイントに置き換えてください

# 送信するデータ
#payload = {
#    "body": "*Header1\n**Header2\n"
#}

def convert(instr):
    payload = {}
    payload['body'] = instr
    # POSTリクエストを送信
    # json引数を使うと、自動的にデータがJSON形式に変換され、
    # ヘッダーのContent-Typeも'application/json'に設定されます。
    response = requests.post(url, json=payload)

    # レスポンスのステータスコードを出力
    print(f"Status Code: {response.status_code}")

    # レスポンスのボディを出力
    print(f"Response Body: {response.text}")

    if response.status_code == 200:
        res = json.loads(response.text)
        print(res['body'])
        return res['body']

convert( "*Header1\n**Header2\n" )

with open('/home/irsl/wiki/HSR.txt') as f:
    convert(f.read())

# https://github.com/kaishuu0123/pukiwiki2markdown.git
