import  json
import  csv
from docarray import Document, DocumentArray
news = []
label=[]
news_array=[]
empty=[]
from clip_client import Client

c = Client('grpc://127.0.0.1:51000')
with open('news/news.json', 'r', encoding='utf-8') as json_file:
    news_data = json.load(json_file)
    for item in news_data:
        news.append(item["ocr"])
        label.append(item["annotation"])
# print(len(news))
# print(len(label))
# news_array.append(news)
batch_size = 50

# 使用循环来分割 news 并编码每个批次
# for i in range(0, len(news), batch_size):
#     # 获取当前批次的内容，注意切片操作是左闭右开的
#     batch = news[i:i + batch_size]
#     # if not batch:
#     # 对当前批次进行编码
#     not_enpty=[]
#     for item in batch:
#         if item is not None:  # 假设非空或非None是要检查的条件
#             # 对当前项进行编码
#             not_enpty.append(item)
#
#     encoded_item = c.encode(not_enpty)  # 注意这里将item放在一个列表中传递给c.encode
#     news_array.append(encoded_item)
    # test = c.encode(batch)
    #
    # # 将编码后的结果追加到 news_array 中
    # news_array.append(test)
for i in range(0, len(news), batch_size):
    # 获取当前批次的内容
    batch = news[i:i + batch_size]
    batch_labels = label[i:i + batch_size]  # 获取当前批次对应的标签
    num=i
    # 遍历当前批次的每个元素
    for item, item_label in zip(batch, batch_labels):
        try:
            # 尝试对OCR文本进行编码
            embedding = c.encode([item])
            # 如果编码成功，则创建一个Document对象并添加到news_array中
            news_array.append(embedding[0])  # 假设c.encode返回的是一个列表，我们取第一个元素作为嵌入
            num+=1
        except Exception as e:
            # 如果编码失败，则打印错误并从news和label中删除对应的元素
            print(f"Failed to encode OCR text for item: {e}")
            # print(i)
            news.pop(num)  # 从news中删除当前元素
            label.pop(num)  # 从label中删除当前元素
            empty.append(num)
            # 因为我们删除了一个元素，所以下一个元素现在位于当前索引，所以不需要增加i
            # 但我们需要减少batch_size，因为我们少处理了一个元素
            # batch_size -= 1
            # 注意：这会影响循环的迭代次数，因为我们现在少了一个元素要处理
            # 如果batch_size变为0，那么我们应该退出当前的for循环迭代
            num+=1
           # if not batch:
   #     # 如果当前批次没有有效文档，可以跳过或记录一个警告
   #     continue
   # # 对当前批次进行编码
   # test = c.encode(batch)
   # # 将编码后的结果追加到 news_array 中
   # news_array.append(test)

import pickle

# 假设 news_array 是你想要保存的数组
# news_array = ...  # 这里应该是你的编码后的数组

# 使用pickle将数组保存到文件
with open('news_array.pkl', 'wb') as f:
    pickle.dump(news_array, f)
with open('news_label.pkl', 'wb') as f:
    pickle.dump(label, f)
separator=''
with open('news.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # 创建一个csv writer对象
    writer = csv.writer(csvfile)

    # 遍历news列表中的每个子列表
    for sublist in news:
        # 将子列表中的所有元素拼接成一个字符串
        concatenated_string = separator.join(sublist)

        # 将拼接后的字符串作为一行写入CSV文件
        # 注意：这里实际上是在写入一个字段，而不是多个字段
        writer.writerow([concatenated_string])
with open('empty.csv', 'w', newline='') as csvfile:
    # 创建一个csv writer对象
    writer = csv.writer(csvfile)

    # 写入空列表（作为一行或多行，取决于你的需求）
    # 如果想写入一个空行，你可以传递一个空列表
    writer.writerow(empty)

