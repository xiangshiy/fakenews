import json
import  csv
import re

data_filename="fact/data.json"
# txt_filename= "fact/fact2.json"
# txt_filename= "fact/fact2.json"
txt_filename= "fact/main.json"
spo_set = []
with open(data_filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

if data:
    for i in data:
        spo_set.append(i)

keywords_to_check = [
    "综上所诉", "证据不足", "有网传消息称", "近日", "近期", "综上"
]

with open(txt_filename, 'r', encoding='utf-8') as f:
    data1 = json.load(f)
# 遍历data中的每个条目，并提取real字段的值
for item in data1:
    real_content = item.get('content')  # 假设real是字典中的一个键
    if real_content:
        sentences = real_content.split('。')
        for sentence in sentences:
            # 去除空白字符和换行符
            sentence = sentence.strip()
            # 排除空句子和包含特定关键词的句子
            sentence = re.sub(r'<[^>]*>', '',sentence)
            if sentence and not any(keyword in sentence for keyword in [
                "综上所诉", "证据不足", "有网传消息称", "近日", "近期", "综上"
            ]):
                # 如果句子不在set中，则添加
                if sentence not in spo_set:
                    spo_set.append(sentence)

with open(data_filename, 'w', encoding='utf-8') as f:
    json.dump(spo_set, f, ensure_ascii=False, indent=4)