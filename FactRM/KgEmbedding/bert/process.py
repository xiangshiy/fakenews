from transformers import BertTokenizer, BertModel
import torch


# 假设你已经有了清洗后的文本
cleaned_text = "微笑大将格拉西莫夫回来了由普京黑海舰队护送灵枢回来了俄军大将格拉西莫夫回来了从塞凡堡运送到了俄战比尔江斯克市全程由俄军黑海舰队护送肃杀之气这下总算搞明百了都是故意为之调虎离山一切都是为了今天格拉西莫夫的尺体是的他回来了能够顺利转移安全着陆难怪俄军自前依旧不承认是乌军击落了自家的飞机普京刻意为一具户体去损失总共约10亿美金的两架飞机moeiranut兄弟情深Or一切都是秘密进行地堡勇士普丁果然是个有情有义的人丢掉了约10亿美金但是接回来的却是一具无头户体AS687中中馨格拉西莫夫回来了快影×照快今天俄军大将微笑男孩格拉西莫夫的灵鹫Dkwpnp"

# 初始化BERT分词器和模型
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# 对文本进行分词和编码
encoded_input = tokenizer(cleaned_text, return_tensors='pt', padding=True, truncation=True, max_length=512)

# 获取BERT模型的输出
with torch.no_grad():
    output = model(**encoded_input)

# 提取特征向量（通常是CLS token的嵌入）
feature_vector = output.last_hidden_state[:, 0, :]
print(feature_vector)
