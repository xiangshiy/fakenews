import json
from os.path import exists
from time import sleep

import bs4
import requests

from website.website3 import join_url

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
        "Cookie": "wdcid=2a775bff15bb14aa; wdlast=1705728771; arialoadData=true; ariawapChangeViewPort=false",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }
    html = requests.get("https://www.piyao.org.cn/jrpy/index.htm", headers=header).text.encode('gbk', 'ignore')
    html = bs4.BeautifulSoup(html, 'html.parser')
    a = html.find_all("a", {"target": "_blank"})
    urls = []
    for i in a:
        if i.get("href").startswith("http"):
            urls.append(i.get("href"))
        else:
            urls.append(join_url(i.get("href")))
    with open("./content4.json", "w+", encoding="utf-8") as f:
        keywords = []
        order = 1000

        for i in urls:
            print(i)
            htm = requests.get(i, headers=header).content
            htm = bs4.BeautifulSoup(htm, 'html.parser')
            p = htm.find_all("p")

            # for j in p:
            #     print(j.get_text())
            def getMainText(start):
                end = len(p)
                while start < end:
                    text = p[start].get_text()
                    if text is not None:
                        if text == "":
                            start += 1
                            continue
                        text = (text
                                .replace(" ", "", 1000)
                                .replace(" ", "", 1000)
                                .replace("\n", "")
                                .replace(" ", "", 100))
                        if (text.startswith("谣言") or
                                text.startswith("误区") or
                                text.startswith("真相")):
                            return {
                                "text": text,
                                "newIndex": start
                            }
                    start += 1
                return None

            s = 0
            while s < len(p):
                t = getMainText(s)
                if t is not None:
                    yaoyan = t["text"]
                    s = t["newIndex"]
                    real_ = getMainText(s + 1)
                    if real_ is not None:
                        real = real_["text"]
                        s = real_["newIndex"]
                        keywords.append({
                            "keyword_order": f"{order}",
                            "keyword": yaoyan[3:],
                            "real": real[3:]
                        })
                        order += 1
                s += 1

            sleep(2)

        json.dump(keywords, f, ensure_ascii=False, indent=4)
