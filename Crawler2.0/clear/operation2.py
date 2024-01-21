"""
删除空视频
"""
import os
import numpy as np
import shutil
import json

# 1.获取数据路径
dataPath = "..\\data-kuaishou"
# 2.获取该目录下所有文件夹
dirs = os.listdir(dataPath)
# 3.遍历文件夹
for dir_ in dirs:
    # print(dir_)
    # 4.获取文件夹路径
    dirPath = os.path.join(dataPath, dir_)
    # 5.获取视频文件夹
    videoPath = os.path.join(dirPath, "video")
    # 6.遍历视频文件夹
    for file in os.listdir(videoPath):
        # print(file)
        # 7.获取文件路径
        filePath = os.path.join(videoPath, file)
        # 8.读取视频文件大小
        fileSize = os.path.getsize(filePath)
        # 9.判断视频文件大小
        if fileSize == 0:
            # 10.删除视频文件
            os.remove(filePath)
            # 11.删除评论文件
            commentPath = os.path.join(dirPath, "comments")
            commentFilePath = os.path.join(commentPath, file.split(".")[0] + ".json")
            try:
                os.remove(commentFilePath)
            except FileNotFoundError:
                print("FileNotFoundError")
            print(file, fileSize)
            print(commentFilePath)
            print(filePath)
            print("=="*20)
            # 12.删除文件夹
            # shutil.rmtree(dirPath)
            # break
