import json
import os
import pickle

import numpy as np
import torch
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import *
from transformers import BertTokenizer


def getFileOrDirPaths(path):
    base_path = '/root/autodl-tmp/fakesv'

    return os.path.join(base_path, path)


class Dataset:

    def __init__(self, path_vid, datamode='title+ocr'):

        self.video_ids = []

        with open(path_vid, "r") as fr:
            for line in fr.readlines():
                self.video_ids.append(line.strip())

        self.video_info = {}

        with open(getFileOrDirPaths('dataset/news.json'), 'r', encoding='utf-8') as f:
            items = json.load(f)
            for item in items:
                try:
                    self.video_info[item['video_id']] = item
                except KeyError:
                    pass

        self.tokenizer = BertTokenizer.from_pretrained(getFileOrDirPaths('bert-base-chinese'))

        self.datamode = datamode

    def __len__(self):
        print('>> len(self.video_ids)=', self.video_ids.__len__())
        return self.video_ids.__len__()

    def __getitem__(self, idx):
        video_id = self.video_ids[idx]
        item = self.video_info[video_id]
        try:
            # audio
            with open(getFileOrDirPaths('dataset/vggish_new/' + video_id + '.pkl'), 'rb') as f:
                vggish_feature = pickle.load(f)
                vggish_feature = torch.FloatTensor(vggish_feature)

            # frames
            with open(getFileOrDirPaths('dataset/Resnet50/' + video_id + '.pkl'), 'rb') as f:
                resnet50_feature = pickle.load(f)
                resnet50_feature = torch.FloatTensor(resnet50_feature)
            # label
            label = item['annotation']
            label = torch.tensor(label)
        except KeyError:
            return None
        except FileNotFoundError:
            return None
        except pickle.UnpicklingError:
            return None

        title_tokens = {}
        # text
        if self.datamode == 'title+ocr':
            title_tokens = self.tokenizer(item['title'] + ' ' + item['ocr'], max_length=512, padding='max_length',
                                          truncation=True)

        title_input_id = torch.LongTensor(title_tokens['input_ids'])
        title_mask = torch.LongTensor(title_tokens['attention_mask'])

        # comments
        comments_inputid = []
        comments_mask = []
        # for comment in item['comments']:
        for comment in item['comments']:
            comment_tokens = self.tokenizer(comment, max_length=250, padding='max_length', truncation=True)
            comments_inputid.append(comment_tokens['input_ids'])
            comments_mask.append(comment_tokens['attention_mask'])
        comments_inputid = torch.LongTensor(np.array(comments_inputid))
        comments_mask = torch.LongTensor(np.array(comments_mask))

        
            
        return {
            'label': label,
            'title_input_id': title_input_id,
            'vggish_feature': vggish_feature,
            'resnet50_feature': resnet50_feature,
        }


import torch.nn.functional as F


def resize_tensor(t, new_size):
    # t = t[0]
    # diff = new_size - len(t)
    # # print('>>diff=', diff)
    # if diff > 0:
    #     t.extend([0] * diff)
    # elif diff < 0:
    #     # 如果新大小小于原始大小，则删除末尾的元素
    #     t = t[:new_size]
    # # print('type(tensor)=', type(t))
    # t = torch.tensor(t)
    # # print('>>tensor.size=', t.shape)
    # return t
    t = t[0]
    diff = new_size - len(t)
    if diff > 0:
        # 如果列表长度不够，使用 torch.cat() 来填充
        padding = torch.zeros(diff, dtype=torch.float32)
        t = torch.cat((t, padding))
    elif diff < 0:
        # 如果列表长度超过指定的大小，截断列表
        t = t[:new_size]
    return t


if __name__ == '__main__':
    dataset = Dataset(getFileOrDirPaths('dataset/video_ids.txt'), datamode='title+ocr')
    concatenated_vector = []
    labels = []
    for i in range(len(dataset)):
        try:
            item = dataset[i]
            if item is None:
                continue
            concatenated_vector.append(resize_tensor(torch.cat((item['title_input_id'].reshape(1, -1),
                                                                item['vggish_feature'].reshape(1, -1),
                                                                item['resnet50_feature'].reshape(1, -1)),
                                                               dim=1).numpy(), 5000))
            labels.append(item['label'])
            # print('>>concatenated_vector.shape=', concatenated_vector[-1].shape)
            # print('>>label=', item['label'])
        except KeyError:
            pass

    print('>> Loaded concatenated_vector.shape=', len(concatenated_vector))
    # concatenated_vector = np.array(concatenated_vector).reshape(1, -1)
    print
    # 构建训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(concatenated_vector, labels, test_size=0.2, random_state=42)

    # 构建Logistic Regression分类器并进行训练
    # clfnn.TransformerEncoderLayer(d_model=self.dim, nhead=2, batch_first=True)

    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    # 检查测试数据集中不同类别的数量
    unique_classes = np.unique(y_test)
    print("Unique classes:", unique_classes)
    print("Number of unique classes:", len(unique_classes))
    # 进行预测并评估模型
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1_score = f1_score(y_test, y_pred, average='weighted')
    auc_score = roc_auc_score(y_test, y_pred)
    recall_score = recall_score(y_test, y_pred, average='weighted')
    precision_score = precision_score(y_test, y_pred, average='weighted')

    print("Accuracy:", accuracy)
    print("F1 score:", f1_score)
    print("AUC score:", auc_score)
    print("Recall score:", recall_score)
    print("Precision score:", precision_score)
