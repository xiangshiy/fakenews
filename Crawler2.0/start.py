import os

from MultiPlatVideoCrawler.conf.config import PROJECT_PATH, ProxyFilePath


def start_mitmdump(port=8080) -> None:
    """
    启动mitmdump
    @param port: 端口号
    """
    # 打开抓包工具
    with open(f"{PROJECT_PATH}\RunProxy.bat", 'w') as f:
        f.write(f"mitmdump -p {port} -s {ProxyFilePath} --flow-detail 0")
    os.system(f"start {PROJECT_PATH}\RunProxy.bat")


if __name__ == "__main__":
    start_mitmdump()


