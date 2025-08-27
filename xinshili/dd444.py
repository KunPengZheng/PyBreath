import subprocess

import requests
import os
import urllib.parse

from xinshili.soft_ip33 import jsons

# https://appfte6oc8n4154.pc.xiaoe-tech.com/xe.course.business.topic.items.get/2.0.0
url = {
    "code": 0,
    "msg": "success",
    "data": {
        "total": 10,
        "list": [
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "p_6653e362e4b0694c9816b365",
                "resource_type": 6,
                "resource_title": "1 、杨萃先：英语小阶-杨妈英语拼音训练营",
                "start_at": "2024.05.27",
                "img_url": "http://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "summary": "",
                "purchase_count": 0,
                "finished_state": 1,
                "resource_count": 48,
                "is_try": 0,
                "show_resource_count": True,
                "can_view": 0,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjo2LCJyZXNvdXJjZV9pZCI6InBfNjY1M2UzNjJlNGIwNjk0Yzk4MTZiMzY1IiwicHJvZHVjdF9pZCI6InBfNjY1M2YzY2JlNGIwNjk0Yzk4MTZjYjIwIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0"
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "p_6673d8a8e4b0694c982dc21e",
                "resource_type": 6,
                "resource_title": "2.1、48首必会儿歌--教学视频",
                "start_at": "2024.06.20",
                "img_url": "http://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "summary": "",
                "purchase_count": 0,
                "finished_state": 0,
                "resource_count": 50,
                "is_try": 0,
                "show_resource_count": True,
                "can_view": 0,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjo2LCJyZXNvdXJjZV9pZCI6InBfNjY3M2Q4YThlNGIwNjk0Yzk4MmRjMjFlIiwicHJvZHVjdF9pZCI6InBfNjY1M2YzY2JlNGIwNjk0Yzk4MTZjYjIwIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0"
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "p_6673dd46e4b0694c982dcbb2",
                "resource_type": 6,
                "resource_title": "2.2、48首必会儿歌-妈妈版",
                "start_at": "2024.06.20",
                "img_url": "http://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "summary": "",
                "purchase_count": 0,
                "finished_state": 0,
                "resource_count": 48,
                "is_try": 0,
                "show_resource_count": True,
                "can_view": 0,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjo2LCJyZXNvdXJjZV9pZCI6InBfNjY3M2RkNDZlNGIwNjk0Yzk4MmRjYmIyIiwicHJvZHVjdF9pZCI6InBfNjY1M2YzY2JlNGIwNjk0Yzk4MTZjYjIwIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0"
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "p_6673df5de4b0694c982dcfaf",
                "resource_type": 6,
                "resource_title": "2.3、48首必会儿歌-爸爸版",
                "start_at": "2024.06.20",
                "img_url": "http://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "summary": "",
                "purchase_count": 0,
                "finished_state": 0,
                "resource_count": 48,
                "is_try": 0,
                "show_resource_count": True,
                "can_view": 0,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjo2LCJyZXNvdXJjZV9pZCI6InBfNjY3M2RmNWRlNGIwNjk0Yzk4MmRjZmFmIiwicHJvZHVjdF9pZCI6InBfNjY1M2YzY2JlNGIwNjk0Yzk4MTZjYjIwIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0"
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "p_6673e0cde4b0694c982dd312",
                "resource_type": 6,
                "resource_title": "2.4、48首必会儿歌-儿歌故事",
                "start_at": "2024.06.20",
                "img_url": "http://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "summary": "",
                "purchase_count": 0,
                "finished_state": 0,
                "resource_count": 48,
                "is_try": 0,
                "show_resource_count": True,
                "can_view": 0,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjo2LCJyZXNvdXJjZV9pZCI6InBfNjY3M2UwY2RlNGIwNjk0Yzk4MmRkMzEyIiwicHJvZHVjdF9pZCI6InBfNjY1M2YzY2JlNGIwNjk0Yzk4MTZjYjIwIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0"
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "p_6673e1fee4b0d84daaebcc49",
                "resource_type": 6,
                "resource_title": "2.5、48首必会儿歌--合辑",
                "start_at": "2024.06.20",
                "img_url": "http://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "summary": "",
                "purchase_count": 0,
                "finished_state": 0,
                "resource_count": 48,
                "is_try": 0,
                "show_resource_count": True,
                "can_view": 0,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjo2LCJyZXNvdXJjZV9pZCI6InBfNjY3M2UxZmVlNGIwZDg0ZGFhZWJjYzQ5IiwicHJvZHVjdF9pZCI6InBfNjY1M2YzY2JlNGIwNjk0Yzk4MTZjYjIwIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0"
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "p_665443d0e4b0d84daad6f4ea",
                "resource_type": 6,
                "resource_title": "3、杨萃先：英语小阶-杨妈英语拼写记单词课",
                "start_at": "2024.05.27",
                "img_url": "http://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "summary": "",
                "purchase_count": 0,
                "finished_state": 1,
                "resource_count": 48,
                "is_try": 0,
                "show_resource_count": True,
                "can_view": 0,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjo2LCJyZXNvdXJjZV9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwicHJvZHVjdF9pZCI6InBfNjY1M2YzY2JlNGIwNjk0Yzk4MTZjYjIwIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0"
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "p_66544429e4b0694c98174953",
                "resource_type": 6,
                "resource_title": "4、杨萃先：英语小阶-杨妈英语小阶大阅读电影与指导课(节选集锦）",
                "start_at": "2024.05.27",
                "img_url": "http://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "summary": "",
                "purchase_count": 0,
                "finished_state": 1,
                "resource_count": 31,
                "is_try": 0,
                "show_resource_count": True,
                "can_view": 0,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjo2LCJyZXNvdXJjZV9pZCI6InBfNjY1NDQ0MjllNGIwNjk0Yzk4MTc0OTUzIiwicHJvZHVjdF9pZCI6InBfNjY1M2YzY2JlNGIwNjk0Yzk4MTZjYjIwIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0"
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "p_6653f639e4b0694c9816ce93",
                "resource_type": 6,
                "resource_title": "【赠送视频课程】杨萃先：瞧这一家子",
                "start_at": "2024.05.27",
                "img_url": "http://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "summary": "",
                "purchase_count": 0,
                "finished_state": 0,
                "resource_count": 101,
                "is_try": 0,
                "show_resource_count": True,
                "can_view": 0,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjo2LCJyZXNvdXJjZV9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwicHJvZHVjdF9pZCI6InBfNjY1M2YzY2JlNGIwNjk0Yzk4MTZjYjIwIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0"
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "p_665ecb65e4b0d84daade75b6",
                "resource_type": 6,
                "resource_title": "【赠送音频课程】杨萃先：瞧这一家子",
                "start_at": "2024.06.04",
                "img_url": "http://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "summary": "",
                "purchase_count": 0,
                "finished_state": 0,
                "resource_count": 111,
                "is_try": 0,
                "show_resource_count": True,
                "can_view": 0,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjo2LCJyZXNvdXJjZV9pZCI6InBfNjY1ZWNiNjVlNGIwZDg0ZGFhZGU3NWI2IiwicHJvZHVjdF9pZCI6InBfNjY1M2YzY2JlNGIwNjk0Yzk4MTZjYjIwIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0"
            }
        ]
    },
    "forward_url": ""
}

