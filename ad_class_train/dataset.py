import torch
from torch.utils.data import DataLoader, Dataset

from skimage import io
import os
import pandas as pd
from sklearn.model_selection import StratifiedKFold

class TrainDataset(Dataset):
    def __init__(self, df, image_dir = 'images_train', img_name = 'image_file',
                 label = 'label', transform=None, train = True,
                 **kwargs
                 ):
        self.df = df
        self.transform = transform
        self.train     = train
        self.image_ids = df[img_name].values
        self.image_dir = image_dir
        self.labels = []
        if label in df.columns:
            self.labels = df[label].values


    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        image_id = str(self.image_ids[idx])
        file_path = os.path.join(self.image_dir, image_id)
        if not os.path.exists(file_path):
            print(self.train, self.image_dir, file_path)
        image = io.imread(file_path)
        # image = cv2.imread(file_path)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']
        if self.train:
            label = torch.tensor(self.labels[idx]).long()
            return (image, label)
        else:
            return image

def set_train_dataframe( label =  'label', image_name = 'image_file',
                        input_file = None,
                        train_file= None,
                        train_images_root= None,
                        val_file= None,
                        val_images_root= None,
                        test_file= None,
                        test_images_root= None,
                        predict_file= None,
                        predict_images_root= None,
                         **kwargs,
                        ):
    # files = os.listdir(ModelConfig.image_dir)
    files = [file for file in os.listdir(train_images_root) if file.endswith('.jpg')]
    ground_truth_data = pd.read_csv(input_file)

    df0 = pd.DataFrame(files)
    df=df0.merge(ground_truth_data, how='left', left_on=0, right_on='image_name').drop(columns='image_name').rename(columns={0:'image_name'})

    folds = df.copy()
    Fold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    str_fold = -1
    for n, (train_index, val_index) in enumerate(Fold.split(folds, folds[label])):
        if n < 7:
            str_fold = 1
        elif n < 9:
            str_fold = 2
        else:
            str_fold = 3
        folds.loc[val_index, 'fold'] = int(str_fold)
    folds_lables = [image_name, label]
    folds[folds['fold'] == 1 ][folds_lables].to_csv(train_file, index = False)
    folds[folds['fold'] == 2 ][folds_lables].to_csv(val_file,   index = False)
    folds[folds['fold'] == 3 ][folds_lables].to_csv(test_file,  index = False)
    folds[folds['fold'] == 3 ][folds_lables].to_csv(predict_file, index=False)
    print(folds['fold'].value_counts())

def set_clear_df(dir, file):
    files_input       = os.listdir(dir)
    ground_truth_data = pd.read_csv(file)
    df0 = pd.DataFrame(files_input)
    df=df0.merge(ground_truth_data, how='left', left_on=0, right_on='image_name').drop(columns='image_name').rename(columns={0:'image_name'})
    df=df.sample(frac=1)
    df['label'] = df['label'].map({'ad': 0, 'not_ad': 1})
    df.dropna(inplace = True)
    df.reset_index(inplace = True, drop=True)

    df['label']  =  df['label'].astype('int')
    new_file = f"{'_'.join(file.split('_')[:-1])}.csv"

    df.to_csv(new_file, index = False)
    # return df


