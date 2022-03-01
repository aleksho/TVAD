from torch.utils.data import DataLoader, Dataset
from skimage import io
import os

class TrainDataset(Dataset):
    def __init__(self, df, CFG, transform=None):
        self.df = df
        self.transform = transform
        self.image_ids = df[CFG.img_name].values
        self.image_dir = CFG.image_dir
        self.labels = []
        if CFG.label in df.columns:
            self.labels = df[CFG.label].values

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        image_id = str(self.image_ids[idx])
        image = io.imread(os.path.join(self.image_dir, image_id))

        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']
        label = self.labels[idx]

        return (image, label)


class PredDataset(Dataset):
    def __init__(self, df, CFG, transform=None):
        self.df = df
        self.transform = transform
        self.image_ids = df[CFG.img_name].values
        self.image_dir = CFG.image_dir

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        image_id = str(self.image_ids[idx])
        image = io.imread(os.path.join(self.image_dir, image_id))

        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']

        return image