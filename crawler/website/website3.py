# __*__ coding:utf-8 __*__
import time

import requests
from playwright.sync_api import sync_playwright
from time import sleep

header = {
    "Host": "www.piyao.org.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "http://www.piyao.org.cn/",
    "Connection": "keep-alive",
    "Cookie": "wdcid=2a775bff15bb14aa; wdlast=1699194569; arialoadData=true; ariawapChangeViewPort=false",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}
print(str(requests.get("https://www.piyao.org.cn/rm/bd.htm", headers=header).text.encode('gbk', 'ignore')))


# 注意：默认是无头模式
with sync_playwright() as p:
    # 分别对应三个浏览器驱动
    browser_type = p.chromium

    # 指定为有头模式，方便查看
    browser = browser_type.launch(headless=False)
    page = browser.new_page()
    page.goto('https://www.piyao.org.cn/jrpy/index.html')

    # # 执行一次搜索操作
    # page.fill("input[name=\"wd\"]", "AirPython")
    # with page.expect_navigation():
    #     # page.press("input[name=\"wd\"]", "Enter")
    time.sleep(2)
    #     # 等待页面加载完全
    #     # page.wait_for_selector("text=榜单")
    #     #
    #     # 截图
    a = page.query_selector_all("#list>li>h2>a")
    for i in a:
        print(i.get_attribute("href"))

    page.screenshot(path=f'example-{browser_type.name}.png')

    # 休眠5s
    sleep(5)

    # 关闭浏览器
    browser.close()