# https://appfte6oc8n4154.pc.xiaoe-tech.com/xe.course.business.column.items.get/2.0.0
url2 = {
    "code": 0,
    "msg": "success",
    "data": {
        "total": 101,
        "list": [
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542759e4b0d84daad6bd83",
                "resource_type": 3,
                "resource_title": "[1]--第1册视频-Who Is It？",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 66472,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NTllNGIwZDg0ZGFhZDZiZDgzIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 5
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_6654275be4b0d84daad6bd88",
                "resource_type": 3,
                "resource_title": "[2]--第2册视频-Seven in a Tent",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 33503,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NWJlNGIwZDg0ZGFhZDZiZDg4IiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_6654275ce4b0694c98170810",
                "resource_type": 3,
                "resource_title": "[3]--第3册视频-Fun at the Fair",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 29408,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NWNlNGIwNjk0Yzk4MTcwODEwIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_6654275ee4b0d84daad6bd8b",
                "resource_type": 3,
                "resource_title": "[4]--第4册视频-A Magic Show",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 24973,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NWVlNGIwZDg0ZGFhZDZiZDhiIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542760e4b0694c9817081a",
                "resource_type": 3,
                "resource_title": "[5]--第5册视频-The Cake",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 21525,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NjBlNGIwNjk0Yzk4MTcwODFhIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542761e4b0694c98170820",
                "resource_type": 3,
                "resource_title": "[6]--第6册视频-Is It？",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 18517,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NjFlNGIwNjk0Yzk4MTcwODIwIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542763e4b0694c9817082a",
                "resource_type": 3,
                "resource_title": "[7]--第7册视频-I See",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 20197,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NjNlNGIwNjk0Yzk4MTcwODJhIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542764e4b0694c98170831",
                "resource_type": 3,
                "resource_title": "[8]--第8册视频-Hide and Seek",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 17582,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NjRlNGIwNjk0Yzk4MTcwODMxIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542766e4b0d84daad6bda8",
                "resource_type": 3,
                "resource_title": "[9]--第9册视频-A Name for the Little Dog",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 16671,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NjZlNGIwZDg0ZGFhZDZiZGE4IiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542768e4b0694c98170840",
                "resource_type": 3,
                "resource_title": "[10]--第10册视频-Naughty the Dog",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 16327,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NjhlNGIwNjk0Yzk4MTcwODQwIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542769e4b0d84daad6bdaf",
                "resource_type": 3,
                "resource_title": "[11]--第11册视频-Go Away,Naughty",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 16342,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NjllNGIwZDg0ZGFhZDZiZGFmIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_6654276be4b0d84daad6bdb3",
                "resource_type": 3,
                "resource_title": "[12]--第12册视频-December the Cat",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 13289,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NmJlNGIwZDg0ZGFhZDZiZGIzIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_6654276de4b0694c9817084e",
                "resource_type": 3,
                "resource_title": "[13]--第13册视频-Mum'Birthday",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 13389,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NmRlNGIwNjk0Yzk4MTcwODRlIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_6654276ee4b0694c98170855",
                "resource_type": 3,
                "resource_title": "[14]--第14册视频-Eat Out",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 12221,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NmVlNGIwNjk0Yzk4MTcwODU1IiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542770e4b0694c9817085f",
                "resource_type": 3,
                "resource_title": "[15]--第15册视频-Go Fishing",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 11552,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NzBlNGIwNjk0Yzk4MTcwODVmIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542771e4b0d84daad6bdc1",
                "resource_type": 3,
                "resource_title": "[16]--第16册视频-I Can",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 11958,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NzFlNGIwZDg0ZGFhZDZiZGMxIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542773e4b0d84daad6bdc4",
                "resource_type": 3,
                "resource_title": "[17]--第17册视频-Day Out",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 10744,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NzNlNGIwZDg0ZGFhZDZiZGM0IiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542774e4b0694c98170871",
                "resource_type": 3,
                "resource_title": "[18]--第18册视频-Have a Picnic",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 11278,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NzRlNGIwNjk0Yzk4MTcwODcxIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542776e4b0d84daad6bdcc",
                "resource_type": 3,
                "resource_title": "[19]--第19册视频-A Happy Ride",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 12043,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NzZlNGIwZDg0ZGFhZDZiZGNjIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66542778e4b0d84daad6bdd0",
                "resource_type": 3,
                "resource_title": "[20]--第20册视频-Go to the Zoo",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 11819,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDI3NzhlNGIwZDg0ZGFhZDZiZGQwIiwicHJvZHVjdF9pZCI6InBfNjY1M2Y2MzllNGIwNjk0Yzk4MTZjZTkzIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320147znjgxxlwodix3j.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_ckoakjcq7pujmmqoqhm0/znjgxxlwodix3j.png",
                "learn_progress": 0
            }
        ]
    },
    "forward_url": ""
}


