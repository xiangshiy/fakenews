from MultiPlatVideoCrawler.Comment import Comment


class DataSet:

    def __init__(self, _vid, url, comments: list[Comment] = None):
        self._vid = _vid
        self.url = url
        self.comments = comments

    def setComment(self, comments: list[Comment]):
        self.comments.extend(comments)

    def __str__(self):
        ret = "{" + f'"_vid":"{self._vid}",' + \
                    f'"url":"{self.url}",' + \
                    '"comments":['
        for i in self.comments:
            ret += str(i) + ","
        ret += "],}"
        return ret

