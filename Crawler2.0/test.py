# import time
#
# from selenium import webdriver
#
# from MultiPlatVideoCrawler.conf.config import Profile_dir
#
# # 添加保持登录的数据路径：安装目录一般在C:\Users\user\AppData\Local\Google\Firefox\User Data
# profile = webdriver.FirefoxProfile(Profile_dir)
# # 驱动选项
# option = webdriver.FirefoxOptions()
# # 解除自动化控制标记
# option.add_argument("--disable-blink-features=AutomationControlled")
# option.profile = profile
# driver = webdriver.Firefox(options=option)
# # 最大化
# driver.maximize_window()
# # 请求
# driver.get(f"https://www.kuaishou.com/search/video?searchKey=都是股份合计")
# time.sleep(5)
# driver.get(f"https://www.kuaishou.com/search/video?searchKey=合计")
a = '{"a": "b"}'
b = eval(a)
print(b["a"])
