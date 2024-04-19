"""
1. 定义DBPDataset类表示数据集,重写__getitem__方法返回三元组。
2. 定义KGEmb模型表示知识图谱Embedding,包含实体与关系Embedding层。
3. 构建DataLoader加载数据集,定义优化器与TransE损失函数进行训练。
4. 训练结束后,ent_emb与rel_emb分别为实体与关系Embedding结果。
5. 将模型参数保存为model.pkl文件,用于重新加载模型。
"""
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from scipy.spatial.distance import cosine
import  pickle

# 加载数据集
class DBPDataset(Dataset):
    def __init__(self, data_path):
        triples = []
        with open(data_path) as f:
            for line in f:
                head, rel, tail = line.strip().split()
                triples.append((int(head), int(rel), int(tail)))
        self.triples = triples

    def __len__(self):
        return len(self.triples)

    def __getitem__(self, idx):
        head, rel, tail = self.triples[idx]
        # 将输入的头实体head,关系rel和尾实体tail构建成pytorch的LongTensor类型。
        return torch.LongTensor([head, rel, tail])


# Embedding模型
class KGEmb(nn.Module):
    def __init__(self, n_ent, n_rel, dim=100):
        """
        :param n_ent: 实体的总数,即数据集中不重复的实体数量。
        :param n_rel: 关系的总数,即数据集中不重复的关系数量。
        :param dim: Embedding的维度,即每个实体/关系的向量表示长度。
        """
        super().__init__()
        self.ent_emb = nn.Embedding(n_ent, dim)
        self.rel_emb = nn.Embedding(n_rel, dim)

    def forward(self, x):
        """
        :param x:
        :return:头实体Embedding、关系Embedding和尾实体Embedding。
        """
        head, rel, tail = x[:, 0], x[:, 1], x[:, 2]
        head_emb = self.ent_emb(head)
        rel_emb = self.rel_emb(rel)
        tail_emb = self.ent_emb(tail)
        return head_emb, rel_emb, tail_emb


# 训练代码
dataset = DBPDataset('./data/index_rel_triple.txt')
# 设置固定的随机种子,使每次初始化产生的随机参数相同
torch.manual_seed(123)
model = KGEmb(n_ent=5360, n_rel=1809)

"""
1. Adam优化器更新Embedding使loss下降
2. DataLoader生成batch数据输入模型
3. 打乱数据顺序使模型泛化能力提高
"""
# 使用Adam优化器,对模型中的所有可训练参数进行更新，通过model.parameters()获得模型的所有可训练参数(Embedding)
opt = torch.optim.Adam(model.parameters())
# 使用DataLoader加载dataset数据集，每批数据大小为8192条三元组，shuffle=True:每个epoch打乱数据顺序
loader = DataLoader(dataset, batch_size=500, shuffle=True)

for epoch in range(200):
    """
    opt.zero_grad() 的作用是:清空优化器opt中保存的梯度值。
    每一次的 loss.backward() 都会累加当前的梯度到已经存储的梯度值。如果不清空梯度,梯度就会不断累加,最终的梯度值错误。
    所以,在每次迭代(每个batch)开始之前,需要调用 opt.zero_grad() 清空优化器中的梯度值,确保本次迭代计算的梯度值正确。
    """
    for step, x in enumerate(loader):
        opt.zero_grad()
        h, r, t = model(x)
        loss = torch.sum(h + r - t)  # TransE损失函数
        loss.backward()  # 反向传播,计算梯度值
        opt.step()  # 优化器更新参数

# ent_emb:
# - 行数为实体总数n,列表示每个实体的Embedding
# - 列数为Embedding维度d,一般在50到200之间
# - 所以ent_emb的shape为[n, d],是一个n行d列的矩阵
# - 可以通过ent_emb[ent]访zzei
# rel_emb:
# - 行数为关系总数m,列表示每个关系的Embedding
# - 列数同样为Embedding维度d
# - 所以rel_emb的shape为[m, d],是一个m行d列的矩阵
# - 可以通过rel_emb[rel]访问第rel个关系的Embedding向量
# NumPy矩阵是一种用于科学计算的二维数组,支持各种矩阵运算与操作
# 得到Embedding结果，ent_emb:实体Embedding矩阵(numpy类型)，rel_emb:关系Embedding矩阵(numpy类型)
ent_emb = model.ent_emb.weight.detach().numpy()
# 创建一个文件对象以写入 pkl 文件
with open('./data/ent_attr_kg_transe.pkl', 'wb') as f:
    # 使用 pickle 的 dump 函数将 ent_emb 保存到文件中
    pickle.dump(ent_emb, f)
rel_emb = model.rel_emb.weight.detach().numpy()

# 保存的不仅仅是Embedding权重,还包括优化器状态,超参数等信息。当我们重新加载这个模型时,它的全部变量都会恢复到保存时的状态,可以直接使用或继续训练。
torch.save(model.state_dict(), './data/model.pkl')  # 保存模型

ent1_emb = ent_emb[4]  # 实体ent1的Embedding
ent2_emb = ent_emb[10]  # 实体ent2的Embedding
sim = cosine(ent1_emb, ent2_emb)  # 两个实体的相似度
"""
- sim > 0.8 : 两个实体语义非常相似,可以认为实体1和实体2表达相同或相近的概念。
- 0.5 < sim < 0.8 : 两个实体语义较相似,在某种程度上表达相近的概念,但也有一定差异。 
- 0.3 < sim < 0.5 : 两个实体语义一般,既有一定相似度但差异也比较大。表达的概念只是有部分重叠或相关。
- sim < 0.3 : 两个实体语义不太相似,差异较大。表达的概念有较大差异。
"""
print(sim)
