# %%
import numpy as np
import mysql.connector
import os
import glob
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import sys
sys.path.append("/home/alexander_nn/TVAD")

# from ad_sql.utils import getConnection, get_one_label
from ad_tokio2.config import model_conf
from ad_tokio2.utils import getConnection, get_one_label


start_time = datetime.now()

# df_file = 'df_all_lables.csv'
# df_path = f'{DIR_HOME}/{df_file}'



# from ad_sql.utils import getConnection , get_one_label, to_zip, get_image_path

dir_sql = model_conf['dir']['dir_sql']
dir_tokio = model_conf['dir']['dir_tokio']

sql_file = 'st1_get_label_count.sql'
sql_path = f'{dir_sql}/{sql_file}'

csv_file_path_start  = f'{dir_tokio}/sql_datas/csv_lable_st1.csv'
csv_file_path_end    = f'{dir_tokio}/sql_datas/csv_lable_count.csv'
# %%

with open(sql_path) as f:
    query_format = f.read()

import os.path
# %%
# if os.path.isfile(csv_file_path_start):
#     os.remove(csv_file_path_start)
#     print( f'del old csv {csv_file_path_start}')
# %%
columns = ['year','day_of_year', 'label' , 'count']

sql_dict=dict(
    query_format = query_format,
    # conf = conf,
    csv_file_path = csv_file_path_start,
    mode = 'w',
    columns = columns
)
get_one_label(**sql_dict)
# %%

# columns


# %%

df = pd.read_csv(csv_file_path_start)
# %%
df=df.set_index(['year', 'day_of_year', 'label'])
df=df.unstack(2)
df=df.reset_index()

# %%
# df.head()
# %%
df.columns =  ["year", "day_of_year", "ad", "not_ad", 'promo']
df['col'] = df['year'].astype(str) +"_" + df['day_of_year'].astype(str)
df.set_index('col', inplace=True)
df = df.fillna(0)
df['min'] = df[['ad','not_ad']].min(axis=1)
df=df[df['min']>0]
df=df.reset_index()

df['min'] = df['min'].astype(int)

# %%
# df.tail()
# %%
df.to_csv(csv_file_path_end, index = False)
# %%

print(f" finish in {datetime.now() - start_time}")
