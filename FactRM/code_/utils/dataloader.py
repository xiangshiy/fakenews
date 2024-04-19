import json
import pickle
import numpy as np
import torch
import random
from torch.utils.data import Dataset
from transformers import BertTokenizer


def str2num(str_x):
    if isinstance(str_x, float):
        return str_x
    elif str_x.isdigit():
        return int(str_x)
    elif 'w' in str_x or '万' in str_x:
        return float(str_x[:-1]) * 10000
    elif '亿' in str_x:
        return float(str_x[:-1]) * 100000000
    else:
        pass


class FactRMDataset(Dataset):

    def __init__(self, video_ids,robustness=False,size=0.05, datamode='title+ocr'):

        self.video_ids = video_ids
        self.video_info = {}
        with open('/root/autodl-tmp/fakesv/dataset/news.json', 'r', encoding='utf-8') as f:
            items = json.load(f)
            for item in items:
                self.video_info[item['video_id']] = item
        if robustness:
            randomnum = set()
            for i in range(int(len(self.video_ids)*size)):
                randomnum.add(random.randint(0,len(self.video_ids)-1))
            for i in randomnum:
                self.video_info[self.video_ids[i]]['annotation'] = 1 if self.video_info[self.video_ids[i]]['annotation'] == 0 else 0
        

        self.tokenizer = BertTokenizer.from_pretrained('/root/autodl-tmp/fakesv/bert-base-chinese')

        self.datamode = datamode

    def __len__(self):
        return len(self.video_ids)

    def __getitem__(self, idx):
        try:
            video_id = self.video_ids[idx]
            item = self.video_info[video_id]
            # label 
            label = item['annotation']
            label = torch.tensor(label)

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

            comments_like = []

            for num in item['count_comment_like']:
                comments_like.append(str2num(num))

            try:
                comments_like = torch.tensor(np.array(comments_like))
            except TypeError:
                comments_like = torch.tensor(np.array([0]))
                
            # audio
            with open('/root/autodl-tmp/fakesv/dataset/vggish_new/' + video_id + '.pkl', 'rb') as f:
                vggish_feature = pickle.load(f)
                vggish_feature = torch.FloatTensor(vggish_feature)

            # frames
            with open('/root/autodl-tmp/fakesv/dataset/Resnet50/' + video_id + '.pkl', 'rb') as f:
                try:
                    resnet50_feature = pickle.load(f)
                    resnet50_feature = torch.FloatTensor(resnet50_feature)        
                except pickle.UnpicklingError:
                    # print(video_id)
                    resnet50_feature = torch.zeros(1, 2048)
        except KeyError as e:
            return None
        return {
            'label': label,
            'title_input_id': title_input_id,
            'title_mask': title_mask,
            'vggish_feature': vggish_feature,
            'resnet50_feature': resnet50_feature,
            'comments_inputid': comments_inputid,
            'comments_mask': comments_mask,
            'comments_like': comments_like
        }
