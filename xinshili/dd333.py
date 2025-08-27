import requests
import os
import requests
import m3u8
import subprocess
import re
from Crypto.Cipher import AES
from urllib.parse import urljoin


def get_play_url():
    url = "https://appfte6oc8n4154.xet-pc.citv.cn/xe.material-center.play/getPlayUrl"  # ⚠️

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Origin": "https://appfte6oc8n4154.xet-pc.citv.cn",  # ⚠️
        "Referer": "https://appfte6oc8n4154.xet-pc.citv.cn/p/t_pc/course_pc_detail/video/v_66542759e4b0d84daad6bd83?content_app_id=&product_id=p_6653f639e4b0694c9816ce93&type=6",
        # ⚠️
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Sec-CH-UA": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"macOS"',
        # ⚠️ 如果需要，可以手动设置 cookie，或使用登录后 session 来管理
        "Cookie": (
            'pc_user_key=950af0b9efe281c240b2fd14ff82b93a; '  # ⚠️ 
            'xenbyfpfUnhLsdkZbX=0; '
            'shop_version_type=8; '
            'show_user_icon=1; '
            'LANGUAGE_appfte6oc8n4154=cn; '
            'sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%221987934099b11e4-07adacc35dc2e08-17525636-1440000-1987934099c14ca%22%7D; '
            'appId="appfte6oc8n4154"; '
            'userInfo={"app_id":"appfte6oc8n4154","user_id":"u_6888a238a49c6_EFVgSkIV5z","phone":"13923003003"}'
        )
    }

    payload = {
        "org_app_id": "",
        "app_id": "appfte6oc8n4154",  # ⚠️
        "user_id": "u_6888a238a49c6_EFVgSkIV5z",  # ⚠️
        "play_sign": [
            "fBXFiMQdEhbgtEtHBmPRYDPysNDyRGJxtm2OiLIW-lZ4cpBl5J-OlHOvgaz4zXqtk0pzSl84YXb67l9Nl88Km1lYWvGFLxm__bl1epttAVM"
            # ⚠️
        ],
        "play_line": "C",
        "opr_sys": "MacIntel"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()  # 返回 JSON 结果
    except requests.RequestException as e:
        print("请求失败:", e)
        return None


def get_m3u8_content(m3u8_url: str) -> str:
    """
    发送 GET 请求获取 m3u8 文件内容

    :param m3u8_url: m3u8 文件的完整 URL
    :return: 返回 m3u8 内容文本（如果成功），否则返回 None
    """

    headers = {
        "Host": "pri-cdn-tx.xiaoeknow.com",
        "Sec-CH-UA-Platform": '"macOS"',
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Sec-CH-UA": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "Sec-CH-UA-Mobile": "?0",
        "Accept": "*/*",
        "Origin": "https://appfte6oc8n4154.xet-pc.citv.cn",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://appfte6oc8n4154.xet-pc.citv.cn/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
    }

    try:
        response = requests.get(m3u8_url, headers=headers)
        response.raise_for_status()
        return response.text  # 返回 M3U8 的原始内容
    except requests.RequestException as e:
        print("❌ 请求失败:", e)
        return None


def download_encrypted_m3u8_video(m3u8_url, output_dir, output_file):
    os.makedirs(output_dir, exist_ok=True)

    headers = {
        "Host": "vth-vod.h5.xed.plus",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "\"macOS\"",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "Accept": "*/*",
        "Origin": "https://appfte6oc8n4154.xet-pc.citv.cn",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://appfte6oc8n4154.xet-pc.citv.cn/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        # "Cookie": "如果有的话"
    }

    # 1. 获取 m3u8 内容
    print("📥 正在下载 m3u8 文件...")
    resp = requests.get(m3u8_url, headers=headers)
    resp.raise_for_status()
    m3u8_obj = m3u8.loads(resp.text)

    # 2. 拼接 ts 地址并下载
    base_url = m3u8_url.rsplit('/', 1)[0] + '/'
    ts_files = []
    print(f"🎬 共找到 {len(m3u8_obj.segments)} 个 ts 片段，开始下载...")

    for i, segment in enumerate(m3u8_obj.segments):
        ts_url = urljoin(base_url, segment.uri)
        ts_path = os.path.join(output_dir, f"{i:05}.ts")
        ts_files.append(ts_path)

        if os.path.exists(ts_path):
            print(f"✅ 跳过已存在: {ts_path}")
            continue

        try:
            r = requests.get(ts_url, headers=headers, stream=True)
            r.raise_for_status()
            with open(ts_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ 下载成功: {ts_path}")
        except Exception as e:
            print(f"❌ 下载失败: {ts_url} - {e}")

    # 3. 生成合并文件列表
    file_list_path = os.path.join(output_dir, "file_list.txt")
    with open(file_list_path, "w") as f:
        for ts_file in ts_files:
            f.write(f"file '{ts_file}'\n")

    # 4. 使用 ffmpeg 合并 ts 文件
    print("📦 开始合并视频...")
    cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", file_list_path,
        "-c", "copy",
        output_file
    ]
    subprocess.run(cmd, check=True)
    print(f"🎉 视频已保存为: {output_file}")


def download_m3u8(host, path, param, ts, ts_folder):
    url = f"{host}/{path}/{ts}&{param}"
    headers = {
        "Host": "vth-vod.h5.xed.plus",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "\"macOS\"",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "Accept": "*/*",
        "Origin": "https://appfte6oc8n4154.xet-pc.citv.cn",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://appfte6oc8n4154.xet-pc.citv.cn/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
    }
    resp = requests.get(url, headers=headers)
    with open(f"{ts_folder}{ts.rstrip('?')}", "wb") as f:
        f.write(resp.content)


def extract_ts_files(text):
    # 匹配所有形如 xxx.ts? 的文件名
    ts_files = re.findall(r'(\S+?\.ts\?)', text)
    return ts_files


def merge_ts_files(folder_path, merged_ts_path):
    ts_files = [f for f in os.listdir(folder_path) if f.endswith('.ts')]
    ts_files.sort()
    with open(merged_ts_path, 'wb') as outfile:
        for ts_file in ts_files:
            file_path = os.path.join(folder_path, ts_file)
            print(f"Merging {file_path} ...")
            with open(file_path, 'rb') as infile:
                outfile.write(infile.read())
    print(f"Merged .ts file saved as {merged_ts_path}")


def convert_ts_to_mp4(ts_path, mp4_path):
    cmd = [
        'ffmpeg',
        '-y',  # 覆盖输出文件
        '-i', ts_path,
        '-c', 'copy',
        mp4_path
    ]
    print("Converting to mp4...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print(f"Conversion successful: {mp4_path}")
    else:
        print("Conversion failed!")
        print(result.stderr.decode())


def download_key(key_url, headers=None):
    resp = requests.get(key_url, headers=headers)
    resp.raise_for_status()
    return resp.content  # 16字节密钥


def decrypt_ts(ts_path, key, iv):
    with open(ts_path, 'rb') as f:
        encrypted_data = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data


def save_decrypted_ts(decrypted_data, save_path):
    with open(save_path, 'wb') as f:
        f.write(decrypted_data)


def decode(uri, iv):
    # 你自己的配置
    key_url = uri
    ts_folder = '/Users/zkp/Downloads/未命名文件夹 2/'  # 已下载加密ts文件夹
    decrypted_folder = '/Users/zkp/Downloads/未命名文件夹 2/decrypted_ts'
    os.makedirs(decrypted_folder, exist_ok=True)

    # 下载密钥
    key = download_key(key_url)
    print(f"Key: {key.hex()}")

    iv_str = iv  # 这个是从m3u8里提取的原始字符串

    # 去掉开头的 '0x' 或 '0X'
    if iv_str.lower().startswith("0x"):
        iv_hex = iv_str[2:]
    else:
        iv_hex = iv_str

    # 把16进制字符串转成bytes
    iv = bytes.fromhex(iv_hex)

    print(f"IV (hex): {iv.hex()}")
    print(f"IV (bytes): {iv}")

    # 解密所有ts
    ts_files = sorted([f for f in os.listdir(ts_folder) if f.endswith('.ts')],
                      key=lambda x: int(x.split('_')[-1].split('.')[0]))
    for ts_file in ts_files:
        encrypted_path = os.path.join(ts_folder, ts_file)
        decrypted_path = os.path.join(decrypted_folder, ts_file)
        decrypted_data = decrypt_ts(encrypted_path, key, iv)
        save_decrypted_ts(decrypted_data, decrypted_path)
        print(f"Decrypted {ts_file}")

    print("所有ts解密完成，下一步用ffmpeg合并decrypted_ts文件夹里的文件")


def merge_ts_files_ffmpeg(decrypted_folder, output_file):
    # 生成 filelist.txt，格式是：
    # file 'path/to/file1.ts'
    # file 'path/to/file2.ts'
    filelist_path = os.path.join(decrypted_folder, 'filelist.txt')
    with open(filelist_path, 'w', encoding='utf-8') as f:
        # 按文件名排序（确保顺序）
        ts_files = sorted([fn for fn in os.listdir(decrypted_folder) if fn.endswith('.ts')],
                          key=lambda x: int(''.join(filter(str.isdigit, x))))
        for ts_file in ts_files:
            full_path = os.path.abspath(os.path.join(decrypted_folder, ts_file))
            f.write(f"file '{full_path}'\n")

    # 调用ffmpeg合并
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', filelist_path,
        '-c', 'copy',
        output_file
    ]
    print("Running ffmpeg merge command...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Merge successful! Output file: {output_file}")
    else:
        print("Merge failed!")
        print(result.stderr)


if __name__ == '__main__':
    # # 使用方法
    result = get_play_url()
    print(result)

    first_key = next(iter(result["data"]))
    play_url = result["data"][first_key]["play_list"]["720p_hls"]["play_url"]
    ext = result["data"][first_key]["play_list"]["720p_hls"]["ext"]
    host = ext["host"]
    path = ext["path"]
    param = ext["param"]
    # print(host)

    m3u8_text = get_m3u8_content(play_url)
    if m3u8_text:
        print(f"✅ {m3u8_text}")

        ts_files = extract_ts_files(m3u8_text)
        # 提取URI
        uri_match = re.search(r'URI="([^"]+)"', m3u8_text)
        uri = uri_match.group(1) if uri_match else None
        # 提取IV
        iv_match = re.search(r'IV=0x([0-9a-fA-F]+)', m3u8_text)
        iv = iv_match.group(1) if iv_match else None

        # print("ts_files:", ts_files)
        print("URI:", uri)
        print("IV:", iv)

        # ts_folder = "/Users/zkp/Downloads/未命名文件夹 2/"
        # for i in ts_files:
        #     download_m3u8(host, path, param, i, ts_folder)

        # merged_ts = "/Users/zkp/Downloads/未命名文件夹 2/merged.ts"  # 合并后的ts文件名
        # output_mp4 = "/Users/zkp/Downloads/未命名文件夹 2/output_video.mp4"  # 输出的mp4文件名
        # merge_ts_files(ts_folder, merged_ts)
        # convert_ts_to_mp4(merged_ts, output_mp4)

        decode(uri, iv)
        decrypted_folder = '/Users/zkp/Downloads/未命名文件夹 2/decrypted_ts/'  # 你的解密ts文件夹
        output_file = '/Users/zkp/Downloads/final_video.mp4'  # 合并后的视频文件名
        merge_ts_files_ffmpeg(decrypted_folder, output_file)

