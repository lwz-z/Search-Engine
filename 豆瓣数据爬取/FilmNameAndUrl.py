import time


class FilmUrl(object):
    """
    爬虫步骤1.爬电影名称和链接
    数据采集目标首先提取电影名称
    https://www.douban.com/doulist/45793279/?start=0&sort=seq&playable=0&sub_type=    这是豆瓣评分最多的550余部电影
    豆瓣网站爬虫变式太多，需要随机应变
    """

    @staticmethod
    def scrapy_main(col, driver):
        """
        爬虫主体
        col: 传入数据库中表的'指针'
        driver：传入浏览器驱动
        """

        # 网页基本地址
        href1 = "https://www.douban.com/doulist/45793279/?start="
        href2 = "&sort=seq&playable=0&sub_type="
        # 爬取22页
        count = 0  # 记录爬取数据条数
        for i in range(22):
            try:
                js = "window.open('{}','_blank');"
                driver.execute_script(js.format(href1 + str(i * 25) + href2))
                if i:
                    driver.switch_to.window(driver.window_handles[-2])
                    driver.close()
                driver.switch_to.window(driver.window_handles[-1])
                driver.implicitly_wait(10)
                print(f"正在爬取第{i+1}页")

                # 获取每页的记录
                dict1 = dict()  # 存放数据的容器
                for ii in range(7, 7 + 25):
                    dict1.clear()
                    num = len(driver.find_elements_by_xpath("/html/body/div[3]/div[1]/div/div[1]/div[%d]/div/div[2]/div/a" % ii))
                    if num > 3:
                        num = 4
                    while driver.find_element_by_xpath(
                            "/html/body/div[3]/div[1]/div/div[1]/div[{0}]/div/div[2]/div[{1}]/a".format(ii, num)).text == "":
                        num += 1
                    dict1["电影"] = driver.find_element_by_xpath(
                        "/html/body/div[3]/div[1]/div/div[1]/div[{0}]/div/div[2]/div[{1}]/a".format(ii, num)).text
                    dict1["url"] = driver.find_element_by_xpath(
                        "/html/body/div[3]/div[1]/div/div[1]/div[{0}]/div/div[2]/div[{1}]/a".format(ii, num)).get_attribute("href")

                    # 数据插入
                    col.insert_one(dict1)
                    count += 1
                    time.sleep(0.1)
                    print(f"完成第{count}条数据的插入")

            except Exception as e:
                print("爬取电影名和url出现异常\n", e)

        driver.close()
        print(f"爬电影名称和链接爬取完成，共获取{count}条数据")
