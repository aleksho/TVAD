
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

clean_dir = f'{dir_datas}/clean_dir_list.csv'

# torch_dir= []

with open(clean_dir, 'r') as file_to_read:
    torch_dir = file_to_read.read().splitlines()
#  %%

# %%
dir_images_list = os.listdir(dir_images)
# dir_images_list = fnmatch.filter(dir_images, '2022_3*')

for folder_list in tqdm(sorted(dir_images_list, reverse=True)):
    if folder_list in torch_dir:
        continue
    dir_path = f'{dir_images}/{folder_list}'
    file_list = os.listdir(dir_path)
    file_list = fnmatch.filter(file_list, '*.jpg')
    for file in tqdm(sorted(file_list), desc=folder_list):
        image_path = f'{dir_path}/{file}'
        try:
            data = torchvision.io.read_image(image_path)
            if data.size()[0] != 3:
                print(f'del data.size() != 3 {image_path}')
                os.remove(image_path)
        except:
            print(f'del {image_path}')
            os.remove(image_path)
    with open(clean_dir, 'a') as file_to_write:
        file_to_write.write(f'{folder_list}\n')




        # print(data.size())
        # if data.size()[0] != 3:
        #     os.remove(image_path)
    #     break
    # break
# %%


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





#  Santa_monica 2 finish in 4:08:07.741582

print(f" Santa_monica 2 finish in {datetime.now() - start_time}")