
import torch
from datetime import datetime
from pytorch_lightning import seed_everything
import zipfile
import os
import fnmatch
import pandas as pd
import shutil
import torchvision
import re
from tqdm import tqdm
import sys
sys.path.append("/home/alexander_nn/TVAD")

# import flash
# from flash.image import ImageClassificationData, ImageClassifier


# from ad_santa_monica.config import model_conf

from ad_santa_monica.config import model_conf

start_time = datetime.now()
dir_files  = model_conf['dir']['dir_files']
dir_images = model_conf['dir']['dir_images']
dir_datas  = model_conf['dir']['dir_datas']

# dir_files = '/mnt/disk1/alexander_nn/work/dir_files/dir_images/'

dataframe_input_file = model_conf['dir']['input_file']

files_zip = fnmatch.filter(os.listdir(dir_files), 'images_*')

# files_zip = fnmatch.filter(os.listdir(dir_files), 'images_2022_3*')

print(len(files_zip))
# %%
for path_to_zip_file in tqdm(sorted(files_zip)):
    # print(path_to_zip_file)
    _, year, day, _, _ = re.split('_|\.', path_to_zip_file)
    name_tag = f'{year}_{day}'
    # if day != '6':
    #     continue
    with zipfile.ZipFile(f'{dir_files}/{path_to_zip_file}', 'r') as zip_file:
        for file in tqdm(desc = f'unzip {path_to_zip_file}', iterable=zip_file.namelist(), total=len(zip_file.namelist())):
            # print(file)
            new_dir = f'{dir_images}/{name_tag}'
            if file.endswith('.csv'):
                zip_file.extract(member=file, path=f'{dir_datas}')
            if os.path.isfile(f'{new_dir}/{file}'):
                continue
            zip_file.extract(member=file, path=new_dir)
        # zip_ref.extractall(dir_images)

# print('End ZipFile ')

files_lables_in_dir_images = fnmatch.filter(os.listdir(dir_images), 'lables_*')
files_images_in_dir_images = fnmatch.filter(os.listdir(dir_images), '*.jpg')

print(len(files_images_in_dir_images))
print(len(os.listdir(dir_datas)))













# for image_name in tqdm(files_images_in_dir_images, desc = 'test data.size()[0]',):
#     # image_name =files_images_in_dir_images[12]
#     image_path = f'{dir_images}/{image_name}'
#     data = torchvision.io.read_image(image_path)
#     if data.size()[0] != 3:
#         os.remove(image_path)

    # nlabel = f"{data.size()[0]}_{data.size()[1]}_{data.size()[2]}"

# files_images_in_dir_images = fnmatch.filter(os.listdir(dir_images), '*.jpg')
# print(f'{len(files_images_in_dir_images)} size = 3')

# for input_file in tqdm(sorted(files_lables_in_dir_images)):
#     gt = pd.read_csv(f"{dir_images}/{input_file}")
#     base_name = os.path.basename(input_file)
#
#     shutil.copy(f"{dir_images}/{base_name}", f"{dir_datas}/{base_name}")

# df0 = pd.DataFrame(files_images_in_dir_images)
# df1 = None
# for input_file in tqdm(sorted(files_lables_in_dir_images)):
#     gt = pd.read_csv(f"{dir_images}/{input_file}")
#     print(f"{dir_images}/{input_file}")
#     if df1 is None:
#         df1 = gt.copy()
#     else:
#         df1 = pd.concat([df1, gt], ignore_index=True)
#
#
# df=df0.merge(df1, how='left', left_on=0, right_on='image_name').drop(columns='image_name').rename(columns={0:'image_name'})
# df.sort_values(by='date')
# df.reset_index(inplace=True)
# # df.to_csv(dataframe_input_file, index=False, compression= 'bz2')
# df.to_csv(dataframe_input_file, index=False)

# # %%
# print(df['labels'].value_counts())
# # %%
#
#     folds = df.copy()
#     Fold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
#     str_fold = -1
#     for n, (train_index, val_index) in enumerate(Fold.split(folds, folds[label])):
#         if n < 7:
#             str_fold = 1
#         elif n < 9:
#             str_fold = 2
#         else:
#             str_fold = 3
#         folds.loc[val_index, 'fold'] = int(str_fold)
#     folds_lables = [image_name, label]
#     folds[folds['fold'] == 1 ][folds_lables].to_csv(train_file, index = False)
#     folds[folds['fold'] == 2 ][folds_lables].to_csv(val_file,   index = False)
#     folds[folds['fold'] == 3 ][folds_lables].to_csv(test_file,  index = False)
#     folds[folds['fold'] == 3 ][folds_lables].to_csv(predict_file, index=False)
#     print(folds['fold'].value_counts())





#Santa_monica 1 finish in 1:40:38.992599


print(f" Santa_monica 1 finish in {datetime.now() - start_time}")