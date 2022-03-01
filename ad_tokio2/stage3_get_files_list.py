import numpy as np
import mysql.connector
import os
import re
import glob
import pandas as pd
from tqdm import tqdm
from pprint import pprint
import csv
from datetime import datetime
import time
import fnmatch
import sys
sys.path.append("/home/alexander_nn/TVAD")

'''
Выкачиваем местоположение всех файлов в интересующих нас директориях
Позже построится мгогоуровневый dict 
для быстрого доступа к списку файлов удовлетворяющему нужному местоположению
на 2022 02 24  данный dict занимает около 40+ gb в памяти сервера
format dict :
recclient_dict[dev_name][folder_name][second] = [list_image_names]
2022 02 26 data 2022 56 done
dir
 finish in 1:03:56.675795

'''



# from ad_tokio2.utils import getConnection, get_one_label
# from ad_tokio2.config import model_conf

from ad_tokio2.utils import getConnection, get_one_label
from ad_tokio2.config import model_conf


start_time = datetime.now()
dir_datas = model_conf['dir']['dir_datas']

file_list_path = f'{dir_datas}/file_recclient_list.csv'
file_all_data  = f'{dir_datas}/file_all_data_list.csv'
file_recclient = f'{dir_datas}/file_all_recclient_list.csv'

files_in_dir = os.listdir(dir_datas)
files_csv = fnmatch.filter(files_in_dir, 'data_*')
new_sql_columns = ['sid', 'aid', 'type', 'name', 'folder_name', 'second', 'video_id', 'start_write_file',
               'place', 'day_of_year', 'channel_id', 'name_date']

dir_api_dict= {}

with open(file_all_data, 'w', newline='') as file_to_write:
    csvwriter = csv.writer(file_to_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(new_sql_columns)

    for csv_name in tqdm(sorted(files_csv), desc='read files_csv'):
        _, year, day, _ = re.split('_|\.', csv_name)
        name_date = f'{year}_{day}'

        with open(f'{dir_datas}/{csv_name}', newline='') as file_to_read:
            reader = csv.reader(file_to_read, delimiter=',')
            columns = next(reader, None)
            for row in reader:
                row.append(name_date)
                csvwriter.writerow(row)
                reclient = row[3]
                try:
                    dir_api_dict[reclient]+=1
                except:
                    dir_api_dict[reclient] =1

df = pd.read_csv(file_all_data)
columns = df.columns
columns_sort = [columns[3], columns[4], columns[5], columns[6]]
df.sort_values(by=columns_sort, inplace=True)
df.to_csv(f'{file_all_data}_n.csv', index=False)

import os, zipfile

with zipfile.ZipFile(f'{file_all_data}.zip', "w",
                     compression=zipfile.ZIP_DEFLATED, compresslevel =9) as zf:
    zf.write(file_all_data, os.path.basename(file_all_data))


with open(file_recclient, 'w', newline='') as file_to_write:
    csvwriter = csv.writer(file_to_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in dir_api_dict.items():
        csvwriter.writerow(row)

with open(file_recclient, newline='') as file_to_read:
    reader = csv.reader(file_to_read, delimiter=',')
    # dir_api_list = [row[0] for row in reader]
    dir_api_list = [tuple(row) for row in reader]

dir_api_list = sorted(dir_api_list)




# pprint(dir_api_list)

# dir_api_list=[
#         'recclient0003',
#         'recclient0005',
#         'recclient0101',
#         'recclient0102',
#         'recclient0201',
#         'recclient0202',
#         'recclient0301_1',
#         'recclient0301_2',
#         'recclient0302',
#         'recclient0303',
#     ]

# for base, count in dir_api_list:
#     file_list_path = f'{dir_datas}/recc_{base}_list.csv'
#     with open(file_list_path, 'w') as f:
#             base_dir_path = f"/var/www/sellavir.self/sofwebclient/frames/api/{base}/"
#             for path, subdirs, files in tqdm(os.walk(base_dir_path), desc=base):
#                 for name in files:
#                     file_jpg = os.path.join(path, name)
#                     # size = os.path.getsize(file_jpg)
#                     _, new_line = file_jpg.split(f'/{base}/')
#                     # f.write(f'{new_line},{size}\n')
#                     f.write(f'{new_line}\n')



print(f" finish in {datetime.now() - start_time}")


