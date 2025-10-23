import argparse
import os
import requests
import json

def get_post(team_name, token, verbose=False):
    url = f'https://api.esa.io/v1/teams/{team_name}/posts'

    params = {
        "access_token": token
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        # ステータスコードが200番台でない場合 (エラーが発生した場合) に例外を発生させる
        response.raise_for_status()

        print(f"req success: {response.status_code}")

        if verbose:
            # response.json() はレスポンスボディを辞書に変換する
            print("\nresponse")
            # json.dumpsを使って、見やすくインデントして表示
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        # ネットワークエラーやHTTPエラーステータスコードなど、リクエストに関するエラーを捕捉
        print(f"errors in request: {e}")
        # エラーレスポンスの内容を表示する場合
        if 'response' in locals() and response is not None:
            print(f"status: {response.status_code}")
            print(f"response: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--team_name", type=str, required=True)
    parser.add_argument("-t", "--token", type=str, required=True)
    parser.add_argument("-v", "--verbose", action='store_true')

    args = parser.parse_args()

    get_post(args.team_name, args.token, verbose=args.verbose)
