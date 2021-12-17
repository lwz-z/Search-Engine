from urllib import request


def CheckURL(url):
    """
    检查url是否可获得
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    }

    try:
        if url:
            req = request.Request(url=url, headers=headers)  # 包装请求头
            response = request.urlopen(req, timeout=2)  # 请求数据，2秒超时
            status = response.status  # 获取响应码
            if status == 404:
                return 0
        return 1
    except Exception as e:
        print("检查url出错\n", e)
