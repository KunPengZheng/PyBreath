import geoip2.database
import socks
import socket
import requests
from contextlib import contextmanager


# ============ 1. IP 代理格式处理 ============= #
def parse_proxy_line(proxy_line):
    # 解析格式：ip:port:user:pass
    parts = proxy_line.strip().split(":")
    if len(parts) != 4:
        raise ValueError("代理格式应为 ip:port:user:pass")
    ip, port, user, pwd = parts
    return {
        "ip": ip,
        "port": int(port),
        "username": user,
        "password": pwd,
        "proxy_string": f"{user}:{pwd}@{ip}:{port}"
    }


# ============ 2. 设置 SOCKS5 代理上下文 ============= #
@contextmanager
def set_socks_proxy(proxy_info):
    original_socket = socket.socket
    socks.set_default_proxy(
        socks.SOCKS5,
        proxy_info["ip"],
        proxy_info["port"],
        username=proxy_info["username"],
        password=proxy_info["password"]
    )
    socket.socket = socks.socksocket
    try:
        yield
    finally:
        socket.socket = original_socket


# ============ 3. 获取 IP 地理位置 ============= #
def get_location_by_ip(ip, db_path="/Users/zkp/Downloads/GeoLite2-City.mmdb"):
    try:
        with geoip2.database.Reader(db_path) as reader:
            response = reader.city(ip)
            country = response.country.name or "未知国家"
            subdivision = response.subdivisions.most_specific.name or "未知州/省"
            city = response.city.name or "未知城市"
            return country, subdivision, city
    except Exception as e:
        return f"查询失败: {e}", None, None


# ============ 4. 测试代理可用性 ============= #
def test_proxy(proxy_string, proxy_type="socks5"):
    proxies = {
        "http": f"{proxy_type}://{proxy_string}",
        "https": f"{proxy_type}://{proxy_string}"
    }
    try:
        resp = requests.get("https://api.ipify.org", proxies=proxies, timeout=8)
        print(f"\t✅ {proxy_type.upper()} 代理可用，IP 为：{resp.text}")
        return True
    except Exception as e:
        print(f"\t❌ {proxy_type.upper()} 代理失败: {e}")
        return False


# ============ 5. 主程序 ============= #
if __name__ == "__main__":
    proxy_lines = [
        "31.59.18.165:6746:rodkjbxe:7ec907jvbgyv",
        "192.177.103.167:6660:rodkjbxe:7ec907jvbgyv",
        "50.114.98.133:5617:rodkjbxe:7ec907jvbgyv",
        "38.153.133.85:9489:rodkjbxe:7ec907jvbgyv",
        "142.147.128.227:6727:rodkjbxe:7ec907jvbgyv",
        "23.27.196.104:6473:rodkjbxe:7ec907jvbgyv",
        "173.0.9.121:5704:rodkjbxe:7ec907jvbgyv",
        "92.113.3.133:6142:rodkjbxe:7ec907jvbgyv",
        "136.0.105.98:6108:rodkjbxe:7ec907jvbgyv",
        "191.101.41.178:6250:rodkjbxe:7ec907jvbgyv",
        "136.0.117.8:6746:rodkjbxe:7ec907jvbgyv",
    ]

    for line in proxy_lines:
        print(f"\n================= 🚀 代理测试: {line} =================")
        try:
            proxy = parse_proxy_line(line)
            ip = proxy["ip"]
            proxy_string = proxy["proxy_string"]

            print(f"🌍 查询 IP {ip} 的地理位置...")
            country, subdivision, city = get_location_by_ip(ip)
            print(f"\t📍 国家: {country}")
            print(f"\t📍 州/省: {subdivision}")
            print(f"\t📍 城市: {city}")

            print("")
            print(f"🌐 测试代理可用性 ({proxy_string})")
            test_proxy(proxy_string, proxy_type="socks5")
            test_proxy(proxy_string, proxy_type="http")
        except Exception as e:
            print(f"⚠️ 处理失败: {e}")
