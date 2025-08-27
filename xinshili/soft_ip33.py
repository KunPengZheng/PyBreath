import requests

jsons = {
    "code": 0,
    "msg": "success",
    "data": {
        "total": 48,
        "list": [
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_6654532ce4b0694c98177293",
                "resource_type": 3,
                "resource_title": "0、导言",
                "is_try": 1,
                "part_try_length": 600,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 70554,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzMmNlNGIwNjk0Yzk4MTc3MjkzIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_67ee3bcee4b0694ca08d91f6",
                "resource_type": 3,
                "resource_title": "听课前1分钟预警！必听！",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2025.04.03",
                "interval_start_at": "",
                "view_count": 40807,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjdlZTNiY2VlNGIwNjk0Y2EwOGQ5MWY2IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_6654532de4b0d84daad716f9",
                "resource_type": 3,
                "resource_title": "1、听音拼写第一组，敢拼就是赢",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 112055,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzMmRlNGIwZDg0ZGFhZDcxNmY5IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_6654532fe4b0694c9817729e",
                "resource_type": 3,
                "resource_title": "2、听音拼写第二组，抓住字母包含音",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 98938,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzMmZlNGIwNjk0Yzk4MTc3MjllIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66545330e4b0d84daad71701",
                "resource_type": 3,
                "resource_title": "3、听音拼写第三组，开闭音节开闭气流【上】",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 78657,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzMzBlNGIwZDg0ZGFhZDcxNzAxIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66545332e4b0694c981772ae",
                "resource_type": 3,
                "resource_title": "4、听音拼写第三组，开闭音节开闭气流【下】",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 68508,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzMzJlNGIwNjk0Yzk4MTc3MmFlIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66545334e4b0694c981772b1",
                "resource_type": 3,
                "resource_title": "5、听音拼写第四组，联想老词写新词【上】",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 61730,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzMzRlNGIwNjk0Yzk4MTc3MmIxIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66545335e4b0694c981772b4",
                "resource_type": 3,
                "resource_title": "6、听音拼写第四组，联想老词写新词【下】",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 54386,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzMzVlNGIwNjk0Yzk4MTc3MmI0IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66545337e4b0694c981772b9",
                "resource_type": 3,
                "resource_title": "7、听音拼写第五组，难点单独练一练",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 57257,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzMzdlNGIwNjk0Yzk4MTc3MmI5IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66545339e4b0694c981772be",
                "resource_type": 3,
                "resource_title": "8、听音拼写第六组，耳朵抓住每个音",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 52877,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzMzllNGIwNjk0Yzk4MTc3MmJlIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_6654533ae4b0694c981772c3",
                "resource_type": 3,
                "resource_title": "9、听音拼写第七组，边读边写才可以",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 51143,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzM2FlNGIwNjk0Yzk4MTc3MmMzIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_6654533ce4b0d84daad7171d",
                "resource_type": 3,
                "resource_title": "10、听音对比第八组，英音美音小差异",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 41804,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzM2NlNGIwZDg0ZGFhZDcxNzFkIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_6654533de4b0d84daad71720",
                "resource_type": 3,
                "resource_title": "11、听音拼写第九组，老外这么写中国词",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 40957,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzM2RlNGIwZDg0ZGFhZDcxNzIwIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_6654533fe4b0694c981772d1",
                "resource_type": 3,
                "resource_title": "12、听音测试第十组，联系老词写新词",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 46807,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzM2ZlNGIwNjk0Yzk4MTc3MmQxIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66545340e4b0d84daad71722",
                "resource_type": 3,
                "resource_title": "13、示范素材1-读谜语英雄记单词",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 55234,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNDBlNGIwZDg0ZGFhZDcxNzIyIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66545342e4b0d84daad71728",
                "resource_type": 3,
                "resource_title": "14、示范素材2-读莎士比亚玩单词",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 37932,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNDJlNGIwZDg0ZGFhZDcxNzI4IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66545344e4b0694c981772de",
                "resource_type": 3,
                "resource_title": "15、示范素材3 发现名著长这样",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 34361,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNDRlNGIwNjk0Yzk4MTc3MmRlIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66545345e4b0694c981772e4",
                "resource_type": 3,
                "resource_title": "16、示范素材4-读穷爸爸富爸爸，看到海量初中词汇",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 35732,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNDVlNGIwNjk0Yzk4MTc3MmU0IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66545347e4b0694c981772ea",
                "resource_type": 3,
                "resource_title": "17、示范素材5-读李嘉诚传，理解记单词必须扎心",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 30112,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNDdlNGIwNjk0Yzk4MTc3MmVhIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            },
            {
                "app_id": "appfte6oc8n4154",
                "resource_id": "v_66545348e4b0d84daad71734",
                "resource_type": 3,
                "resource_title": "18、示范素材6-看小侦探记单词",
                "is_try": 0,
                "part_try_length": 0,
                "can_view": 0,
                "start_at": "2024.05.27",
                "interval_start_at": "",
                "view_count": 30950,
                "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNDhlNGIwZDg0ZGFhZDcxNzM0IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
                "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
                "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
                "learn_progress": 0
            }
        ]
    },
    "forward_url": ""
}

