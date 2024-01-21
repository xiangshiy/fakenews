"""
2. content1.JSON中搜索content为空的，重新进行爬取
"""
import json
import requests

# 1.读取content1.json
with open("./content/content1.json", "r", encoding="utf-8") as f:
    content = json.load(f)
    # 2.遍历content1.json
    for item in content:
        if item["content"] == "":
            # 3.重新爬取
            url = "https://api.factpaper.cn/fact-check/front/proveInfo"
            data = {"proveId": item["proveId"]}
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
            try:
                a = json.loads(
                    requests.post(url, headers=header, data=json.dumps(data)).text.encode('gbk', 'ignore').decode('gbk'))[
                    'data']
            except requests.exceptions.ConnectTimeout as e:
                continue
            c = a['checkInfoList'][0]['content'][str(a['checkInfoList'][0]['content']).find("综上所述"):-4]
            item["content"] = c
    # 4.保存content1.json
    with open("./content/content1.json", "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=4)