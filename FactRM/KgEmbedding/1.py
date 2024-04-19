# import  pickle
# import  numpy as np
# with open('news_label.pkl', 'rb') as f:
#     # 使用pickle.load()反序列化对象
#     data3= pickle.load(f)
# empty_indices = []  # 保存空元素的索引
#
# # 遍历列表找出空元素的索引并保存
# for i, element in enumerate(data3):
#     if element=="":  # 如果元素为空
#         empty_indices.append(i)
#
# # 删除空元素
# for index in reversed(empty_indices):  # 从后向前遍历索引，以避免删除元素后索引的偏移问题
#     del data3[index]
# array3 = np.array(data3)
# print(array3.shape)
# with open('news_array1.pkl', 'wb') as f:
#     pickle.dump(data3, f)
# # 打印结果
import csv
from clip_client import Client
import  pickle
c = Client('grpc://127.0.0.1:51000')
csv_file_path = 'news.csv'  # 替换为你的 CSV 文件路径
news_array = []
with open(csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    # 逐行读取 CSV 文件并进行嵌入
    for row in csv_reader:
        a=c.encode(row)
        news_array.append(a[0])
print(len(news_array))
with open('news_array1.pkl', 'wb') as f:
    pickle.dump(news_array, f)
