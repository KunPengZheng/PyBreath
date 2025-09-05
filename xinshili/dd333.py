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
            'pc_user_key=8ff6a46a8cc289a592f7d867a6520d5c;'  # ⚠️ 
            'xenbyfpfUnhLsdkZbX=0;'
            'shop_version_type=8;'
            'show_user_icon=1;'
            'LANGUAGE_appfte6oc8n4154=cn;'
            'sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%22198b210de2a9e6-06cff2f94585198-16525636-1484784-198b210de2b1704%22%7D;'
            'appId="appfte6oc8n4154";'
            'userInfo={"app_id":"appfte6oc8n4154","birth":null,"can_modify_phone":true,"universal_union_id":null,"user_id":"u_6888a238a49c6_EFVgSkIV5z","wx_account":"","wx_avatar":"http://commonresource-1252524126.cdn.xiaoeknow.com/image/default.svg","wx_gender":0,"phone":"13923003003","pc_user_key":"8ff6a46a8cc289a592f7d867a6520d5c","permission_visit":0,"permission_comment":0,"permission_buy":0,"pwd_isset":true,"channels":[{"type":"wechat","active":0},{"type":"qq","active":0}],"area_code":"86"}'
        )
    }

    payload = {
        "org_app_id": "",
        "app_id": "appfte6oc8n4154",  # ⚠️
        "user_id": "u_6888a238a49c6_EFVgSkIV5z",  # ⚠️
        "play_sign": [
            "fBXFiMQdEhbgtEtHBmPRYDPysNDyRGJxtm2OiLIW-lbRmYVxwNmbG1zUxMsyJXsXHmGeimdxjoGQXYaF9AskJbWSuNLe7Fc3GbsmSDO-NBc"
            # ⚠️
        ],
        "play_line": "A",
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


def download_m3u8(host, path, param, ts, ts_folder, cipher):
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
    enc_data = resp.content
    # 确保数据长度是 16 的倍数（去掉 padding 不完整的部分）
    enc_data = enc_data[:len(enc_data) - (len(enc_data) % 16)]
    # 解密
    result_data = cipher.decrypt(enc_data)
    with open(f"{ts_folder}{ts.rstrip('?')}", "wb") as f:
        f.write(result_data)


def extract_ts_files(text):
    # 匹配所有形如 xxx.ts? 的文件名
    ts_files = re.findall(r'(\S+?\.ts\?)', text)
    return ts_files


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


def merge_ts_files(folder, output_file):
    # 找到所有 .ts 文件，并按文件名排序
    ts_files = sorted([f for f in os.listdir(folder) if f.endswith(".ts")])

    if not ts_files:
        print("❌ 没有找到 .ts 文件")
        return

    # 写入 file_list.txt 供 ffmpeg 使用
    list_file = os.path.join(folder, "file_list.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for ts in ts_files:
            f.write(f"file '{os.path.join(folder, ts)}'\n")

    # 调用 ffmpeg 合并
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        output_file
    ]

    subprocess.run(cmd, check=True)
    print(f"✅ 合并完成: {output_file}")


if __name__ == '__main__':
    # # 使用方法
    result = get_play_url()
    # print(result)

    first_key = next(iter(result["data"]))
    play_url = result["data"][first_key]["play_list"]["720p_hls"]["play_url"]
    ext = result["data"][first_key]["play_list"]["720p_hls"]["ext"]
    host = ext["host"]
    path = ext["path"]
    param = ext["param"]
    # print(host)

    m3u8_text = get_m3u8_content(play_url)
    if m3u8_text:
        # print(f"✅ {m3u8_text}")

        ts_files = extract_ts_files(m3u8_text)
        # 提取URI
        uri_match = re.search(r'URI="([^"]+)"', m3u8_text)
        uri = uri_match.group(1) if uri_match else None
        # 提取IV
        iv_match = re.search(r'IV=0x([0-9a-fA-F]+)', m3u8_text)
        iv_hex = iv_match.group(1) if iv_match else None
        iv = bytes.fromhex(iv_hex)

        key_url = f"{uri}&uid=u_6888a238a49c6_EFVgSkIV5z"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "Referer": "https://appfte6oc8n4154.xet-pc.citv.cn/",
        }
        resp = requests.get(key_url, headers=headers)
        key = resp.content  # 返回的就是原始 key（二进制）
        cipher = AES.new(key, AES.MODE_CBC, iv)

        ts_folder = "/Users/zkp/Downloads/未命名文件夹 2/"
        for i in ts_files:
            download_m3u8(host, path, param, i, ts_folder, cipher)

        merge_ts_files(ts_folder, "/Users/zkp/Downloads/output.mp4")
