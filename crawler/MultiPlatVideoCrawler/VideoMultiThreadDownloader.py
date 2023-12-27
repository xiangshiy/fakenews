import collections
import threading
import mitmproxy
import requests
from threading import Thread


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

    def download_control(self, option: str, /, video: tuple = None):
        # 创建锁
        lock = threading.RLock()
        # 加锁
        lock.acquire()
        # 下载任务
        if "download" == option:
            # 判断线程池的任务数是否达到上限
            if self.free_thread_num == 0:
                # 将任务添加到任务队列末尾
                self.video_download_task.append(video)
            else:
                # 线程池中的线程数减1
                self.free_thread_num -= 1
                # 异步执行下载任务
                Thread(target=self.download_video,
                       args=(video,)).start()
        # 下载结束
        elif option == "finish":
            # 线程池中的线程数加1
            self.free_thread_num += 1
            # 判断任务队列是否为空
            if len(self.video_download_task) != 0:
                # 线程池中的线程数减1
                self.free_thread_num -= 1

                # 从任务队列中取出任务
                Thread(target=self.download_video,
                       args=(self.video_download_task.popleft())).start()
        # 释放锁
        lock.release()

    def download_video(self, video: tuple):
        """
        下载视频
        @param video: 视频链接元组(视频id, 视频链接)
        """
        # 创建锁
        lock = threading.RLock()
        # 加锁
        lock.acquire()

        order = self.video_order
        self.video_order += 1

        # 释放锁
        lock.release()

        # 下载视频
        with open(f"{self.save_path}\\{self.platform}\\{video[0]}.mp4", "wb+") as f:
            f.write(requests.get(video[1]).content)
            mitmproxy.ctx.log(
                f"下载视频{self.platform}_video_{order}.mp4成功",
                "warn")

        # 下载结束，通知下载控制器
        self.download_control("finish")
