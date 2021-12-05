import random
import time
import requests


def ClearURL(col):
    """
    清洗无效url
    :param col: 数据库指针
    :return: 总共有效url条数
    ...建议不用，容易封ip
    """
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    }

    try:
        for data in col.find():
            sleep_time = random.uniform(0.5, 3.0)
            time.sleep(sleep_time)
            url = data['url']
            if url:
                response = requests.request("get", url=url, headers=headers)
                status = response.status_code
                if status == 404:
                    col.delete_one(data)
            else:
                col.delete_one(data)
    except Exception as e:
        print("清洗数据出错\n", e)

