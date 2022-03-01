import numpy as np
import os
import re
from tqdm import tqdm
import csv
from datetime import datetime
import fnmatch
import os
import sys

path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)
print(list(sys.path))

# from ad_tokio2.utils import getConnection, get_one_label
# from ad_tokio2.config import model_conf

from utils import getConnection, get_one_label
from utils.ad_config import model_conf

start_time = datetime.now()
dir_datas = model_conf['dir']['dir_datas']
dir_files = model_conf['dir']['dir_files']

file_list_path = f'{dir_datas}/file_list.csv'


base_dir_path = f"/var/www/sellavir.self/sofwebclient/frames/api"
secondIdx =1
files_in_dir = os.listdir(dir_datas)
files_csv = fnmatch.filter(files_in_dir, 'data_*')
files_rec = fnmatch.filter(files_in_dir, 'recc_*')

print(len(files_csv))
# recc_recclient0003_list.csv
# files_rec = fnmatch.filter(files_in_dir, '*recclient0102*')

new_sql_columns = ['S.id', 'A.id', 'A.type', 'D.name', 'V.folder_name', 'S.second', 'S.video_id', 'V.start_write_file',
               'D.place', 'DAYOFYEAR(V.start_write_file)', 'V.channel_id', 'image_name']

from glob import glob

for csv_name in sorted(files_csv):
    _, year, day, _ = re.split('_|\.',csv_name)
    tozip_name = f'{year}_{day}'
    # print(tozip_name)
    if day != '260':
        continue
    csv_file_path_tozip = f'{dir_files}/tozip_{tozip_name}_files.csv'
    # if os.path.isfile(csv_file_path_tozip):
    #     continue
    # print(csv_file_path_tozip)
    # with open(csv_file_path_tozip, 'w', newline='') as csvfile:
    #     csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     csvwriter.writerow(new_sql_columns)

    with open(f'{dir_datas}/{csv_name}', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        columns = next(reader, None)
        for row in tqdm(reader, desc= f'{csv_name}'):
            sid = row[0]
            aid = row[1]
            label = row[2]
            dev_name = row[3]
            folder_name = row[4]
            second = row[5]
            video_id = row[6]
            start_write_file = row[7]
            new_sec = int(second) + secondIdx
            imageName = f"{new_sec}_*{video_id}.jpg"
            # base_dict = recclient_dict[dev_name][folder_name][new_sec]
            base_dict = f"/var/www/sellavir.self/sofwebclient/frames/api/{dev_name}/{folder_name}/"
            filePattern = os.path.join(base_dict, imageName)
            secondFiles = sorted(glob(filePattern))
            print(filePattern)
            f=secondFiles[0]
            # secondFiles = fnmatch.filter(base_dict, imageName)



print(f" stage 4 finish in {datetime.now() - start_time}")




# with zipfile.ZipFile(file=file_zip, mode="w", ) as out_zip:
#     out_zip.write(file_label, os.path.basename(file_label))
#     with open(file_csv, newline='') as csvfile:
#         reader = csv.reader(csvfile, delimiter=',')
#         columns = next(reader, None)
#         for row in tqdm(reader):
#             file_path = row[11]
#             file_name = row[12]
#             out_zip.write(file_path, file_name)

    # i=0
    # with open(csv_file_path_tozip, 'w', newline='') as csvfile:
    #     csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     csvwriter.writerow(new_sql_columns)
    #     for row in tqdm(new_dataframe):
    #         i+=1
    #         csvwriter.writerow(row)
    # print(f'rows {i}')


# for csv_name in csv_files:
#     # _, year, day, _ = re.split('_|\.',csv_file)
#     with open(f'{dir_datas}/{csv_name}', newline='') as csv_file:
#         reader = csv.reader(csv_file, delimiter=',')
#         columns = next(reader, None)
#         for row in tqdm(reader):
#             sid = row[0]
#             aid = row[1]
#             label = row[2]
#             dev_name = row[3]
#             folder_name = row[4]
#             second = row[5]
#             video_id = row[6]
#             start_write_file = row[7]
#             basePath = f"/var/www/sellavir.self/sofwebclient/frames/api/{dev_name}/{folder_name}/"

# files_in_dir = os.listdir(dir_datas)
# csv_files = fnmatch.filter(files_in_dir, 'data_*')






# # print(secondFiles)
# # print(filePattern)
# # print(recclient_dict[dev_name][0])
# with Pool(8) as threadpool:
#     matches = threadpool.map(multi_regexp, row, recclient_dict)
#
# # secondFiles = multi_regexp(row, recclient_dict)
#
# for file_second_name in secondFiles:
#     file_base = os.path.basename(file_second_name)
#     row.append(file_base)
#     csvwriter.writerow(row)
#     # print(file_path)
#     # new_dataframe.append([*row, file_base])
#     # print(len(new_dataframe))