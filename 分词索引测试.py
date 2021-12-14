#分词索引搜索测试
import pymongo
import jieba
Client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = Client["pymongodb3"]
collection = db["db"]
collection2 = db["dbfc"]
class Ftest01():
    def setData(self):
        listFc= []  # 每条电影对应的部分信息的分词，用来和输入的关键词进行检索
        listData = []  # 每条电影的部分字段的信息，用来在网页上显示关键词对应的搜索结果
        #获取数据库中已经存在的数据
        datas =list(collection.find())
        for i in datas:    #i，一个电影的字典信息
            SData = " "
            Surl=" "
            for j in i:    #j，字典中的key
                if j!="_id" and j!="url":
                    SData=SData+str(i[j])
                if j=="url":
                    Surl=str([i[j]])
            listData.append(SData)
            listi=jieba.lcut_for_search(SData)  #分词
            listFc.append(str(set(listi)))
            idata= {'fcdata':str(set(listi)),'url':Surl,'fileData':SData}
            collection2.insert_one(idata)#将处理后的数据存入数据库
        #创建文本索引
        collection2.create_index([("fcdata", pymongo.TEXT)])
    def getData(self):
        #分词测试
        a=input("请输入要查询的电影名、演员及电影相关内容(例如：哪吒魔童摔跤数据库)：")
        inputList=jieba.lcut_for_search(a)
        #去掉"的"
        try:
            inputList.remove("的")
        except:
            pass
        print(inputList)
        inputString2=""
        for i in inputList:
            inputString2=inputString2+i+" "
        print("查询结果如下：")
        result=collection2.find({"$text": {"$search":inputString2+"*"}})  #通过创建的索引查询，用空格隔开，代表或
        k=1
        for i in result:
            for j in i:
                if j=="fileData":
                    print(i[j])
                    print(i["url"])
                    print("############################################################################################")
            k=0
        if k:
            print("未查询到相关信息!")

if __name__=="__main__":
    fc = Ftest01()
    a=input("已存在dbfc数据集?(y/n)")
    if a=="y":
        pass
    else:
        fc.setData()
    while True:
        b=input("查询?(y/n)")
        if b=="y":
            fc.getData()
        else:
            break

