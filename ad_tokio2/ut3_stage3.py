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
import pandas as pd
import sys

sys.path.append("/home/alexander_nn/TVAD")

from ad_tokio2.utils import getConnection, get_one_label
from ad_tokio2.config import model_conf


start_time = datetime.now()
dir_datas = model_conf['dir']['dir_datas']

file_list_path = f'{dir_datas}/file_recclient_list.csv'
file_all_data  = f'{dir_datas}/file_all_data_list.csv'
file_recclient = f'{dir_datas}/file_all_recclient_list.csv'


df = pd.read_csv(file_all_data)
columns = df.columns
columns_sort = [columns[3], columns[4], columns[5], columns[6]]
df.sort_values(by=columns_sort, inplace=True)
df.to_csv(f'{file_all_data}_n.csv', index=False)
