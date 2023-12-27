import mitmproxy
import json
import re

# 生成判断url中是否包含comment的正则表达式
comment_url = re.compile("^https://www\.douyin\.com/aweme/v1/web/comment/list/")
def response(flow):
    if comment_url.match(flow.request.url):
        json_data = json.loads(flow.response.get_text())
        mitmproxy.ctx.log.info(json_data['comments'])
        with open("comment.json", "a+", encoding="utf-8") as f:
            f.write(json.dumps(json_data['comments'], ensure_ascii=False,indent=4))
            