#
# {
#   "code": 0,
#   "msg": "success",
#   "data": {
#     "total": 48,
#     "list": [
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_6654534ae4b0d84daad71736",
#         "resource_type": 3,
#         "resource_title": "19、示范素材7-带你记小学单词",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 35059,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNGFlNGIwZDg0ZGFhZDcxNzM2IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_6654534ce4b0694c981772f2",
#         "resource_type": 3,
#         "resource_title": "20、示范素材8-中考单词猜出来",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 29280,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNGNlNGIwNjk0Yzk4MTc3MmYyIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_6654534de4b0d84daad71739",
#         "resource_type": 3,
#         "resource_title": "21、示范素材9-十岁就要看看高考卷",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 31777,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNGRlNGIwZDg0ZGFhZDcxNzM5IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_6654534fe4b0694c981772f5",
#         "resource_type": 3,
#         "resource_title": "22、（新版）闭眼三步拼写1-没有e结尾",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 32498,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNGZlNGIwNjk0Yzk4MTc3MmY1IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545350e4b0694c981772fa",
#         "resource_type": 3,
#         "resource_title": "23、（新版）闭眼三步拼写2有e结尾",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 26797,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNTBlNGIwNjk0Yzk4MTc3MmZhIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545352e4b0d84daad71743",
#         "resource_type": 3,
#         "resource_title": "24、（新版）闭眼三步拼写3-字母c的软音和硬音",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 23519,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNTJlNGIwZDg0ZGFhZDcxNzQzIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545354e4b0694c98177300",
#         "resource_type": 3,
#         "resource_title": "25、（新版）闭眼三步拼写4-字母bl，cl，fl在开头和结尾",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 21789,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNTRlNGIwNjk0Yzk4MTc3MzAwIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545355e4b0694c98177303",
#         "resource_type": 3,
#         "resource_title": "26、（新版）闭眼三步拼写5 结尾的l",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 22146,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNTVlNGIwNjk0Yzk4MTc3MzAzIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545357e4b0694c98177308",
#         "resource_type": 3,
#         "resource_title": "27、（新版）闭眼三步拼写6鼻音n",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 21170,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNTdlNGIwNjk0Yzk4MTc3MzA4IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545358e4b0d84daad7174d",
#         "resource_type": 3,
#         "resource_title": "28、（新版）闭眼三步拼写7-元音字母加r",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 19294,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNThlNGIwZDg0ZGFhZDcxNzRkIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_6654535ae4b0d84daad7174f",
#         "resource_type": 3,
#         "resource_title": "29、（新版）闭眼三步拼写8-长单词切分",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 19735,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNWFlNGIwZDg0ZGFhZDcxNzRmIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_6654535be4b0694c9817730c",
#         "resource_type": 3,
#         "resource_title": "30、（新版）闭眼三步拼写9-警惕自然拼读",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 16993,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNWJlNGIwNjk0Yzk4MTc3MzBjIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_6654535de4b0d84daad71751",
#         "resource_type": 3,
#         "resource_title": "31、（新版）杨妈手把手带你阅读记单词-西游记1",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 26345,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNWRlNGIwZDg0ZGFhZDcxNzUxIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_6654535ee4b0694c98177311",
#         "resource_type": 3,
#         "resource_title": "32、（新版）杨妈手把手带你阅读记单词-西游记2",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 21513,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNWVlNGIwNjk0Yzk4MTc3MzExIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545360e4b0d84daad71758",
#         "resource_type": 3,
#         "resource_title": "33、（新版）杨妈手把手带你阅读记单词-西游记3",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 20812,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNjBlNGIwZDg0ZGFhZDcxNzU4IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545362e4b0694c98177314",
#         "resource_type": 3,
#         "resource_title": "34、（新版）杨妈手把手带你阅读记单词-西游记",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 20049,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNjJlNGIwNjk0Yzk4MTc3MzE0IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545363e4b0694c98177316",
#         "resource_type": 3,
#         "resource_title": "35、（新版）杨妈手把手带你阅读记单词-西游记5",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 18151,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNjNlNGIwNjk0Yzk4MTc3MzE2IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545365e4b0694c9817731a",
#         "resource_type": 3,
#         "resource_title": "36、（新版）杨妈手把手带你阅读记单词-课文1",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 17325,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNjVlNGIwNjk0Yzk4MTc3MzFhIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545375e4b0694c9817733e",
#         "resource_type": 3,
#         "resource_title": "37、（新版）杨妈手把手带你阅读记单词-课文2",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 16095,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNzVlNGIwNjk0Yzk4MTc3MzNlIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545367e4b0d84daad7175e",
#         "resource_type": 3,
#         "resource_title": "38、彩蛋-大师姐胡娜有话说",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 13065,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNjdlNGIwZDg0ZGFhZDcxNzVlIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       }
#     ]
#   },
#   "forward_url": ""
# }


