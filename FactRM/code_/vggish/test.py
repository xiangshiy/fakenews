from torch.utils.data import Dataset


class A(Dataset):

    def __init__(self):
        self.a = 10
        self.b = 20

    def __getitem__(self, item):
        return {
            'a':self.a,
            'b':self.b
        }

a = A()
print(a.items())