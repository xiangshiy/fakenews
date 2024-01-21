import random
import re
import json
import threading

import mitmproxy.ctx
import MultiPlatVideoCrawler.VideoMultiThreadDownloader as VideoMultiThreadDownloader
from urllib.parse import urlparse, parse_qs

from MultiPlatVideoCrawler.CommentSaver import CommentSaver
# from MultiPlatVideoCrawler.conf.config import
from MultiPlatVideoCrawler.utils.log import log_warn

"""
flow.request.scheme  请求协议
flow.request.host    请求host
flow.request.url     请求URL链接
flow.request.method  请求方法
flow.request.query   请求URL查询参数
flow.request.path    请求URL https://www.baidu.com/
flow.request.path_components  #请求URL不包含域名的元祖 ('project', 'classify', 'list')
flow.request.urlencoded_form  请求POST数据
flow.response.status_code  HTTP响应状态码
flow.response.headers    HTTP响应头信息
flow.response.get_text   HTTP响应内容
"""

# 初始化抖音下载器
douyin_downloader = VideoMultiThreadDownloader.VideoMultiThreadDownloader(
    "VideoSavePath",
    "douyin", 10)

# 初始化快手下载器
# kuaishou_downloader = VideoMultiThreadDownloader.VideoMultiThreadDownloader(
#     VideoSavePath,
#     "kuaishou", 10)

# 生成判断url中是否包含comment的正则表达式
comment_url = re.compile("^https://www\.douyin\.com/aweme/v1/web/comment/list/")
video_list_url = re.compile("^https://www\.douyin\.com/aweme/v1/web/general/search/single/")
comment_tem = {
    "aweme_id": "a",
    "comment": [
        {
            "text": "",
            "digg_count": 12
        },
        {
            "text": "",
            "digg_count": 12
        }
    ]
}


def response(flow):
    # 判断是否满足评论url
    if comment_url.match(flow.request.url):

        # 格式转换
        json_data = json.loads(flow.response.get_text())

        # comment_list
        comment_list = []
        aweme_id = json_data['comments'][0]['aweme_id']

        # 迭代存储
        for comment_data in json_data['comments']:
            # 评论文本
            # 视频id
            # 点赞数
            comment_list.append({
                "text": comment_data['text'],
                "digg_count": comment_data['digg_count']
            })
        CommentSaver(aweme_id, {
                                        "aweme_id": aweme_id,
                                        "comment": comment_list,
                                        "count": len(json_data['comments'])
                                        }).save()
    elif video_list_url.match(flow.request.url):
        # 格式转换
        print(flow.request.url)
        json_data = json.loads(flow.response.get_text())['data']
        for v in json_data:
            vid = v['aweme_info']['aweme_id']
            url_list = v['aweme_info']['video']['download_addr']['url_list']
            for url in url_list:
                log_warn(url)
                try:
                    douyin_downloader.download_control("download", (vid, url))
                except Exception as e:
                    log_warn(f'{url} failed!!')
                else:
                    break
