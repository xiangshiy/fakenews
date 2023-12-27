from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
# 添加保持登录的数据路径：安装目录一般在C:\Users\黄\AppData\Local\Google\Firefox\User Data
Profile_dir = r"C:\Users\prejudice\AppData\Roaming\Mozilla\Firefox\Profiles\kjm3b46u.default-release-1"
profile = webdriver.FirefoxProfile(Profile_dir)

option = webdriver.FirefoxOptions()
option.add_argument("--disable-blink-features=AutomationControlled")
option.profile = profile
gecko_driver_path = 'D:\Python\python3.11.4\geckodriver.exe'
#固定搭配直接用就行了
service = Service(executable_path=gecko_driver_path)
# 初始化driver
driver = webdriver.Firefox(options=option,service=service)
driver.get("https://www.douyin.com/")
driver.maximize_window()