# {
#   "code": 0,
#   "msg": "success",
#   "data": {
#     "total": 48,
#     "list": [
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545368e4b0694c98177320",
#         "resource_type": 3,
#         "resource_title": "39、彩蛋-多感官+词缀",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 11585,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNjhlNGIwNjk0Yzk4MTc3MzIwIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_6654536ae4b0d84daad71762",
#         "resource_type": 3,
#         "resource_title": "40.警惕词根词缀法",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 9934,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNmFlNGIwZDg0ZGFhZDcxNzYyIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_6654536be4b0694c98177324",
#         "resource_type": 3,
#         "resource_title": "41、彩蛋- 关于天赋的质疑",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 9422,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNmJlNGIwNjk0Yzk4MTc3MzI0IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_6654536de4b0694c98177326",
#         "resource_type": 3,
#         "resource_title": "42、彩蛋-刘三炮吐槽杨妈的方法",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 10701,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNmRlNGIwNjk0Yzk4MTc3MzI2IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_6654536fe4b0d84daad71766",
#         "resource_type": 3,
#         "resource_title": "43、彩蛋-学语文 我们这样记单词",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 10173,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNmZlNGIwZDg0ZGFhZDcxNzY2IiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545370e4b0d84daad7176a",
#         "resource_type": 3,
#         "resource_title": "44、加更1：巧记周一到周日",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 11013,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNzBlNGIwZDg0ZGFhZDcxNzZhIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545372e4b0694c98177331",
#         "resource_type": 3,
#         "resource_title": "45、加更2：巧记一月到十二月",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 10757,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNzJlNGIwNjk0Yzk4MTc3MzMxIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       },
#       {
#         "app_id": "appfte6oc8n4154",
#         "resource_id": "v_66545373e4b0694c9817733b",
#         "resource_type": 3,
#         "resource_title": "46 、加更3：“偏旁部首”构词法",
#         "is_try": 0,
#         "part_try_length": 0,
#         "can_view": 0,
#         "start_at": "2024.05.27",
#         "interval_start_at": "",
#         "view_count": 11999,
#         "jump_url": "/content_page/eyJ0eXBlIjoyLCJyZXNvdXJjZV90eXBlIjozLCJyZXNvdXJjZV9pZCI6InZfNjY1NDUzNzNlNGIwNjk0Yzk4MTc3MzNiIiwicHJvZHVjdF9pZCI6InBfNjY1NDQzZDBlNGIwZDg0ZGFhZDZmNGVhIiwiYXBwX2lkIjoiYXBwZnRlNm9jOG40MTU0In0",
#         "img_url_compressed": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/compress/414320333fhyildlwoao5yo.png",
#         "img_url": "https://wechatapppro-1252524126.file.myqcloud.com/appfte6oc8n4154/image/b_u_conjssra7lj0i9hfnst0/fhyildlwoao5yo.png",
#         "learn_progress": 0
#       }
#     ]
#   },
#   "forward_url": ""
# }

