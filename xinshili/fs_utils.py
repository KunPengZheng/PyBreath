import requests

url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
app_id = "cli_a71b49e8b4aad013"
app_secret = "7L9WNS6YWwQNVUN3iEtQKgb8BoQSJRzn"


def get_token():
    # 应用凭证里的 app id 和 app secret
    post_data = {"app_id": app_id, "app_secret": app_secret}
    r = requests.post(url, data=post_data)
    tat = r.json()["tenant_access_token"]  # token
    print(f"token:{tat}")
    return tat
