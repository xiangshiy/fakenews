# __*__ coding:utf-8 __*__
import json
import time
from os.path import exists

import requests
from playwright.sync_api import sync_playwright
from time import sleep
import bs4
import urllib3


def join_url(url):
    """ 拼接url """
    if url.startswith("http"):
        return url
    else:
        url = urllib3.util.parse_url("https://www.piyao.org.cn/bd/" + url).url
        return url


def getTimeFromUrl(url):
    """ 从url中获取时间 """
    # 'https://www.piyao.org.cn/20221216/24c3358e36cc4de99b15915c2a2e26e1/c.html', 'https://www.piyao.org.cn/2022-11/10/c_1211699454.htm'
    if '-' in url:
        t = url.replace("https://www.piyao.org.cn/", "")
        ts = t.split("/")
        return ts[0].replace("-", "") + ts[1]
    else:
        t = url.replace("https://www.piyao.org.cn/", "")
        ts = t.split("/")
        return ts[0]


if __name__ == '__main__':
    # 获取网页源代码
    header = {
        "Host": "www.piyao.org.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.piyao.org.cn/",
        "Connection": "keep-alive",
        "Cookie": "wdcid=2a775bff15bb14aa; wdlast=1705665369; arialoadData=true; ariawapChangeViewPort=false",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

    resp = requests.get("https://www.piyao.org.cn/rm/bd.htm", headers=header).text.encode('gbk', 'ignore')
    html = bs4.BeautifulSoup(resp, 'html.parser')
    a = html.find_all("a", {"target": "_blank"})
    urls = []
    for i in a:
        if i.get("href").startswith("http"):
            urls.append(i.get("href"))
        else:
            urls.append(join_url(i.get("href")))
    print(urls)

    header = {
        "Host": "www.piyao.org.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "utf-8",
        "Connection": "keep-alive",
        "Cookie": "wdcid=2a775bff15bb14aa; wdlast=1705666682; arialoadData=true; ariawapChangeViewPort=false",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

    # 获取详细内容
    with open("./content/content3.json", "a+", encoding="utf-8") as f:
        keywords = []
        index = 0
        for i in urls:
            resp = requests.get(i, headers=header).content
            html = bs4.BeautifulSoup(resp, 'html.parser')
            content = html.find_all("p")
            flag = False
            for j in content:
                text = j.find("strong")
                if text is not None:
                    text = text.text
                    if text.startswith("谣言"):
                        flag = True
                        keywords.append({
                            "keyword_order": f"{700 + index}",
                            "keyword": text[4:]
                        })
                        continue
                if flag or "-" in i:
                    img = j.find("img")
                    if img is None:
                        continue
                    src = img.get("src")
                    src = i.replace(i.split("/")[-1], "") + src
                    if exists(f"./content/content3/{700 + index}.jpg"):
                        index += 1
                        continue
                    with open(f"./content/content3/{700 + index}.jpg", "wb") as f1:
                        f1.write(requests.get(src).content)
                    index += 1
            sleep(2)
        json.dump(keywords, f, indent=4, skipkeys=True, ensure_ascii=False)
