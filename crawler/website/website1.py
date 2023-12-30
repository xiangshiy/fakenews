import requests
import re
import json
import jieba
from MultiPlatVideoCrawler.conf.config import PROJECT_PATH

if __name__ == '__main__':
    header = {
        "Host": "api.factpaper.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "lang": "zh",
        "Content-Length": "38",
        "Origin": "https://www.factpaper.cn",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers"
    }
    url = "https://api.factpaper.cn/fact-check/front/proveList"

    data = {"pageNum": 1, "pageSize": 450, "status": 1}
    response = requests.post(url, headers=header, data=json.dumps(data))
    with open(f"{PROJECT_PATH}\keywords\keywords.json", "a+", encoding="utf-8") as f:
        cc = []
        keyword = []
        for item in json.loads(response.text)["data"]["list"]:
            print(item['title'], item['proveId'])
            # f.writelines(item['title'][3:] + "\r")
            keyword.append({
                "keyword_order": item['proveId'],
                "keyword": item['title'][3:]
            })
            host = "https://api.factpaper.cn/fact-check/front/proveInfo"
            header = {
                "Host": "api.factpaper.cn",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/json",
                "lang": "zh",
                "Content-Length": "17",
                "Origin": "https://www.factpaper.cn",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "TE": "trailers"
            }
            data = {"proveId": item['proveId']}
            try:
                a = json.loads(
                    requests.post(host, headers=header, data=json.dumps(data)).text.encode('gbk', 'ignore').decode('gbk'))[
                    'data']
            except requests.exceptions.ConnectTimeout as e:
                continue
            c = a['checkInfoList'][0]['content'][str(a['checkInfoList'][0]['content']).find("综上所述"):-4]
            cc.append({
                "title": item['title'],
                "proveId": item['proveId'],
                "content": c,
                "finalResult": a['finalCheckInfo']['finalResult'],
            })
        json.dump(keyword, f, indent=4, skipkeys=True, ensure_ascii=False)
        with open("./content/content1.json", "a+", encoding="utf-8") as fi:
            json.dump(cc, fi, indent=4, skipkeys=True, ensure_ascii=False)


