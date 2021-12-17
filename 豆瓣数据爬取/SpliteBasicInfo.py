# 导演: 陈凯歌
# 编剧: 芦苇 / 李碧华
# 主演: 张国荣 / 张丰毅 / 巩俐 / 葛优 / 英达 / 蒋雯丽 / 吴大维 / 吕齐 / 雷汉 / 尹治 / 马明威 / 费振翔 / 智一桐 / 李春 / 赵海龙 / 李丹 / 童弟 / 沈慧芬 / 黄斐 / 徐杰
# 类型: 剧情 / 爱情 / 同性
# 制片国家/地区: 中国大陆 / 中国香港
# 语言: 汉语普通话
# 上映日期: 1993-07-26(中国大陆) / 1993-01-01(中国香港)
# 片长: 171分钟 / 155分钟(美国剧场版)
# 又名: 再见，我的妾 / Farewell My Concubine / Adieu Ma Concubine
# IMDb: tt0106332
from ConnectMongodb import MongodbHandle

def spliteBasicInfo(col):
    """
    拆分电影基本信息，使得数据更加值观
    :param col:基本信息所在数据库
    """
    for data in col.find({}, {"_id": 0, "basicinfo": 1}):
        try:
            datas = data['basicinfo'].split("\n")
            data_update = dict()
            for data_block in datas:
                data_blocks = data_block.split(": ")
                data_key = data_blocks[0]
                data_value = data_blocks[1]
                data_update[f"{data_key}"] = data_value
            col.update_one(data, {"$set": {"basicinfo": data_update}})
        except Exception as e:
            print("拆分数据出现异常\n", e)
