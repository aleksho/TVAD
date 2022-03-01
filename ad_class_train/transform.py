import pandas as pd
import pytorch_lightning as pl
import albumentations as A

from torch.utils.data import DataLoader
from albumentations.pytorch import ToTensorV2
from ad_class_train.dataset import TrainDataset



class TVAD_DataModule(pl.LightningDataModule):
    def __init__(self,
                 train_file=None,
                 train_images_root=None,

                 val_file=None,
                 val_images_root=None,

                 test_file=None,
                 test_images_root=None,

                 predict_file=None,
                 predict_images_root=None,

                 num_workers=2,
                 n_splits=5,
                 batch_size=8,
                 **kwargs,
                 ):
        super().__init__()
        self.batch_size = batch_size
        self.train_transform = train_transform
        self.val_transform = pred_transform

        self.n_splits = n_splits
        self.train_file = train_file
        self.val_file = val_file
        self.test_file = test_file
        self.predict_file = predict_file

        self.train_images_root = train_images_root
        self.val_images_root = val_images_root
        self.test_images_root = test_images_root
        self.predict_images_root = predict_images_root

        self.num_workers = num_workers

        self.save_hyperparameters()
        # print(f'num_workers {num_workers}')

    def prepare_data(self):
        # prepare_data is called only once on 1- GPU in a distributed computing
        # df = pd.read_csv(self.train_file)
        # df["kfold"] =-1
        # df = df.sample(frac=1).reset_index(drop=True)
        # stratify = StratifiedKFold(n_splits=self.n_splits)
        # for i, (t_idx,v_idx) in enumerate(stratify.split(X=df.img_name.values,
        #                                                 y=df.label.values)):
        #     df.loc[v_idx,"kfold"] = i
        # df.to_csv(self.train_folds, index=False)
        train  = pd.read_csv(self.train_file)
        val    = pd.read_csv(self.val_file)
        test   = pd.read_csv(self.test_file)
        predict= pd.read_csv(self.predict_file)

        self.train_dataset = TrainDataset(train, image_dir=self.train_images_root, transform=self.train_transform)
        self.val_dataset   = TrainDataset(val,   image_dir=self.val_images_root,   transform=self.val_transform)
        self.test_dataset  = TrainDataset(test,  image_dir=self.test_images_root,  transform=self.val_transform)
        ################ ##########################
        self.pred_dataset = TrainDataset(predict, image_dir=self.predict_images_root, transform=self.val_transform,
                                         train=False)

    # def setup(self,stage=None):
    # dfx   = pd.read_csv(self.train_folds)
    # train = dfx.loc[dfx["kfold"]!=1]
    # val   = dfx.loc[dfx["kfold"]==1]
    # test =  pd.read_csv(self.test_file)
    # if stage == 'fit' or None:
    # pass

    def train_dataloader(self):
        return DataLoader(self.train_dataset,
                          batch_size=self.batch_size,
                          num_workers=self.num_workers,
                          pin_memory=True,
                          drop_last=True,
                          shuffle=True,
                          persistent_workers = True,
                          )

    def val_dataloader(self):
        return DataLoader(self.val_dataset,
                          batch_size=self.batch_size,
                          num_workers=self.num_workers,
                          pin_memory=True,
                          )

    def test_dataloader(self):
        return DataLoader(self.test_dataset,
                          batch_size=self.batch_size,
                          num_workers=self.num_workers,
                          pin_memory=False,
                          )

    def predict_dataloader(self):
        return DataLoader(self.pred_dataset,
                          batch_size=self.batch_size,
                          num_workers=self.num_workers,
                          pin_memory=False,
                          )


train_transform = A.Compose(
    [
        A.Resize(300, 300),
        A.RandomBrightnessContrast(p=0.2, brightness_limit=(-0.2, 0.2), contrast_limit=(-0.2, 0.2)),
        A.HueSaturationValue(p=0.2, hue_shift_limit=0.2, sat_shift_limit=0.2, val_shift_limit=0.2),
        A.ShiftScaleRotate(p=0.2, shift_limit=0.2, scale_limit=0.2, rotate_limit=0),
        A.CoarseDropout(p=0.2),
        A.Transpose(p=0.5),
        A.HorizontalFlip(p=0.5),
        A.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
        ToTensorV2(),
    ]

)

pred_transform = A.Compose(
    [
        A.Resize(300, 300),
        A.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
        ToTensorV2(),
    ]
)