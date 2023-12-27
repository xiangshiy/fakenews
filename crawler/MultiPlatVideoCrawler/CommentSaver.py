import json
from json import JSONDecoder
from typing import Type

from conf.config import PROJECT_PATH
from utils.log import log_warn


class CommentSaver:

    def __init__(self, video_id, comment):
        self.video_id = video_id
        self.comments = comment
        self.save_path = f"F:\大创准备\大创准备1\crawler\comment\\{video_id}.json"
        self.comment_num = 0

    def save(self):
        with open(self.save_path, "w+") as f:
            json.loads(str(self))
            json.dump(json.loads(str(self)), f)

        log_warn(f"保存评论{self.save_path}.json成功")

    def __str__(self):
        ret = "{" + f'"aweme_id":"{self.video_id}",' + \
              '"comments":['
        for comment in self.comments:
            ret += f'"{comment}",'
        ret = ret[:len(ret) - 1]
        ret += "]}"
        return ret
