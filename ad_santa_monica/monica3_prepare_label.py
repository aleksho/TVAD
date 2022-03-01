
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
import csv
from sklearn.model_selection import StratifiedKFold

sys.path.append("/home/alexander_nn/TVAD")

# import flash
# from flash.image import ImageClassificationData, ImageClassifier


# from ad_santa_monica.config import model_conf

from ad_santa_monica.config import model_conf

start_time = datetime.now()
dir_files  = model_conf['dir']['dir_files']
dir_images = model_conf['dir']['dir_images']
dir_datas  = model_conf['dir']['dir_datas']

input_file = model_conf['dir']['input_file']

# dir_files = '/mnt/disk1/alexander_nn/work/dir_files/dir_images/'

dataframe_input_file = model_conf['dir']['input_file']

files_lables = fnmatch.filter(os.listdir(dir_datas), 'lables_2022_*')

raw_dataframe = f'{dir_datas}/raw_dataframe.csv'
mod_dataframe = f'{dir_datas}/mod_dataframe.csv'



# %%
add_columns = True
with open(raw_dataframe, 'w',  newline='') as file_to_write:
    csvwriter = csv.writer(file_to_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for csv_file in tqdm(sorted(files_lables), desc= 'read_csv', display=False):
        with open(f'{dir_datas}/{csv_file}', newline='') as file_to_read:
            reader = csv.reader(file_to_read, delimiter=',')
            columns = next(reader, None)
            if add_columns == True:
                csvwriter.writerow([*columns, 'image_file'])
                add_columns = False
            else:
                for row in reader:
                    new_col = '/'.join([row[13], row[11]])
                    csvwriter.writerow([*row, new_col])


# %%

tqdm.pandas(desc="test isfile")

df = pd.read_csv(raw_dataframe)
print(len(df))
df = df[df.progress_apply(lambda x: os.path.isfile(f"{dir_images}/{x['image_file']}"), axis=1)]
# print(len(df))

# 'atype', 'image_file'
df = df[df['secondIdx'] ==1]
df.reset_index(inplace=True)
df['target_id'] = df['vchannel_id'].astype(str) + '_' + df['atype'].astype(str)
my_list = df['target_id'].value_counts().sort_index().reset_index()['index'].values
my_dict = {x: i for i, x in enumerate(my_list)}
df['label']  = df['atype']
df['multilabel'] = df['target_id'].map(my_dict)
df.to_csv(input_file, index=False)

# %%

folds = df.copy()
folds_lables = ['label', 'image_file']
Fold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
str_fold = -1
for n, (train_index, val_index) in enumerate(Fold.split(folds, folds[folds_lables[0]])):
    if n < 7:
        str_fold = 1
    elif n < 9:
        str_fold = 2
    else:
        str_fold = 3
    folds.loc[val_index, 'fold'] = int(str_fold)

folds[folds['fold'] == 1 ][folds_lables].to_csv(model_conf['dir']['train_file'], index = False)
folds[folds['fold'] == 2 ][folds_lables].to_csv(model_conf['dir']['val_file'],   index = False)
folds[folds['fold'] == 3 ][folds_lables].to_csv(model_conf['dir']['test_file'],  index = False)
folds[folds['fold'] == 3 ][folds_lables].to_csv(model_conf['dir']['predict_file'], index=False)

print(f" Santa_monica 3 set fold finish in {datetime.now() - start_time}")
from pprint import pprint

pprint(folds['fold'].value_counts(normalize=True))

# %%
# print(folds.fold.value_counts(normalize=True))




# %%
# image_file = df.image_file[10]
# file_path = f'{dir_images}/{image_file}'
# import matplotlib.pyplot as plt
# # print(image_file)
# image = plt.imread(file_path)
# plt.imshow(image)
# # %%
# plt.imshow(image)
# plt.show()
# %%
# dir_images_list = os.listdir(dir_images)
# csv_list = fnmatch.filter(os.listdir(dir_datas), '2022_3*')

# for folder_list in tqdm(sorted(dir_images_list, reverse=False)):
#     dir_path = f'{dir_images}/{folder_list}'
#     file_list = os.listdir(dir_path)
#
#     for file in sorted(file_list):
#         image_path = f'{dir_path}/{file}'
#         data = torchvision.io.read_image(image_path)
#         print(data.size())
#         #     if data.size()[0] != 3:
#         #         os.remove(image_path)
#         break
#     break







# %%
# add_columns = True
# print(len(files_lables))
# with open(f'{raw_dataframe}', 'w',  newline='') as file_to_write:
#     csvwriter = csv.writer(file_to_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     for csv_file in tqdm(sorted(files_lables)):
#         with open(f'{dir_datas}/{csv_file}', newline='') as file_to_read:
#             reader = csv.reader(file_to_read, delimiter=',')
#             columns = next(reader, None)
#             if add_columns == True:
#                 csvwriter.writerow(columns)
#                 add_columns = False
#
#             for row in reader:
#                 csvwriter.writerow(row)

# # %%
# df = pd.read_csv(raw_dataframe)
# df['target_id'] = df['vchannel_id'].astype(str) + '_' + df['atype'].astype(str)
# # %%
# my_list = df['target_id'].value_counts().sort_index().reset_index()['index'].values
# my_dict = {x: i for i, x in enumerate(my_list)}
# df['labels'] = df['target_id'].map(my_dict)
# df.to_csv(mod_dataframe, index=False)
# %%
# df.to_csv(mod_dataframe, index=False)
# df['target'].value_counts()


# %%
# print(my_dict['1_0'])

# # %%
# print(df.target_id.value_counts())












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



