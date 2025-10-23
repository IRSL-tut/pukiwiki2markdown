import os
import shutil
import urllib.parse
import argparse

def try_decode(_encoded_str):
    encoded_str = urllib.parse.unquote(_encoded_str)
    if encoded_str != _encoded_str:
        return _encoded_str
    #print('en: ', _encoded_str, encoded_str)
    try:
        encoded_bytes = bytes.fromhex(encoded_str)
    except Exception:
        return encoded_str
    ##
    try:
        return encoded_bytes.decode('euc_jp')
    except UnicodeDecodeError:
        pass
    ##
    try:
        return encoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        pass
    ##
    return encoded_str

def _my_decode_impl(instr):
    if len(instr) <= 0:
        return instr
    out = try_decode(instr)
    #print('impl: ', out)
    return out

def my_decode(instr):
    res = [ _my_decode_impl(a) for a in instr.split('.') ]
    #print('in : ', instr)
    res = '.'.join(res)
    #print('out ', res)
    return res

def copy_and_decode_tree(source_dir, destination_dir, verbose=False, simulation=False):
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

        # --- 2. ディレクトリツリーを再帰的に走査 ---
        # os.walkは、指定したディレクトリ以下の全てのディレクトリとファイルを探索する
        for src_dirpath, src_dirnames, src_filenames in os.walk(source_dir):

            # --- 3. コピー先のパスを計算 ---
            # コピー元ルートからの相対パスを計算し、各階層名をデコードする
            # 例: src_dirpath が "directory_A/folder%20name" の場合...
            #   1. relpath -> "folder%20name"
            #   2. split(os.sep) -> ["folder%20name"]
            #   3. unquote -> ["folder name"]
            #   4. join -> "folder name"
            #   5. dest_dirpath -> "directory_B/folder name"
            if src_dirpath == source_dir:
                relative_path = ""
            else:
                relative_path = os.path.relpath(src_dirpath, source_dir)

            # decoded_parts = [urllib.parse.unquote(part) for part in relative_path.split(os.sep)]
            decoded_parts = [ my_decode(part) for part in relative_path.split(os.sep)]

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
                # ファイル名をデコード
                filename_decoded = my_decode(filename_encoded)

                # コピー元（エンコードされた名前）とコピー先（デコードされた名前）のフルパスを作成
                src_file_path = os.path.join(src_dirpath, filename_encoded)
                dest_file_path = os.path.join(dest_dirpath, filename_decoded)

                if '/' in filename_decoded:
                    if verbose:
                        print(f"  skip: {src_file_path} -> {dest_file_path}")
                    continue

                # ファイルをコピー
                if not simulation:
                    shutil.copy2(src_file_path, dest_file_path)
                if verbose:
                    print(f"  copy: {src_file_path} -> {dest_file_path}")
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

    args = parser.parse_args()

    copy_and_decode_tree(args.input_directory, args.output_directory,
                         verbose=args.verbose, simulation=args.simulation)
