import collections
import os
from torch.utils.data import DataLoader
from models.Baselines import *
from models.FactRM import FactRMModel
from utils.dataloader import *
from models.Trainer import Trainer


def pad_sequence(seq_len, lst, emb):
    result = []
    for video in lst:
        if isinstance(video, list):
            video = torch.stack(video)
        ori_len = video.shape[0]
        if ori_len == 0:
            video = torch.zeros([seq_len, emb], dtype=torch.long)
        elif ori_len >= seq_len:
            if emb == 200:
                video = torch.FloatTensor(video[:seq_len])
            else:
                video = torch.LongTensor(video[:seq_len])
        else:
            video = torch.cat([video, torch.zeros([seq_len - ori_len, video.shape[1]], dtype=torch.long)], dim=0)
            if emb == 200:
                video = torch.FloatTensor(video)
            else:
                video = torch.LongTensor(video)
        result.append(video)
    return torch.stack(result)


def pad_frame_sequence(seq_len, lst):
    attention_masks = []
    result = []
    for video in lst:
        video = torch.FloatTensor(video)
        ori_len = video.shape[0]
        if ori_len >= seq_len:
            gap = ori_len // seq_len
            video = video[::gap][:seq_len]
            mask = np.ones((seq_len))
        else:
            video = torch.cat((video, torch.zeros([seq_len - ori_len, video.shape[1]], dtype=torch.float)), dim=0)
            mask = np.append(np.ones(ori_len), np.zeros(seq_len - ori_len))
        result.append(video)
        mask = torch.IntTensor(mask)
        attention_masks.append(mask)
    return torch.stack(result), torch.stack(attention_masks)


def _init_fn(worker_id):
    np.random.seed(2022)


def FactRM_collate_fn(batch):
    num_comments = 23
    num_frames = 83
    num_audioframes = 50

    title_inputid = [item['title_input_id'] for item in batch if item is not None]
    title_mask = [item['title_mask'] for item in batch if item is not None]

    comments_like = [item['comments_like'] for item in batch if item is not None]
    comments_inputid = [item['comments_inputid'] for item in batch if item is not None]
    comments_mask = [item['comments_mask'] for item in batch if item is not None]

    comments_inputid_resorted = []
    comments_mask_resorted = []
    comments_like_resorted = []

    for idx in range(len(comments_like)):
        comments_like_one = comments_like[idx]
        comments_inputid_one = comments_inputid[idx]
        comments_mask_one = comments_mask[idx]
        if comments_like_one.shape != torch.Size([0]):
            try:
                comments_inputid_one, comments_mask_one, comments_like_one = (list(t) for t in zip(*sorted(
                    zip(comments_inputid_one, comments_mask_one, comments_like_one), key=lambda s: s[2], reverse=True)))
            except ValueError:
                pass
        comments_inputid_resorted.append(comments_inputid_one)
        comments_mask_resorted.append(comments_mask_one)
        comments_like_resorted.append(comments_like_one)

    comments_inputid = pad_sequence(num_comments, comments_inputid_resorted, 250)
    comments_mask = pad_sequence(num_comments, comments_mask_resorted, 250)
    comments_like = []
    for idx in range(len(comments_like_resorted)):
        comments_like_resorted_one = comments_like_resorted[idx]
        if len(comments_like_resorted_one) >= num_comments:
            comments_like.append(torch.tensor(comments_like_resorted_one[:num_comments]))
        else:
            if isinstance(comments_like_resorted_one, list):
                comments_like.append(
                    torch.tensor(comments_like_resorted_one + [0] * (num_comments - len(comments_like_resorted_one))))
            else:
                comments_like.append(torch.tensor(
                    comments_like_resorted_one.tolist() + [0] * (num_comments - len(comments_like_resorted_one))))

    frames = [item['resnet50_feature'] for item in batch if item is not None]
    frames, frames_masks = pad_frame_sequence(num_frames, frames)

    audioframes = [item['vggish_feature'] for item in batch if item is not None]
    audioframes, audioframes_masks = pad_frame_sequence(num_audioframes, audioframes)

    label = [item['label'] for item in batch if item is not None]

    return {
        'label': torch.stack(label),
        'title_input_id': torch.stack(title_inputid),
        'title_mask': torch.stack(title_mask),
        'comments_inputid': comments_inputid,
        'comments_mask': comments_mask,
        'comments_like': torch.stack(comments_like),
        'vggish_feature': audioframes,
        'audioframes_masks': audioframes_masks,
        'resnet50_feature': frames,
        'frames_masks': frames_masks,
    }


