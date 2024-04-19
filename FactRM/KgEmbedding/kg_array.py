import json
from fuzzywuzzy import fuzz
import  pickle
# 读取entity.json中的数据
entity_data = []
with open('entity.json', 'r', encoding='utf-8') as jsonfile:
    # for line in jsonfile:
    #     entity_data.append(json.loads(line.strip()))
    data1=json.load(jsonfile)
print(len(data1))
#读取all_ent.txt中的数据，构建字典{id: 实体1}
all_entities = {}
with open('data/all_ent.txt', 'r', encoding='utf-8') as entfile:
    for line in entfile:
        data = line.strip().split('  ')
        all_entities[data[0]] = data[1]

# 进行相似度对比并存入kg_narry中
kg_narry = []
from fuzzywuzzy import fuzz

for entities in data1:
    found = False  # 使用 found 变量来标记是否找到匹配的实体
    if not entities:  # 检查 entities 是否为空
        kg_narry.append('1')
    else:
        for entity in entities:
            if not found:
                # 第一次遍历使用70作为阈值
                for ent_id, ent_name in all_entities.items():
                    similarity = fuzz.ratio(entity, ent_name)
                    if similarity >= 90:
                        kg_narry.append(ent_id)
                        found = True
                        break
            if not found:
                # 如果没有找到，降低阈值到50再次遍历
                for ent_id, ent_name in all_entities.items():
                    similarity = fuzz.ratio(entity, ent_name)
                    if similarity >= 80:
                        kg_narry.append(ent_id)
                        found = True
                        break
            if not found:
                # 如果没有找到，降低阈值到50再次遍历
                for ent_id, ent_name in all_entities.items():
                    similarity = fuzz.ratio(entity, ent_name)
                    if similarity >= 60:
                        kg_narry.append(ent_id)
                        found = True
                        break
            if not found:
                # 如果没有找到，降低阈值到50再次遍历
                for ent_id, ent_name in all_entities.items():
                    similarity = fuzz.ratio(entity, ent_name)
                    if similarity >= 40:
                        kg_narry.append(ent_id)
                        found = True
                        break
            if not found:
                # 如果没有找到，降低阈值到50再次遍历
                for ent_id, ent_name in all_entities.items():
                    similarity = fuzz.ratio(entity, ent_name)
                    if similarity >= 20:
                        kg_narry.append(ent_id)
                        found = True
                        break

# 确保不会重复添加同一个实体

print(len(kg_narry))
# print(kg_narry)
with open('kg_array.pkl', 'wb') as f:
    pickle.dump(kg_narry, f)
