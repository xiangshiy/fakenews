import json
import re

from bs4 import BeautifulSoup as bs
import requests

from MultiPlatVideoCrawler.conf.config import PROJECT_PATH

header = {
    "Host": "chinafactcheck.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://chinafactcheck.com/",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://chinafactcheck.com",
    "Alt-Used": "chinafactcheck.com",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Content-Length": "0",
    "TE": "trailers"
}
PAGE_NUM = 2  # max 50

with open(f"{PROJECT_PATH}\keywords\keywords.json", "a+", encoding="utf-8") as f:
    keyword = []
    cc = []
    href = set()
    order = 0
    for page in range(1, PAGE_NUM + 1):
        url = f"https://chinafactcheck.com/?paged={page}"
        response = requests.get(url, headers=header)
        soup = bs(response.text, "html.parser")
        pattern = re.compile(r'<.*?>')

        post_title = soup.findAll("h2", {"class": "post-title"})

        post_title = bs(str(post_title), "html.parser")
        for i in post_title:
            if i == ' ': continue
            k = pattern.sub("", str(i)).replace("\n", '').replace('[', '').replace(']', "").replace(',', '')
            print(k)
            keyword.append({
                "keyword_order": f"{order}",
                "keyword": k
            })
            order += 1

        for a in soup.findAll("a", {"target": "_blank"}):
            # print(a['href'])
            href.add(a['href'])
    index = 0
    page = 1
    for b in href:
        if b.startswith("https://chinafactcheck.com/"):
            print(b)
            try:
                resp = requests.get(b, headers={
                "Host": "chinafactcheck.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://chinafactcheck.com/",
                "Alt-Used": "chinafactcheck.com",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "TE": "trailers"
            })
            except requests.exceptions.ReadTimeout as e:
                continue
            detail = bs(resp.text, "html.parser")
            conclusion = detail.findAll("div", {"class": "content-item content-conclusion"})
            conclusion = bs(str(conclusion), "html.parser")
            for i in conclusion:
                c = pattern.sub("", str(i)).replace("\n", '').replace('[', '').replace(']', "")
                try:
                    cc.append({
                        "title": keyword[index],
                        "proveId": f"{index}",
                        "content": c,
                        "finalResult": "",
                    })
                except IndexError as e:
                    continue
                index += 1
    json.dump(keyword, f, indent=4, skipkeys=True, ensure_ascii=False)
    with open("./content/content2.json", "a+", encoding="utf-8") as fi:
        json.dump(cc, fi, indent=4, skipkeys=True, ensure_ascii=False)
