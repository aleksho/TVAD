from datetime import datetime
import pandas as pd
from sklearn.model_selection import StratifiedKFold

# import flash
# from flash.image import ImageClassificationData, ImageClassifier


# from ad_santa_monica.config import model_conf

from utils.ad_config import model_conf

start_time = datetime.now()
dir_files  = model_conf['dir']['dir_files']
dir_images = model_conf['dir']['dir_images']
dir_datas  = model_conf['dir']['dir_datas']
input_file = model_conf['dir']['input_file']
mod_dataframe = f'{dir_datas}/mod_dataframe.csv'
df=pd.read_csv(mod_dataframe)

# %%
max_len = df['labels'].value_counts()[0]
split1 = int(max_len//8*8*.7//8*8)
split2 = max_len//8*8*.15//8*8
split3 = int(split1+split2)
print(max_len, (split1)/max_len, (max_len-split3)/max_len)
# %%
df0 = df[df['labels'] ==0].copy()
df1 = df[df['labels'] ==1].copy()

df0.sort_values(by='vstart_write_file', inplace=True)
df1.sort_values(by='vstart_write_file', inplace=True)

df_train = pd.concat([df0[:split1], df1[:split1]], ignore_index=True)
df_val   = pd.concat([df0[split1:split3], df1[split1:split3]], ignore_index=True)
df_test  = pd.concat([df0[split3:], df1[split3:]] , ignore_index=True)

df_train = df_train.sample(frac=1).reset_index(drop=True)
df_val   = df_val.sample(frac=1).reset_index(drop=True)
df_test  = df_test.sample(frac=1).reset_index(drop=True)

df_train.to_csv(model_conf['dir']['train_file']  , index=False)
df_val.to_csv( model_conf['dir']['val_file']      , index=False)
df_test.to_csv(model_conf['dir']['test_file']     , index=False)
df_test.to_csv(model_conf['dir']['predict_file'], index=False)



# # %%
# df_train['labels'].value_counts()
# # %%
# df_val['labels'].value_counts()
# # %%
# df_test['labels'].value_counts()
# # %%
# df_train.tail()
# # %%
# df_val.tail()
# # %%
# df_test.tail()
# %%
#
# for input_file in tqdm(sorted(files_lables_in_dir_images)):
#     gt = pd.read_csv(f"{dir_images}/{input_file}")
#     base_name = os.path.basename(input_file)


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







print(f" Santa_monica 2 finish in {datetime.now() - start_time}")