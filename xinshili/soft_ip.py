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
        "password": pwd
    }


# ============ 2. 设置 SOCKS5 代理上下文 ============= #
@contextmanager
def set_socks_proxy(proxy_info):
    # ✅ 保存原始 socket
    original_socket = socket.socket

    socks.set_default_proxy(
        socks.SOCKS5,
        proxy_info["ip"],
        proxy_info["port"],
        username=proxy_info["username"],
        password=proxy_info["password"]
    )

    # ✅ 设置 socks 代理
    socket.socket = socks.socksocket
    try:
        yield
    finally:
        # ✅ 还原原始 socket
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


def test_proxy(proxy, proxy_type="socks5"):
    proxies = {
        "http": f"{proxy_type}://{proxy}",
        "https": f"{proxy_type}://{proxy}"
    }
    try:
        resp = requests.get("https://api.ipify.org", proxies=proxies, timeout=8)
        print(f"✅ {proxy_type.upper()} 代理可用，IP 为：{resp.text}")
    except Exception as e:
        print(f"❌ {proxy_type.upper()} 代理失败: {e}")


# ============ 5. 主程序 ============= #
if __name__ == "__main__":
    proxy_line = "107.173.93.174:6128:gpjgjuez:bxg8ru2lx942"
    proxy = parse_proxy_line(proxy_line)

    # 获取国家
    print(f"🌍 正在查询 IP {proxy['ip']} 所属国家...")
    country, subdivision, city = get_location_by_ip(proxy["ip"])
    print(f"📍 国家: {country}")
    print(f"📍 州/省: {subdivision}")
    print(f"📍 城市: {city}")

    proxy = "gpjgjuez:bxg8ru2lx942@107.173.93.174:6128"
    # test_proxy(proxy, proxy_type="http")
    test_proxy(proxy, proxy_type="socks5")
