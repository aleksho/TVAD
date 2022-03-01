import os
from tqdm import tqdm

import sys
sys.path.append("/home/alexander_nn/TVAD")

# from ad_tokio2.utils import getConnection, get_one_label
# from ad_tokio2.config import model_conf

from ad_tokio2.config import model_conf
from ad_tokio2.utils import getConnection, get_one_label

import csv
from datetime import datetime

'''
Выкачивает из базы и создаёт списк данных для меток ad и not_ad в дне года.

Из файла sql_df_path берём  ограничения на LIMIT запроса в базу данных для дня года.
Это позволяет взять равное количесво меток обоего класса
fetch 242 sql in time 2:21:25.185623

'''

start_time = datetime.now()

dir_sql   = model_conf['dir']['dir_sql']
dir_datas = model_conf['dir']['dir_datas']



sql_file      = 'sql_step_ad.sql'
sql_file_path = f'{dir_sql}/{sql_file}'

dir_tokio = model_conf['dir']['dir_tokio']
sql_df_path    = f'{dir_tokio}/sql_datas/csv_lable_count.csv'

sql_columns = ['S.id', 'A.id', 'A.type', 'D.name', 'V.folder_name', 'S.second', 'S.video_id', 'V.start_write_file',
               'D.place', 'DAYOFYEAR(V.start_write_file)', 'V.channel_id']

with open(sql_file_path) as f:
    query_format = f.read()
i=0
with open(sql_df_path, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    _ = next(reader, None)
    print('get sql list')
    for row in tqdm(reader):
        i+=1
        csv_file_sql_day = f'{dir_datas}/data_{row[0]}.csv'
        if os.path.isfile(csv_file_sql_day):
            continue
        print(f'work {csv_file_sql_day}')
        for label in ['ad', 'not_ad']:
            conf = {'year': row[1],'day_of_year': row[2],'label': label,'limit': row[6]}
            if os.path.isfile(csv_file_sql_day):
                mode = 'a'
            else:
                mode = 'w'
            sql_dict=dict(
                query_format = query_format,
                conf = conf,
                csv_file_path = csv_file_sql_day,
                mode = mode,
                columns = sql_columns,
            )
            get_one_label(**sql_dict)

date_end = datetime.now() - start_time
print(f"fetch {i} sql in time {date_end}")


