from selenium import webdriver

from FilmNameAndUrl import FilmUrl
from FilmInfo import FileInfo
from ConnectMongodb import MongodbHandle
from SpliteBasicInfo import spliteBasicInfo


# Mongodb数据库连接
client = MongodbHandle(db_name="豆瓣电影")
db = client.db

# 爬虫步骤1.爬电影名称和链接
if "电影链接" not in db.list_collection_names():
    driver = webdriver.Chrome("chromedriver")  # 浏览器驱动
    col = db["电影链接"]  # 存放数据库
    fileurl = FilmUrl().scrapy_main(col, driver)

    # 关闭驱动
    driver.quit()


# 爬虫步骤2.通过html爬取豆瓣电影相关详情
col_in = db["电影链接"]
col_out = db["电影信息"]

if col_out.estimated_document_count() < col_in.estimated_document_count():
    driver = webdriver.Chrome("chromedriver")  # 浏览器驱动
    fileinfo = FileInfo().fileinfo(col_in, col_out, driver)

    # 拆分基本信息
    spliteBasicInfo(col_out)

    # 关闭驱动
    driver.quit()

# 将mongodb的id整理
col2 = db['电影整理后信息']
contents = col_out.find()
for index, content in enumerate(contents):
    num = index + 1
    content['_id'] = num
    col2.insert_one(content)


# 关闭数据库
client.close_db()
