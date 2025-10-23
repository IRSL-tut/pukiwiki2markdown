import argparse
import os
import requests
import json
from markdownify import markdownify as md

# 送信先URL
url = 'http://localhost:8080/api/v1/convert'

def convert(instr, verbose=False):
    payload = {}
    payload['body'] = instr
    # POSTリクエストを送信
    # json引数を使うと、自動的にデータがJSON形式に変換され、
    # ヘッダーのContent-Typeも'application/json'に設定されます。
    response = requests.post(url, json=payload)

    # レスポンスのステータスコードを出力
    ## print(f"Status Code: {response.status_code}")

    # レスポンスのボディを出力
    ## print(f"Response Body: {response.text}")

    if response.status_code == 200:
        res = json.loads(response.text)
        if verbose:
            print(res['body'])
        return res['body']

def copy_and_decode_tree(source_dir, destination_dir, verbose=False, simulation=False, useMarkdownify=True):
    """
    ディレクトリを再帰的にコピーし、ファイル名とディレクトリ名をデコードする。

    Args:
        source_dir (str): コピー元のディレクトリパス。
        destination_dir (str): コピー先のディレクトリパス。
    """
    try:
        if not os.path.isdir(source_dir):
            raise FileNotFoundError(f"エラー: コピー元ディレクトリ '{source_dir}' が見つかりません。")

        if os.path.exists(destination_dir):
            raise FileExistsError(f"エラー: コピー先ディレクトリ '{destination_dir}' は既に存在します。")

        for src_dirpath, src_dirnames, src_filenames in os.walk(source_dir):

            if src_dirpath == source_dir:
                relative_path = ""
            else:
                relative_path = os.path.relpath(src_dirpath, source_dir)

            decoded_parts = relative_path.split(os.sep)

            # 先頭の要素が '.' の場合は空文字列に変換する
            if decoded_parts and decoded_parts[0] == '.':
                decoded_parts = []

            decoded_relative_path = os.path.join(*decoded_parts) if decoded_parts else ""
            dest_dirpath = os.path.join(destination_dir, decoded_relative_path)

            # デコードされた名前でコピー先にディレクトリを作成 (空のディレクトリもコピーするため)
            if not os.path.exists(dest_dirpath):
                if not simulation:
                    os.makedirs(dest_dirpath)

            # --- 4. ファイルをコピー ---
            for filename_encoded in src_filenames:
                filename_decoded = filename_encoded

                # コピー元（エンコードされた名前）とコピー先（デコードされた名前）のフルパスを作成
                src_file_path = os.path.join(src_dirpath, filename_encoded)
                dest_file_path = os.path.join(dest_dirpath, filename_decoded)
                dest_file_path = dest_file_path.replace('.txt', '.md')

                with open(src_file_path) as f:
                    res = convert(f.read(), verbose=verbose)
                    if res is not None:
                        if not simulation:
                            with open(dest_file_path, 'w') as wf:
                                if useMarkdownify:
                                    try:
                                        rmd = md(res, autolinks=False)
                                        wf.write(rmd)
                                    except Exception as e:
                                        print(res)
                                        print(e)
                                else:
                                    wf.write(res)
                        if verbose:
                            print(f"  convert: {src_file_path} -> {dest_file_path}")
        if verbose:
            print("\nコピーが完了しました。")

    except FileNotFoundError as e:
        print(e)
    except FileExistsError as e:
        print(e)
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_directory", type=str, required=True)
    parser.add_argument("-o", "--output_directory", type=str, required=True)
    parser.add_argument("-v", "--verbose", action='store_true')
    parser.add_argument("-s", "--simulation", action='store_true')
    parser.add_argument("-m", "--use_markdownify", action='store_true')

    args = parser.parse_args()

    copy_and_decode_tree(args.input_directory, args.output_directory,
                         verbose=args.verbose, simulation=args.simulation, useMarkdownify=args.use_markdownify)
