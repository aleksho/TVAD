import os
import re
from tqdm import tqdm
import csv
from datetime import datetime
import fnmatch
import zipfile
import warnings
warnings.simplefilter("ignore", UserWarning)

import sys
sys.path.append("/home/alexander_nn/TVAD")

'''
Создание архива картинок и файла с метками
'''

from ad_tokio2.utils import getConnection, get_one_label
from ad_tokio2.config import model_conf

# from utils.ad_config import model_conf

start_time = datetime.now()
dir_files  = model_conf['dir']['dir_files']
dir_images = model_conf['dir']['dir_images']

base_dir_path = f"/var/www/sellavir.self/sofwebclient/frames/api"
files_in_dir = os.listdir(dir_files)
files_tozip = fnmatch.filter(files_in_dir, 'tozip_*')

max_count = 100000
# max_count = 100
# _count = 0

def to_zip(file_label= None,  file_zip= None, list_files = None ):
    with zipfile.ZipFile(file=file_zip, mode="w", ) as out_zip:
        out_zip.write(file_label, os.path.basename(file_label))
        for row in tqdm(list_files, desc=os.path.basename(file_zip)):
            file_name = row[11]
            file_path = row[-1]
            out_zip.write(file_path, file_name)

def save_files(csv_file_path = None, list_rows = None, zip_file_path =None, columns = None):
    with open(csv_file_path, 'w', newline='') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(columns)
        for row in list_rows:
            csvwriter.writerow(row[:-1])
    to_zip_dict = dict(
        file_label=csv_file_path,
        file_zip=zip_file_path,
        list_files=list_rows
    )
    to_zip(**to_zip_dict)



# %%
list_rows=[]

csv_tag = None
for tozip_name in tqdm(sorted(files_tozip,  reverse=True)):
    # print(re.split('_|\.',tozip_name))
    _, year, day, _, _ = re.split('_|\.',tozip_name)
    csv_tag = f'{year}_{day}'
    csv_file_path  = f'{dir_images}/lables_{csv_tag}_files.csv'
    zip_file_path  = f'{dir_images}/images_{csv_tag}_files.zip'
    if csv_tag is None:
        print(f'None {zip_file_path}')
        break
    if os.path.isfile(zip_file_path):
        continue

    with open(f'{dir_files}/{tozip_name}', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        columns = next(reader, None)
        for row in reader:
            # sid = row[0]
            # aid = row[1]
            # label = row[2]
            dev_name = row[3]
            folder_name = row[4]
            # image_date = row[7]
            image_name = row[11]
            row[2] = 0 if row[2] == 'ad' else 1
            image_path = f"/var/www/sellavir.self/sofwebclient/frames/api/{dev_name}/{folder_name}/{image_name}"

            new_row = [*row, image_path ]
            list_rows.append(new_row)

        to_save_files_dict =dict (
                csv_file_path = csv_file_path,
                list_rows = list_rows,
                zip_file_path = zip_file_path,
                columns = columns,
                )

        # if len(list_rows) > max_count:
        save_files(**to_save_files_dict)
        list_rows =[]
        csv_name = None
        # break

save_files(**to_save_files_dict)

print(f" stage5  finish in {datetime.now() - start_time}")


