import logging
import pyautogui
import os
import time

from MultiPlatVideoCrawler.conf.config import PROJECT_PATH
# from conf.config import PROJECT_PATH

class AutoSlider:

    platform_url = {
        "kuaishou": "https://www.kuaishou.com/",
        "douyin": "https://www.douyin.com/"
    }

    def __init__(self, platform: str) -> None:

        # 自动 防故障功能
        pyautogui.FAILSAFE = False

        # 自动延迟
        pyautogui.PAUSE = 1

        self.platform = platform

        # 打开浏览器
        self.open_browser("Firefox")

        # 打开代理
        self.start_mitmdump()

        # 搜索
        self.search("假新闻")

    def open_browser(self, browser_name: str) -> None:
        """
        打开浏览器
        @param browser_name: 浏览器名称(Chrome, Firefox, Edge)
        """
        # 打开浏览器
        if browser_name not in ("‘Chrome", "Firefox", "Edge"):
            os.system(f'start Firefox --proxy-server=127.0.0.1:8080 --new-window {self.platform_url[self.platform]}')
            return None
        os.system(f'start {browser_name} --proxy-server=127.0.0.1:8080 --new-window {self.platform_url[self.platform]}')

    @staticmethod
    def start_mitmdump(port=8080, script_path="F:\大创准备\大创准备1\crawler\crawler\Proxy.py") -> None:
        """
        启动mitmdump
        @param port: 端口号
        @param script_path: 脚本路径
        """
        # 打开抓包工具
        os.system(f"start {PROJECT_PATH}\RunProxy.bat")

    def search(self, keyword: str) -> None:
        """
        在平台中搜索
        @param keyword: 搜索关键字
        """
        # 找到输入框的位置
        location = pyautogui.locateCenterOnScreen(
            f'screenshot/{self.platform}InputBox.png',
            confidence=None
        )

        while location is None:
            location = pyautogui.locateCenterOnScreen(
                f'screenshot/{self.platform}InputBox.png'
            )

            logging.info(pyautogui.position())
        pyautogui.click(location.x, location.y, 1)
        time.sleep(2)

        # 将输入法切换为中文
        pyautogui.hotkey('shift', 'alt')

        # 输入搜索内容
        pyautogui.typewrite(keyword)
        pyautogui.press('space')
        pyautogui.press('enter')
