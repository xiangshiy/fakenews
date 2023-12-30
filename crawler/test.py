# import json
# import re
#
# import mitmproxy.ctx
# from mitmproxy.coretypes.multidict import MultiDictView
#
# kuaishou_request_url = re.compile("^https://www\.kuaishou\.com/graphql")
#
#
# def response(flow):
#     if kuaishou_request_url.match(flow.request.url):
#         # mitmproxy.ctx.log(str(flow.request.content), "warn")
#         # flow.request.urlencoded_form.fields
#         # MultiDictView()
#         queryData = json.loads(flow.request.content)
#         if queryData['operationName'] == "commentListQuery":
#             # 格式转换
#             json_data = json.loads(flow.response.get_text())['data']
#         elif queryData['operationName'] == "visionSearchPhoto":
#             # 格式转换
#             video_list = json.loads(flow.response.get_text())['data']['visionSearchPhoto']['feeds']
#             for v in video_list:
#                 try:
#                     video = v['photo']
#                     # try:
#                     #     self.douyin_downloader.download_control("download", (video['id'], video['photoUrl']))
#                     # except Exception:
#                     #     log_warn(f'a failure!!')
#                     mitmproxy.ctx.log(str((video['id'], video['photoUrl'])),  "warn")
#
#                 except KeyError as e:
#                     print(e)
#                     continue
import os

# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# # os.mkdir('./a')
# # os.mkdir('./a')
# driver = webdriver.Firefox()
# driver.get("https://baidu.com")
# driver.find_element(By.XPATH,"//div/div/div/span/div/a")
P = os.path.abspath(__file__)
print(P)