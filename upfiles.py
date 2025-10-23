import argparse
import os
import requests
import json

def post(name, body_md, team_name, token, category='pukiwiki/test', tags=['pukiwiki'],
         wip=False, message='auto update by upfiles.py', verbose=False):
    url = f'https://api.esa.io/v1/teams/{team_name}/posts'

    params = {
        "access_token": token
    }

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "post": {
            "name": name,
            "body_md": body_md,
            "tags": tags,
            "category": category,
            "wip": wip,
            "message": message,
        },
    }

    try:
        response = requests.post(url, params=params, headers=headers, json=payload)

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

def post_tree(source_dir, team_name, token, prefix='', verbose=False, simulation=False):
    """
    Args:
        source_dir (str): コピー元のディレクトリパス。
    """
    if not os.path.isdir(source_dir):
        raise FileNotFoundError(f"エラー: コピー元ディレクトリ '{source_dir}' が見つかりません。")

    for src_dirpath, src_dirnames, src_filenames in os.walk(source_dir):
        if src_dirpath == source_dir:
            relative_path = ""
        else:
            relative_path = os.path.relpath(src_dirpath, source_dir)

        for fname in src_filenames:
            # print("a: ", fname)
            name = fname.split('.')[0]
            src_file_path = os.path.join(src_dirpath, fname)
            with open(src_file_path) as f:
                body = f.read()
                if not simulation:
                    post(name, body, team_name, token, category=prefix, verbose=verbose)
                else:
                    print(f'post({name}, {body}, {team_name}, {token}, verbose={verbose})')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_directory", type=str, required=True)
    parser.add_argument("-n", "--team_name", type=str, required=True)
    parser.add_argument("-t", "--token", type=str, required=True)
    parser.add_argument("-p", "--prefix", type=str, default='pukiwiki/')
    parser.add_argument("-v", "--verbose", action='store_true')
    parser.add_argument("-s", "--simulation", action='store_true')

    args = parser.parse_args()

    post_tree(args.input_directory, args.team_name, args.token, prefix=args.prefix, verbose=args.verbose, simulation=args.simulation)
