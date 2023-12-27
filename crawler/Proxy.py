import random
import re
import json
import threading

import mitmproxy.ctx
import MultiPlatVideoCrawler.VideoMultiThreadDownloader as VideoMultiThreadDownloader
from urllib.parse import urlparse, parse_qs

from MultiPlatVideoCrawler.CommentSaver import CommentSaver
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
    "F:\大创准备\大创准备1\crawler\\video",
    "douyin", 10)

# 初始化快手下载器
kuaishou_downloader = VideoMultiThreadDownloader.VideoMultiThreadDownloader(
    "F:\大创准备\大创准备1\crawler\\video",
    "kuaishou", 10)
douyin_host = ("v26-web.douyinvod.com", "v3-web.douyinvod.com", "v3-webc.douyinvod.com")

# 使用正则表达式判断是否有_rand参数
_rand_pattern = re.compile(r"__rand=\d+")


def request(flow):
    # 通过请求mime_type判断视频请求
    if "mime_type=video_mp4" in flow.request.url and _rand_pattern.search(flow.request.url) is None:
        mitmproxy.ctx.log(flow.request.url, 'warn')
        parsed_url = urlparse(flow.request.url)
        try:
            vid = parse_qs(parsed_url.query)['__vid'][0]
            log_warn(vid)
        except KeyError as e:
            vid = random.randint(1, 100000)
        douyin_downloader.download_control("download", (vid, flow.request.url))


# 生成判断url中是否包含comment的正则表达式
comment_url = re.compile("^https://www\.douyin\.com/aweme/v1/web/comment/list/")

# 评论集合
comment_collection = {}

last_aweme_id = None


def response(flow):
    # 判断是否满足评论url
    if comment_url.match(flow.request.url):

        # 格式转换
        json_data = json.loads(flow.response.get_text())

        # comment_list
        comment_list = []
        # 视频id
        aweme_id = json_data['comments'][0]['aweme_id']
        global last_aweme_id
        if last_aweme_id is None:
            last_aweme_id = aweme_id
        elif last_aweme_id != aweme_id:
            save_comment()
            last_aweme_id = aweme_id

        # 迭代存储
        for comment_data in json_data['comments']:
            # 评论文本
            comment = comment_data['text']
            # 视频id
            aweme_id = comment_data['aweme_id']
            # 点赞数
            digg_count = comment_data['digg_count']
            # 添加到评论集合
            comment_list.append(comment)
        if aweme_id not in comment_collection.keys():
            comment_collection[aweme_id] = comment_list
        else:
            comment_collection[aweme_id].extend(comment_list)


def save_comment():
    lock = threading.RLock()
    lock.acquire()
    for aweme_id in comment_collection.keys():
        # 保存评论
        comment_saver = CommentSaver(aweme_id, comment_collection[aweme_id])
        comment_saver.save()
    comment_collection.clear()
    lock.release()
