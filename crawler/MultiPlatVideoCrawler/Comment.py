# comment类
class Comment:
    # 评论文本
    text = None
    # 视频id
    aweme_id = None

    def __init__(self, text, aweme_id):
        self.text = text
        self.aweme_id = aweme_id

    def __eq__(self, other):
        return self.text == other.text and self.aweme_id == other.aweme_id

    def __hash__(self):
        return hash(self.text + self.aweme_id)

    def __str__(self):
        return '{"aweme_id":' + self.aweme_id + "," + str(self.text) + "}"
