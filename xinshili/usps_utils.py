import requests


def test():
    url = 'http://xyl.weibone.com/member/api/track'
    pd = {
        'apikey': 'ak_bc6f10b8e85a4fe1867c61c644128b05',
        'track_numbers': ['9400136208265766176863']
    }
    resp = requests.post(
        url=url,
        json=pd
    )
    print(resp.json())


test()