def api(first_resource_id, first_resource_type, resource_id, resource_title):
    url = "https://appfte6oc8n4154.xet-pc.citv.cn/xe.course.business.video.mutli_line/1.0.0"

    headers = {
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
        "req-uuid": "20250811152754000820379",
        "retry": "1",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://appfte6oc8n4154.xet-pc.citv.cn",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": f"https://appfte6oc8n4154.xet-pc.citv.cn/p/t_pc/course_pc_detail/video/{resource_id}?content_app_id=&product_id={first_resource_id}&type={first_resource_type}",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    }

    # 原始复杂 JSON cookie字符串
    raw_userInfo = '{"app_id":"appfte6oc8n4154","birth":null,"can_modify_phone":true,"universal_union_id":null,"user_id":"u_6888a238a49c6_EFVgSkIV5z","wx_account":"","wx_avatar":"http://commonresource-1252524126.cdn.xiaoeknow.com/image/default.svg","wx_gender":0,"phone":"13923003003","pc_user_key":"950af0b9efe281c240b2fd14ff82b93a","permission_visit":0,"permission_comment":0,"permission_buy":0,"pwd_isset":true,"channels":[{"type":"wechat","active":0},{"type":"qq","active":0}],"area_code":"86"}'

    raw_shopInfo = '{"base":{"shop_id":"appfte6oc8n4154","merchant_id":"mchGAcCcohL1NVd","shop_name":"博商大课堂","shop_logo":"http://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/khvgn8g80h7iazwah9av.jpg","main_type":null,"use_https":0,"footer_logo":"http://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/cmVzb3VyY2Utc2hvcFNldHRpbmctNjkxNzU5MDY.","profile":"","use_collection":0,"wx_app_type":1,"create_time":"2020-11-16 16:02:38","extra":"","check_name":null,"shop_tag":0,"is_authorized":1},"domain":{"h5_url":"https://appfte6oc8n4154.h5.xiaoeknow.com","pc_common_url":"https://appfte6oc8n4154.pc.xiaoe-tech.com","pc_custom_url":"","shop_id":"appfte6oc8n4154"},"version_type":4,"expire_time":"2026-11-18 14:13:16","pre_version":0,"rights_type":0,"status":{"is_sealed":0,"is_expired":0,"sealed_reason":""}}}'

    cookies = {
        "shop_version_type": "8",
        "LANGUAGE_appfte6oc8n4154": "cn",
        "sensorsdata2015jssdkcross": '{"$device_id":"1987934099b11e4-07adacc35dc2e08-17525636-1440000-1987934099c14ca"}',
        "appId": "appfte6oc8n4154",
        "sa_jssdk_2015_appfte6oc8n4154_xet-pc_citv_cn": '{"distinct_id":"u_6888a238a49c6_EFVgSkIV5z","first_id":"1987934099b11e4-07adacc35dc2e08-17525636-1440000-1987934099c14ca","props":{}}',
        "anonymous_user_key": "dV9hbm9ueW1vdXNfNjg5OTg1MDQ2YWNmN19CblFINkVnemZt",
        "pc_user_key": "950af0b9efe281c240b2fd14ff82b93a",
        "xenbyfpfUnhLsdkZbX": "0",
        "newuserdays": "90",
        "olduserdays": "180",
        "logintime": "1755006753",
        "show_user_icon": "1",
        "userInfo": urllib.parse.quote(raw_userInfo, safe=''),
        "shopInfo": urllib.parse.quote(raw_shopInfo, safe=''),
    }

    data = {
        "resource_id": resource_id
    }

    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    # print(response.status_code)
    jsons = response.json()
    print(jsons)

    encrypt_url = jsons.get("data", {}).get("cloud_data").get("hw").get("encrypt_url")
    download_m3u8_to_mp4(encrypt_url, "/Users/zkp/Downloads/未命名文件夹 3/", f"{resource_title}.mp4")


def download_m3u8_to_mp4(m3u8_url, output_dir, output_filename="output.mp4"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    cmd = [
        "ffmpeg",
        "-reconnect", "1",
        "-reconnect_at_eof", "1",
        "-reconnect_streamed", "1",
        "-reconnect_delay_max", "5",
        "-protocol_whitelist", "file,http,https,tcp,tls,crypto",
        "-i", m3u8_url,
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        "-y",
        output_path
    ]

    print("开始下载并转换为mp4...")
    subprocess.run(cmd, check=True)
    print(f"完成，文件保存在 {output_path}")


if __name__ == "__main__":
    first_resource_id = "p_6653f639e4b0694c9816ce93"
    first_resource_type = 6

    list_data = url2.get("data", {}).get("list", [])
    for item in list_data:
        resource_id = item["resource_id"]
        resource_title = item["resource_title"]
        api(first_resource_id, first_resource_type, resource_id, resource_title)
