"""
删除空评论以及对应的视频
"""
import json
import os

# 1.获取数据路径
dataPath = "..\\data-kuaishou"
# 2.获取该目录下所有文件夹
dirs = os.listdir(dataPath)
# 3.遍历文件夹
for dir_ in dirs:
    # print(dir_)
    # 4.获取文件夹路径
    dirPath = os.path.join(dataPath, dir_)
    # 5.遍历评论文件夹
    commentPath = os.path.join(dirPath, "comments")
    # 空评论视频id列表
    emptyCommentVideoIdList = []
    for file in os.listdir(commentPath):
        # print(file)
        # 6.获取文件路径
        filePath = os.path.join(commentPath, file)
        # 7.读取文件
        with open(filePath, "r", encoding="utf-8") as f:
            comment = json.load(f)
            if int(comment["count"]) == 0:
                emptyCommentVideoIdList.append(comment["aweme_id"])
    # 8.获取视频文件夹
    videoPath = os.path.join(dirPath, "video")

    for videoId in emptyCommentVideoIdList:
        print(videoId)
        # 9.删除视频文件
        videoFilePath = os.path.join(videoPath, videoId + ".mp4")
        os.remove(videoFilePath)
        # 10.删除评论文件
        commentFilePath = os.path.join(commentPath, videoId + ".json")
        os.remove(commentFilePath)



