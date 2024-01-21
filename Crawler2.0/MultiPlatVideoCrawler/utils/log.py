# 打印测试函数
import mitmproxy


def log_warn(text): mitmproxy.ctx.log(text, "warn")


def log_INFO(info): mitmproxy.ctx.log("[INFO] " + info, "warn")
