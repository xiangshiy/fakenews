# 项目名
import os

# 磁盘名
DiskName = __file__[0]
# 项目路径
PROJECT_PATH = os.path.abspath(__file__)[0:-37]
# 代理文件路径
ProxyFilePath = f"{PROJECT_PATH}\Proxy.py"
# 数据保存路径
DouYinDataSavePath = f"{PROJECT_PATH}\data-douyin"
KuaiShowDataSavePath = f"{PROJECT_PATH}\data-kuaishou"
# 浏览器用户文件路径
# --------------只改这个-------------------
Profile_dir = r"C:\Users\CHALN\AppData\Roaming\Mozilla\Firefox\Profiles\bl883mpl.default-release-1"