def getFileOrDirPaths(path):
    base_path = '/root/autodl-tmp/fakesv'

    return os.path.join(base_path, path)

class Run():
    def __init__(self,config
                 ):

        self.model = None
        self.model_name = config['model_name']
        self.mode_eval = config['mode_eval']
        self.fold = config['fold']
        self.data_type = 'FactRM'

        self.epoches = config['epoches']
        self.batch_size = config['batch_size']
        self.num_workers = config['num_workers']
        self.epoch_stop = config['epoch_stop']
        self.seed = config['seed']
        self.device = config['device']
        self.lr = config['lr']
        self.lambd = config['lambd']
        self.save_param_dir = config['path_param']
        self.path_tensorboard = config['path_tensorboard']
        self.dropout = config['dropout']
        self.weight_decay = config['weight_decay']
        self.event_num = 616
        self.mode = 'normal'

    def get_dataloader(self, data_type, data_fold):
        collate_fn = None
        video_ids = []
        with open(getFileOrDirPaths('dataset/video_ids.txt'), "r") as fr:
            for line in fr.readlines():
                video_ids.append(line.strip())
        
        video_ids_train = [video_ids[i] for i in range(len(video_ids)) if i % 2 == 0]
        video_ids_test = [video_ids[i] for i in range(len(video_ids)) if i % 2 == 1]
        video_ids_test = video_ids_test[len(video_ids_test)//2:]
        video_ids_train.extend(video_ids_test[0:len(video_ids_test)//2])
        
        dataset_train = FactRMDataset(video_ids_train,robustness=True,size=0.45)
        dataset_test  = FactRMDataset(video_ids_test,robustness=False,size=0.05)
        collate_fn = FactRM_collate_fn       
        train_dataloader = DataLoader(dataset_train,
                                      batch_size=self.batch_size,
                                      num_workers=self.num_workers,
                                      pin_memory=True,
                                      shuffle=True,
                                      worker_init_fn=_init_fn,
                                      collate_fn=collate_fn)

        test_dataloader = DataLoader(dataset_test, batch_size=self.batch_size,
                                     num_workers=self.num_workers,
                                     pin_memory=True,
                                     shuffle=False,
                                     worker_init_fn=_init_fn,
                                     collate_fn=collate_fn)

        dataloaders = dict(zip(['train', 'test'], [train_dataloader, test_dataloader]))

        return dataloaders


    def get_model(self):
        print("Loading Model FactRM")
        self.model = FactRMModel(bert_model='bert-base-chinese', fea_dim=128, dropout=self.dropout)
        return self.model

    def main(self):
        if self.mode_eval == "cv":
            collate_fn = None
            history = collections.defaultdict(list)
            print('-' * 50)
            print('-' * 50)
            print("Loading Model")
            self.model = self.get_model()
            print("Model Loaded")
            print("Loading Data")
            dataloaders = self.get_dataloader(data_type=self.data_type, data_fold=0)
            print("Data Loaded")
            trainer = Trainer(model=self.model,
                                device=self.device,
                                lr=self.lr,
                                dataloaders=dataloaders,
                                epoches=self.epoches,
                                dropout=self.dropout,
                                weight_decay=self.weight_decay,
                                mode=self.mode,
                                model_name=self.model_name,
                                event_num=self.event_num,
                                epoch_stop=self.epoch_stop,
                                save_param_path=self.save_param_dir + self.data_type + "/" + self.model_name + "/",
                                writer=None)

            print("Start Training")
            result = trainer.train()

            history['auc'].append(result['auc'])
            history['f1'].append(result['f1'])
            history['recall'].append(result['recall'])
            history['precision'].append(result['precision'])
            history['acc'].append(result['acc'])

            print('results cross-validation: ')
            for metric in ['acc', 'f1', 'precision', 'recall', 'auc']:
                print('%s : %.4f +/- %.4f' % (metric, np.mean(history[metric]), np.std(history[metric])))

        else:
            print("Not Available")