def api(resource_id):
    # 请求 URL
    url = "https://appfte6oc8n4154.xet-pc.citv.cn/xe.course.business.audio.info.get/2.0.0"
    video_url = "https://appfte6oc8n4154.xet-pc.citv.cn/xe.course.business.video.detail_info.get/2.0.0"

    # 请求头
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://appfte6oc8n4154.xet-pc.citv.cn",
        "Referer": "https://appfte6oc8n4154.xet-pc.citv.cn/p/t_pc/course_pc_detail/audio/a_6673de49e4b0694c982dcd70?product_id=p_6673dd46e4b0694c982dcbb2&content_app_id=&type=6",
    }

    # 请求 Cookie（⚠️ 可选，但部分接口需要身份认证）
    cookies = {
        "pc_user_key": "f1d05643776cd11b4a18b1d808e61842",
        "LANGUAGE_appfte6oc8n4154": "cn",
        "appId": "appfte6oc8n4154",
        # 可以根据需要添加更多 cookie
    }

    # 请求体（表单数据）
    data = {
        "resource_id": f"{resource_id}",
        "opr_sys": "MacIntel",
        "product_id": "p_6673dd46e4b0694c982dcbb2",
        "content_app_id": ""  # 如果为空也要传
    }

    # 发送 POST 请求
    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    # 输出响应
    print("状态码:", response.status_code)
    print("返回内容:")
    print(response.text)

    if response.status_code == 200:
        try:
            json_data = response.json()
            audio_info = json_data.get("data", {}).get("audio_info")
            title = audio_info.get("title")
            audio_url = audio_info.get("audio_url")

            if audio_url:

                # 获取文件名
                file_path = f"/Users/zkp/Downloads/【私域部门专属】杨萃先：小阶总课包陪跑营/3/{title}.mp3"

                # 下载音频文件
                audio_response = requests.get(audio_url, stream=True)
                with open(file_path, "wb") as f:
                    for chunk in audio_response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                print(f"✅ 音频已保存至: {file_path}")
            else:
                print("❌ 无法找到 audio_url 字段")
        except Exception as e:
            print("❌ 解析 JSON 时出错:", e)
    else:
        print("❌ 请求失败，状态码:", response.status_code)


if __name__ == '__main__':
    # 提取 list 字段
    list_data = jsons.get("data", {}).get("list", [])

    # 输出结果
    print("提取到的 list 数据：")
    for item in list_data:
        resource_id = item["resource_id"]
        api(resource_id)
