import json
import logging
import os
import re
import time

from threading import Thread

from selenium.webdriver.common.by import By
from selenium import webdriver
from MultiPlatVideoCrawler.VideoMultiThreadDownloader import VideoMultiThreadDownloader
from MultiPlatVideoCrawler.CommentSaver import CommentSaver
from MultiPlatVideoCrawler.conf.config import PROJECT_PATH, Profile_dir, DouYinDataSavePath, KuaiShowDataSavePath, \
    VIDEO_MAX_NUM
from MultiPlatVideoCrawler.utils.log import log_warn, log_INFO

DataSavePath = 0


class AutoSlider:

    def __init__(self, platform: str) -> None:
        self.kuaishou_downloader = None
        self.option = None
        self.keywords = []
        platform_url = {
            "kuaishou": "https://www.kuaishou.com/",
            "douyin": "https://www.douyin.com/"
        }
        global DataSavePath
        DataSavePath = KuaiShowDataSavePath if platform == 'kuaishou' else DouYinDataSavePath
        # 生成判断url中是否包含comment的正则表达式
        self.comment_url = re.compile("^https://www\.douyin\.com/aweme/v1/web/comment/list/")
        self.video_list_url = re.compile("^https://www\.douyin\.com/aweme/v1/web/general/search/single/")
        self.kuaishou_request_url = re.compile("^https://www\.kuaishou\.com/graphql")

        self.douyin_downloader = None
        # 浏览器驱动（火狐）
        self.driver = None

        # 视频平台
        self.platform = platform

        # 视频平台主页
        self.platform_url = platform_url[platform]

        # 设置浏览器参数
        self.setBrowserOption()

        # 导入关键字
        self.addKeyWords()

        # 保存状态->是否开始搜索->决定是否调用search方法 search方法只会调用一次
        self.isStart = False

        # 当前搜索的关键字id
        self.now_search = None

    def addKeyWords(self):
        """"为搜索添加关键字，并为其创建文件夹"""
        # 打开文件
        with open(f"{PROJECT_PATH}\keywords\LastKeyIN{self.platform}.json", "r", encoding="utf-8") as f:
            last = json.load(f)
            last = last['Lastkeyword']

        with open(f"{PROJECT_PATH}\keywords\keywords.json", "r", encoding="utf-8") as f:
            flag = False
            for i in json.load(f):
                if last == '' or last is None:
                    flag = True
                if flag == False and i["keyword_order"] == int(last):
                    flag = True
                if not flag:
                    continue
                # 添加关键字
                self.keywords.append(i)
                # 关键字id文件夹
                self.mkdir(f"{DataSavePath}\\{i['keyword_order']}")
                # 评论
                self.mkdir(f"{DataSavePath}\\{i['keyword_order']}\\comments")
                # 视频
                self.mkdir(f"{DataSavePath}\\{i['keyword_order']}\\video")

    def setBrowserOption(self) -> None:
        """设置浏览器参数"""
        # 添加保持登录的数据路径：安装目录一般在C:\Users\user\AppData\Local\Google\Firefox\User Data
        profile = webdriver.FirefoxProfile(Profile_dir)
        # 驱动选项
        option = webdriver.FirefoxOptions()
        # 解除自动化控制标记
        option.add_argument("--disable-blink-features=AutomationControlled")
        option.profile = profile

        # 初始化driver
        self.option = option

    @staticmethod
    def get_html_elements(driver, xpath: str) -> list:
        """
        获取html元素列表
        @param driver:
        @param xpath: xpath
        @return: html元素列表
        """
        try:
            elements = driver.find_elements(By.XPATH, xpath)
        except Exception as e:
            logging.error(e)
            elements = []
        return elements

    @staticmethod
    def doFuncUntilNoException(func, args: tuple) -> any:
        """执行函数，如果报错，等待一段时间后继续执行直到正常执行"""
        while True:
            try:
                result = func(*args)
            except Exception as e:
                print(e)
                time.sleep(1)
                log_warn("an error!")
                continue
            else:
                return result

    def setNowSearch(self, keyID) -> any:
        """设置当前搜索的关键字"""
        self.now_search = keyID['keyword_order']
        with open(f"{PROJECT_PATH}\keywords\LastKeyIN{self.platform}.json", "w", encoding="utf-8") as f:
            json.dump({
                "Lastkeyword": self.now_search
            }, f)

    def searchInDouYin(self) -> None:
        """
        在平台中搜索
        """

        time.sleep(5)
        for keyword in self.keywords:
            # 设置当前搜索
            self.setNowSearch(keyword)
            # 初始化抖音下载器
            self.douyin_downloader = VideoMultiThreadDownloader(
                f"{DataSavePath}\\{self.now_search}\\video",
                "douyin", 10)
            # 打开浏览器
            driver = webdriver.Firefox(options=self.option)
            # 最大化
            driver.maximize_window()
            # 请求
            driver.get(f"https://www.douyin.com/search/{keyword['keyword']}")
            video_order = 0

            def findScrollList():
                li = self.doFuncUntilNoException(driver.find_elements, (By.XPATH, "//ul[@data-e2e='scroll-list']/li"))
                time.sleep(2)
                return li[0].get_attribute('class')

            className = self.doFuncUntilNoException(findScrollList, ())

            log_warn(className)
            for i in range(VIDEO_MAX_NUM):
                scroll2view = """
                                 let element = document.getElementsByClassName(\"""" + className + "\")[" + str(
                    i) + "];" + \
                              """                 
                                 element.scrollIntoView({  
                                    behavior: 'smooth',
                                    block: 'start',
                                    inline: 'start'
                                 });
                              """
                driver.execute_script(scroll2view)
                try:
                    self.get_html_elements(driver,
                                           f"//div[@data-e2e='feed-comment-icon']")[video_order].click()
                except Exception as e:
                    print(e)
                time.sleep(5)
                video_order += 1
            driver.quit()

    def searchInKuaiShou(self):

        time.sleep(5)
        for keyword in self.keywords:
            # 设置当前搜索
            self.setNowSearch(keyword)

            # 初始化快手下载器
            self.kuaishou_downloader = VideoMultiThreadDownloader(
                f"{DataSavePath}\\{self.now_search}\\video",
                "kuaishou", 10)
            # 打开浏览器
            gecko_driver_path = 'D:\Python\python3.11.4\geckodriver.exe'
            # 固定搭配直接用就行了
            # service = Service(executable_path=gecko_driver_path)
            driver = webdriver.Firefox(options=self.option)
            # 最大化
            driver.maximize_window()
            # 请求
            driver.get(f"https://www.kuaishou.com/search/video?searchKey={keyword['keyword']}")
            time.sleep(5)
            card = self.doFuncUntilNoException(driver.find_element,
                                               (By.CSS_SELECTOR,
                                                "div.video-card:nth-child(1)>div:nth-child(1)>div:nth-child(1)"))
            # 点击第一张卡片
            self.doFuncUntilNoException(card.click, ())
            time.sleep(2)
            next_t = self.doFuncUntilNoException(driver.find_element,
                                                 (By.CSS_SELECTOR, "div.video-switch-next"))
            for i in range(VIDEO_MAX_NUM):
                time.sleep(5)
                # 下一个
                self.doFuncUntilNoException(next_t.click, ())
            driver.quit()

    @staticmethod
    def mkdir(path):
        try:
            os.mkdir(path)
        except FileExistsError as e:
            # print(e)
            pass

    def response(self, flow):
        if not self.isStart:
            self.isStart = True
            # 搜索
            if self.platform == "douyin":
                Thread(target=self.searchInDouYin).start()
            else:
                Thread(target=self.searchInKuaiShou).start()
        if flow is None:
            return

        # 判断是否满足评论url
        if self.comment_url.match(flow.request.url):
            log_warn("a comment!")

            # 格式转换
            json_data = json.loads(flow.response.get_text())

            comment_list = []
            aweme_id = json_data['comments'][0]['aweme_id']

            # 迭代存储
            for comment_data in json_data['comments']:
                comment_list.append({
                    "text": comment_data['text'],
                    "digg_count": comment_data['digg_count']
                })
            # 保存评论
            CommentSaver(aweme_id, {
                "aweme_id": aweme_id,
                "comment": comment_list,
                "count": len(comment_list)
            }, f"{DataSavePath}\\{self.now_search}\\comments").save()
        elif self.video_list_url.match(flow.request.url):
            # 格式转换
            json_data = json.loads(flow.response.get_text())['data']
            for v in json_data:
                try:
                    vid = v['aweme_info']['aweme_id']
                    url_list = v['aweme_info']['video']['download_addr']['url_list']
                    for url in url_list:
                        # log_warn(url)
                        try:
                            self.douyin_downloader.download_control("download", (vid, url))
                        except Exception:
                            log_warn(f'{url} failed!!')
                        else:
                            break
                except KeyError as e:
                    print(e)
                    continue
        elif self.kuaishou_request_url.match(flow.request.url):
            queryData = json.loads(flow.request.content)
            if queryData['operationName'] == "commentListQuery":
                # 格式转换
                json_data = json.loads(flow.response.get_text())['data']
                log_warn("a comment!")
                comment_list = []
                aweme_id = queryData['variables']['photoId']

                # 迭代存储
                for comment_data in json_data['visionCommentList']['rootComments']:
                    comment_list.append({
                        "text": comment_data['content'],
                        "digg_count": comment_data['likedCount']
                    })
                # 保存评论
                CommentSaver(aweme_id, {
                    "aweme_id": aweme_id,
                    "comment": comment_list,
                    "count": len(comment_list)
                }, f"{DataSavePath}\\{self.now_search}\\comments").save()
            elif queryData['operationName'] == "visionSearchPhoto":
                # 格式转换
                video_list = json.loads(flow.response.get_text())['data']['visionSearchPhoto']['feeds']
                for v in video_list:
                    try:
                        video = v['photo']
                        self.kuaishou_downloader.download_control("download", (video['id'], video['photoUrl']))
                    except KeyError as e:
                        print(e)
                        continue


if __name__ == "__main__":
    obj = AutoSlider("kuaishou")
    obj.searchInKuaiShou()
