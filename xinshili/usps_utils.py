import requests
import json


def track(lists):
    url = 'http://xyl.weibone.com/member/api/track'
    pd = {
        'apikey': 'ak_bc6f10b8e85a4fe1867c61c644128b05',
        'track_numbers': lists
    }
    resp = requests.post(
        url=url,
        json=pd
    )

    data_str = resp.json()

    # 替换 JSON 不合法部分
    data_str = data_str.replace("'", '"')  # 将单引号替换为双引号
    data_str = data_str.replace("True", "true").replace("False", "false")  # 转换布尔值
    data_str = data_str.replace("None", "null")  # 转换 None 为 null

    # 尝试加载为 JSON
    try:
        data = json.loads(data_str)
        print("修正后的 JSON 数据：", json.dumps(data, indent=4, ensure_ascii=False))
        return data
    except json.JSONDecodeError as e:
        print("JSON 格式错误:", e)
