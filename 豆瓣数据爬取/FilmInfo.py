import time


class FileInfo(object):
    """
    爬虫步骤2.通过html爬取豆瓣电影相关信息
    """

    @staticmethod
    def fileinfo(col_in, col_out, driver):
        """
        提取网页mongo中爬取的所有电影信息
        col_in: url数据库表
        col_out: 基本信息存放的位置
        driver: 浏览器驱动
        """
        filenames = []
        sosuos = []
        flag = 0
        try:
            for x in col_in.find():
                ppp = x["电影"]
                lll = x["url"]
                if ppp == "肖申克的救赎 The Shawshank Redemption":
                    flag = 1
                if flag:
                    filenames.append(ppp)
                    sosuos.append(lll)
        except Exception as e:
            print("获取电影信息时出现异常\n", e)

        # 去除数据库连接
        del col_in

        kk = 548
        for baseurl in sosuos[548:]:
            try:
                js = "window.open('{}','_blank');"
                driver.execute_script(js.format(baseurl))
                time.sleep(0.1)
                if kk:
                    driver.switch_to.window(driver.window_handles[-2])
                    driver.close()
                driver.switch_to.window(driver.window_handles[-1])
                driver.implicitly_wait(2)

                print(driver.current_url)
                if len(driver.find_elements_by_xpath("//*[@id=\"info\"]/span[3]/span[2]/a")) != 0:
                    stringeg = driver.find_elements_by_xpath("//*[@id=\"info\"]/span[3]/span[2]/a")[-1].text
                    if stringeg[0:2] == "更多":
                        driver.find_elements_by_xpath("//*[@id=\"info\"]/span[3]/span[2]/a")[-1].click()
                if len(driver.find_elements_by_xpath("//*[@id=\"link-report\"]/span[1]/a")) != 0:
                    stringeg = driver.find_elements_by_xpath("//*[@id=\"link-report\"]/span[1]/a")[-1].text
                    if stringeg[1:5] == "展开全部":
                        driver.find_elements_by_xpath("//*[@id=\"link-report\"]/span[1]/a")[-1].click()

                news = driver.find_elements_by_xpath("//*[@id=\"info\"]")[-1].text
                about = driver.find_elements_by_xpath("//*[@id=\"link-report\"]")[-1].text
                awards = driver.find_elements_by_xpath("//*[@id=\"content\"]/div[3]/div[1]/div[8]/ul")
                if len(awards) == 0:
                    awards = driver.find_elements_by_xpath("//*[@id=\"content\"]/div[2]/div[1]/div[8]/ul")
                stringa = ""
                for award in awards:
                    stringa += award.text + "\n"
                stringa = stringa[:-1]
                score = driver.find_elements_by_xpath("//*[@id=\"interest_sectl\"]/div[1]/div[2]/strong")[-1].text
                scorepeople = driver.find_elements_by_xpath("//*[@id=\"interest_sectl\"]/div[1]/div[2]/div/div[2]/a/span")[
                    -1].text

                d1 = dict()
                d1["name"] = filenames[kk]
                d1["url"] = baseurl
                d1["basicinfo"] = news
                d1["about"] = about
                d1["awards"] = stringa
                d1["score"] = score
                d1["scorepeople"] = scorepeople
                col_out.insert_one(d1)
                kk += 1
            except Exception as e:
                print("爬取电影详情出现异常\n", e)

        driver.close()
        print("豆瓣电影相关信息获取完成")
