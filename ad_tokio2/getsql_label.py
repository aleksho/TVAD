# %%
import numpy as np
import mysql.connector
import os
import glob
import pandas as pd
from tqdm import tqdm
import csv
from utils import getConnection , get_one_label, to_zip, get_image_path, get_image_path2
# from utils import getConnection , get_one_label, to_zip, get_image_path
SSH_CONNECT = False
SSH_PORT = 33360
# SSH_PORT = 3306


day_start = 1
day_end   = 245
DIR_HOME = '/home/alexander_nn/TVAD/ad_sql'
DIR_FILES = f'{DIR_HOME}/dir_files'
sql_file = '245.sql'
sql_path = f'{DIR_HOME}/{sql_file}'

with open(sql_path) as f:
    query_format = f.read()

conf ={
    'start':day_start,
    'end' : day_end,
    'label': 'ad',
    'limit' : 12000,
}
day_of_year = conf['end']
csv_file_path_start  = f'{DIR_FILES}/csv_{day_of_year}_start.csv'
csv_file_path_end    = f'{DIR_FILES}/csv_{day_of_year}.csv'
csv_file_path_tozip = f'{DIR_FILES}/csv_{day_of_year}_tozip.csv'

columns =[ 'sid', 'aid', 'label', 'name', 'folder_name',  'second','video_id',
           'start_write_file', 'place', 'day_of_year', 'channel_id', 'file_path', 'image_name']
import os.path
# %%
# if os.path.isfile(csv_file_path_start):
#     os.remove(csv_file_path_start)
#     print( f'del old csv {csv_file_path_start}')
#
# for label in [ 'ad', 'not_ad']:
#     conf['label'] = label
#     if os.path.isfile(csv_file_path_start):
#         mode = 'a'
#     else:
#         mode = 'w'
#     sql_dict=dict(
#         query_format = query_format,
#         conf = conf,
#         csv_file_path = csv_file_path_start,
#         # mode = mode
#     )
#     get_one_label(**sql_dict)
# %%
# for i, x in enumerate(columns):
#     print(i, x)

# %%
new_dataframe =[]
import csv
with open(csv_file_path_start, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # columns = next(reader, None)
    print('get basePath')
    for row in tqdm(reader):
        sid         = row[0]
        aid         = row[1]
        label       = row[2]
        dev_name    = row[3]
        folder_name = row[4]
        second      = row[5]
        video_id    = row[6]
        start_write_file = row[7]
        basePath = f"/var/www/sellavir.self/sofwebclient/frames/api/{dev_name}/{folder_name}/"
        for secondIdx in [1,3,6]:
            # file_lists = get_image_path(basePath, second, secondIdx=secondIdx)
            file_lists = get_image_path2(basePath, second, secondIdx=secondIdx)
            for file_path in file_lists:
                file_base = os.path.basename(file_path)
                # print(file_path)
                new_dataframe.append([*row, file_path, file_base])



i=0
with open(csv_file_path_tozip, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(columns)
    for row in tqdm(new_dataframe):
        i+=1
        csvwriter.writerow(row)
print(f'rows {i}')

# %%
df =pd.read_csv(csv_file_path_tozip)
new_col =['sid','aid','image_name','label','start_write_file','day_of_year','place', 'channel_id']
df[new_col].to_csv(csv_file_path_end, index=False)
# %%
# file_zip = f'{DIR_FILES}/images_{day_of_year}.zip'
# to_zip_dict = dict(
#         file_csv = csv_file_path_tozip,
#         file_label= csv_file_path_end,
#         file_zip= file_zip
#         )
# to_zip(**to_zip_dict)


print('done')