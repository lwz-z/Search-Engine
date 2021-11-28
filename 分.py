import jieba
import pandas as pd
import pymongo
import pymysql

f = open('dbfilm.csv',encoding = 'UTF-8')
data=pd.read_csv(f) #将csv文件读入并转化为dataframe形式

def check_contain_chinese(check_str):
    for ch in check_str:
       if u'\u4e00' <= ch <= u'\u9fff':
          return True
       if "a" <= ch <= "z" or "A" <= ch <= "X":
          return True
       if "0" <= ch <= "9":
          return True
    return False


id = data['_id'].values
url = data['url'].values
name = data['电影'].values
data2 = []
# print(id,url,name)
for i in range (len(id)):
    cut = jieba.cut(name[i])
    keyword = ""
    for  c in cut:
        if check_contain_chinese(c):
            keyword += " "+c
    keyword = keyword.strip()
    data2.append([name[i],keyword,url[i]])
print(data2)

data3 = pd.DataFrame(data2,columns=["title","keyword","url"])
# print(data3)
data3.to_csv("cleaned_database.csv",index=False)

titlelist=[]
keywordlist = []
urllist =[]
for line in data3.itertuples():
    title, keyword, url = line[1],line[2],line[3]
    titlelist.append(title)
    keywordlist.append(keyword)
    urllist.append(url)



db = pymysql.connect(host='127.0.0.1', user="root", password="123456", port=3306, db="nosql")
cursor = db.cursor()
for i in range (len(titlelist)):
    cursor.execute("insert into film(title,keywords,url) values (%s,%s,%s)",(titlelist[i],keywordlist[i],urllist[i]))
    # print("插入成功")
db.commit()
sql = "select * from film;"
res = cursor.execute(sql)
# res = list(res)
# length = len(res)
print(res)




