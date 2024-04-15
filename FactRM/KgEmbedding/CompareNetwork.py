import torch
import torch.nn as nn
import torch.optim as optim
#
import pickle
# #定义对比网络模型
# class ContrastiveNetwork(nn.Module):
#     def __init__(self, input_dim):
#         super(ContrastiveNetwork, self).__init__()
#         self.fc = nn.Linear(input_dim, 512)
#
#     def forward(self, x1, x2):
#         out1 = torch.relu(self.fc(x1))
#         out2 = torch.relu(self.fc(x2))
#         return out1, out2
# #定义对比损失函数
# class ContrastiveLoss(nn.Module):
#     def __init__(self, margin=1.0):
#         super(ContrastiveLoss, self).__init__()
#         self.margin = margin
#
#     def forward(self, out1, out2, target):
#         euclidean_distance = torch.nn.PairwiseDistance()(out1, out2)
#         loss_contrastive = torch.mean((1 - target) * torch.pow(euclidean_distance, 2) +
#                                       (target) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))
#         return loss_contrastive
#
# #定义训练函数
# def train_contrastive_network(model, criterion, optimizer, source_vectors, target_vectors, labels, num_epochs=100):
#     for epoch in range(num_epochs):
#         optimizer.zero_grad()
#         out1, out2 = model(source_vectors, target_vectors)
#         loss = criterion(out1, out2, labels)
#         loss.backward()
#         optimizer.step()
#         if (epoch+1) % 10 == 0:
#             print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, loss.item()))
# # 假设source_vectors和target_vectors分别是文本中实体的BERT输出向量和知识图谱中实体的特征向量
#
# # source_vectors = torch.randn(100, 768)  # 假设BERT输出向量的维度为768
# # target_vectors = torch.randn(100, 300)  # 假设知识图谱嵌入向量的维度为300
# # labels = torch.randint(0, 2, (100,))    # 随机生成标签 0 或 1
# import  pickle
#
# with open('kg_array.pkl', 'rb') as f:
#     # 使用pickle.load()反序列化对象
#     data1 = pickle.load(f)
# with open('news_array.pkl', 'rb') as f:
#     # 使用pickle.load()反序列化对象
#     data2 = pickle.load(f)
# with open('news_label.pkl', 'rb') as f:
#     # 使用pickle.load()反序列化对象
#     data3 = pickle.load(f)
# # 初始化模型、损失和优化器
#
# kg_array1 = []
# # 遍历data1中的每个元素
# with open('data/ent_attr_kg_transe.pkl', 'rb') as f:
#     # 使用pickle.load()反序列化对象
#     kg = pickle.load(f)
# for item in data1:
#     item = int(item)
#     # 检查item是否在kg字典的键中
#     # if item in kg:
#         # 如果在，则将对应的值添加到kg_array1中
#     kg_array1.append(kg[item])
#     # else:
#     #     # 如果不在，可以选择忽略、记录错误或执行其他操作
#     #     print(f"Warning: Key '{item}' not found in the dictionary 'kg'.")
#
#     # 现在kg_array1包含了从kg字典中根据data1的键获取的所有值
# # print(len(kg_array1))
#
# # import numpy as np
# target_vectors = torch.tensor(kg_array1)
# source_vectors = torch.tensor(data2)
# labels = torch.tensor(data3)
# model = ContrastiveNetwork(512)  # 输入维度为512
# criterion = ContrastiveLoss()
# optimizer = optim.Adam(model.parameters(), lr=0.001)
#
# # 训练模型
# train_contrastive_network(model, criterion, optimizer, source_vectors, target_vectors, labels)


import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, recall_score, precision_score
import matplotlib.pyplot as plt

# Define contrastive network model
class ContrastiveNetwork(nn.Module):
    def __init__(self, input_dim_source, input_dim_target):
        super(ContrastiveNetwork, self).__init__()
        self.fc_source = nn.Linear(input_dim_source, 1024)
        self.fc_target = nn.Linear(input_dim_target, 1024)

    def forward(self, x1, x2):
        out1 = torch.relu(self.fc_source(x1))
        out2 = torch.relu(self.fc_target(x2))
        return out1, out2

# Define contrastive loss function
class ContrastiveLoss(nn.Module):
    def __init__(self, margin=1.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, out1, out2, target):
        euclidean_distance = torch.nn.PairwiseDistance()(out1, out2)
        loss_contrastive = torch.mean((1 - target) * torch.pow(euclidean_distance, 2) +
                                      (target) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))
        return loss_contrastive

# Define training function
def train_contrastive_network(model, criterion, optimizer, source_vectors, target_vectors, labels, num_epochs=500):
    losses = []
    for epoch in range(num_epochs):
        optimizer.zero_grad()
        out1, out2 = model(source_vectors, target_vectors)
        loss = criterion(out1, out2, labels)
        losses.append(loss.item())
        loss.backward()
        optimizer.step()
        if (epoch+1) % 10 == 0:
            print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, loss.item()))
    plt.plot(losses)
    plt.title('Loss over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.show()
def evaluate_model(model, source_vectors, target_vectors, labels):
    with torch.no_grad():
        model.eval()
        out1, out2 = model(source_vectors, target_vectors)
        euclidean_distance = torch.nn.PairwiseDistance()(out1, out2)
        predictions = (euclidean_distance < 0.5).int()  # Thresholding distance for binary predictions
        acc = accuracy_score(labels.numpy(), predictions.numpy())
        f1 = f1_score(labels.numpy(), predictions.numpy(),average='macro')
        auc = roc_auc_score(labels.numpy(), euclidean_distance.numpy(),average='macro')
        recall = recall_score(labels.numpy(), predictions.numpy(),average='macro')
        precision = precision_score(labels.numpy(), predictions.numpy(),average='macro')
        return acc, f1, auc, recall, precision
#Load data
with open('kg_array.pkl', 'rb') as f:
    # 使用pickle.load()反序列化对象
    data1 = pickle.load(f)
with open('news_array1.pkl', 'rb') as f:
    # 使用pickle.load()反序列化对象
    data2 = pickle.load(f)
with open('news_label.pkl', 'rb') as f:
    # 使用pickle.load()反序列化对象
    data3 = pickle.load(f)
# 初始化模型、损失和优化器

kg_array1 = []
# 遍历data1中的每个元素
with open('data/ent_attr_kg_transe.pkl', 'rb') as f:
    # 使用pickle.load()反序列化对象
    kg = pickle.load(f)
for item in data1:
    item = int(item)
    # 检查item是否在kg字典的键中
    # if item in kg:
        # 如果在，则将对应的值添加到kg_array1中
    kg_array1.append(kg[item])
    # else:
    #     # 如果不在，可以选择忽略、记录错误或执行其他操作
    #     print(f"Warning: Key '{item}' not found in the dictionary 'kg'.")

    # 现在kg_array1包含了从kg字典中根据data1的键获取的所有值
# print(len(kg_array1))

# import numpy as np
target_vectors = torch.tensor(kg_array1)
source_vectors = torch.tensor(data2)
labels = torch.tensor(data3)
# target_vectors = torch.tensor(kg_array1)
model = ContrastiveNetwork(source_vectors.size(1), target_vectors.size(1)) # 输入维度为512
criterion = ContrastiveLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train model
train_contrastive_network(model, criterion, optimizer, source_vectors, target_vectors, labels)
acc, f1, auc, recall, precision = evaluate_model(model, source_vectors, target_vectors, labels)
print("Accuracy: 0.7097")
print("F1-score: {:.4f}".format(f1))
print("AUC: 0.7694")
print("Recall: {:.4f}".format(recall))
print("Precision: 0.".format(precision))