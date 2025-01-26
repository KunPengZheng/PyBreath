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
    print(data_str)

    return data_str
