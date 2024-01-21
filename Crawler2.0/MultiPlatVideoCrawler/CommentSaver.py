import json

from MultiPlatVideoCrawler.utils.log import log_warn


class CommentSaver:

    def __init__(self, video_id, comment, save_path):
        self.video_id = video_id
        self.comments = comment
        self.save_path = save_path

    def save(self):
        with open(f"{self.save_path}\\{self.video_id}.json", "w+", encoding="utf-8") as f:
            # json.loads(str(self))
            json.dump(self.comments, f, indent=4, skipkeys=True, ensure_ascii=False)

        log_warn(f"保存评论{self.video_id}.json成功")
