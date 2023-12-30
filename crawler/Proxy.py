import mitmproxy

from MultiPlatVideoCrawler.AutoSlider import AutoSlider

mitmproxy.ctx.log("start load......!", "warn")
# obj = AutoSlider("douyin")
obj = AutoSlider("kuaishou")
addons = [obj]
obj.response(None)
mitmproxy.ctx.log("proxy is running!", "warn")

