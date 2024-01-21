import collections
import threading
import requests
from threading import Thread

from MultiPlatVideoCrawler.conf.config import VIDEO_MAX_NUM
from MultiPlatVideoCrawler.utils.log import log_warn


class VideoMultiThreadDownloader:
    # 空闲线程数
    free_thread_num = 0

    def __init__(self, save_path, platform, thread_num=10):
        super().__init__()

        self.video_order = 0
        self.video_download_task = collections.deque()
        self.save_path = save_path
        self.thread_num = thread_num
        self.free_thread_num = thread_num
        self.platform = platform
        self.video_num = 0
        header1 = {
            "Accept": "*/*",
            "Accept-Encoding": "identity;q=1, *;q=0",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "v26-web.douyinvod.com",
            "Origin": "https://www.douyin.com",
            "Range": "bytes=0-",
            "Referer": "https://www.douyin.com/",
            "Sec-Fetch-Dest": "video",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        header2 = {
            "Host": "v2.kwaicdn.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept": "video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Referer": "https://www.kuaishou.com/",
            "Range": "bytes=0-",
            "Origin": "https://www.kuaishou.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "video",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Accept-Encoding": "identity",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        if platform == 'douyin':
            self.header = header1
        else:
            self.header = header2

    def download_control(self, option: str, /, video_t: tuple = None):
        def download_video(video: tuple):
            """
            下载视频
            @param video: 视频链接元组(视频id, 视频链接)
            """

            # 下载视频
            with open(f"{self.save_path}\\{video[0]}.mp4", "wb+") as f:
                f.write(requests.get(video[1], headers=self.header).content)
                log_warn(
                    f"下载视频{video[0]}.mp4成功",
                )

            # 下载结束，通知下载控制器
            self.download_control("finish")

        # 创建锁
        lock = threading.RLock()
        # 加锁
        lock.acquire()
        # 下载任务
        if "download" == option and self.video_num < VIDEO_MAX_NUM:
            # 判断线程池的任务数是否达到上限
            if self.free_thread_num == 0:
                # 将任务添加到任务队列末尾
                self.video_download_task.append(video_t)
            else:
                # 线程池中的线程数减1
                self.free_thread_num -= 1
                # 异步执行下载任务
                Thread(target=download_video,
                       args=(video_t,)).start()
                self.video_num += 1

        # 下载结束
        elif option == "finish" and self.video_num < VIDEO_MAX_NUM:
            # 线程池中的线程数加1
            self.free_thread_num += 1
            # 判断任务队列是否为空
            if len(self.video_download_task) != 0:
                # 线程池中的线程数减1
                self.free_thread_num -= 1

                # 从任务队列中取出任务
                Thread(target=download_video,
                       args=(self.video_download_task.popleft(),)).start()
                self.video_num += 1
        # 释放锁
        lock.release()
