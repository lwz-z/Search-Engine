import pymongo


class MongodbHandle(object):
    """
    用于处理与mongodb数据库交互工作
    """

    def __init__(self, host="127.0.0.1", port=27017, db_name=None, user=None, password=None):
        """
        建立连接
        host: 连接ip
        port: 服务端口
        db_name: 数据库名
        user: 用户名
        password: 用户密码
        """
        try:
            self.conn = pymongo.MongoClient(host, port)
            self.db = self.conn[db_name]
            if user:
                self.db.authenticate(user, password)
        except Exception as e:
            print("连接数据库时异常, 请检查")
            print(e)

    def close_db(self):
        """
        用于关闭数据库
        """
        self.conn.close()
