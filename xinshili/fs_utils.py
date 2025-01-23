import requests
import json

app_id = "cli_a71b49e8b4aad013"
app_secret = "7L9WNS6YWwQNVUN3iEtQKgb8BoQSJRzn"


def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    # 应用凭证里的 app id 和 app secret
    post_data = {"app_id": app_id, "app_secret": app_secret}
    r = requests.post(url, data=post_data)
    tat = r.json()["tenant_access_token"]  # token
    print(f"token:{tat}")
    return tat


def detail_sheet_value(tat, lists, ck_time):
    """
    写入数据到 飞书 zbw轨迹跟踪2025.1 表的 详sheet
    """
    # values_prepend:它会在指定位置上方新增一行，而不是直接覆盖现有数据; values:若指定范围内已有数据，将被新写入的数据覆盖。
    # BGrnsxMFfhfoumtUDF8cXM8jnGg：表格地址中?前面的部分，表示该文档
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/BGrnsxMFfhfoumtUDF8cXM8jnGg/values"
    header = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(tat)}  # 请求头
    # JZrQj9：表格地址中 ?sheet= 后面的部分，表示表的名字
    # 因为首行是行头，所以表格中的出库时间所在行为：出库时间+1
    map_sheet_ck_time = str(int(ck_time) + 1)
    post_data = {"valueRange": {"range": f"JZrQj9!B{map_sheet_ck_time}:K{map_sheet_ck_time}", "values": [lists]}}
    # values_prepend 需要使用post请求方式，values需要使用put请求方式
    r2 = requests.put(url, data=json.dumps(post_data), headers=header)  # 请求写入
    print(r2.json())  # 输出来判断写入是否成功
