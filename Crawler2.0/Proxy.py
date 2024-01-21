import mitmproxy

from MultiPlatVideoCrawler.AutoSlider import AutoSlider
from MultiPlatVideoCrawler.utils.log import log_INFO

log_INFO("Start load....")
# obj = AutoSlider("douyin")
obj = AutoSlider("kuaishou")
addons = [obj]
obj.response(None)
log_INFO("Proxy is running!")
obj.response(None)



