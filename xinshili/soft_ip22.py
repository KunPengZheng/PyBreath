import requests

# 1. 要查询的 IP 列表，最多 100 个
ips = [
    {"query": "142.147.128.227", "fields": "city,country,countryCode,query,regionName", "lang": "zh"}
]

# 2. ip-api 的 batch 请求 URL
url = "http://ip-api.com/batch"

# 3. 发起 POST 请求
response = requests.post(url, json=ips)

# 4. 解析并输出结果
if response.status_code == 200:
    results = response.json()
    print(results)
    for item in results:
        ip = item.get("query")
        city = item.get("city", "未知城市")
        country = item.get("country", "未知国家")
        print(f"{ip} is in {city}, {country}")
else:
    print(f"请求失败，状态码: {response.status_code}")
