import numpy as np
import os
import re
from tqdm import tqdm
import csv
from datetime import datetime
import fnmatch
import sys
sys.path.append("/home/alexander_nn/TVAD")

from ad_tokio2.utils import getConnection, get_one_label
from ad_tokio2.config import model_conf

# from utils.utils import getConnection, get_one_label
# from utils.ad_config import model_conf

start_time = datetime.now()
dir_datas = model_conf['dir']['dir_datas']
dir_files = model_conf['dir']['dir_files']
dir_errors=  model_conf['dir']['dir_errors']

file_list_path = f'{dir_datas}/file_list.csv'


base_dir_path = f"/var/www/sellavir.self/sofwebclient/frames/api"
secondIdx =1
files_in_dir = os.listdir(dir_datas)
files_csv = fnmatch.filter(files_in_dir, 'data_*')
files_rec = fnmatch.filter(files_in_dir, 'recc_*')

# recc_recclient0003_list.csv
# files_rec = fnmatch.filter(files_in_dir, '*recclient0102*')

recclient_dict = {}

for rec_name in tqdm(sorted(files_rec)):
    _, recclient, _ = re.findall('(recc_)(.+)(_list.csv)',rec_name)[0]
    if recclient_dict.get(recclient) is None:
        recclient_dict[recclient] = {}
    with open(f'{dir_datas}/{rec_name}') as recc_file:
        recclients = recc_file.read().splitlines()
        for line in tqdm(recclients, desc = f'{recclient}'):
            r_head, r_tail = re.split('/', line)
            # if r_head != '3ch_20210629_224630':
            #     continue

            relist = re.split('_|\.', r_tail)
            r_second, ids = int(relist[0]), relist[-2]

            if recclient_dict[recclient].get(r_head) is None:
                recclient_dict[recclient][r_head] = {}

            if recclient_dict[recclient][r_head].get(r_second) is None:
                recclient_dict[recclient][r_head][r_second] = []

            recclient_dict[recclient][r_head][r_second].append(r_tail)
#             # break
print(f" stage recclient {datetime.now() - start_time}")
# %%
# new_sql_columns = ['S.id', 'A.id', 'A.type', 'D.name', 'V.folder_name', 'S.second', 'S.video_id', 'V.start_write_file',
#                'D.place', 'DAYOFYEAR(V.start_write_file)', 'V.channel_id', 'image_name', 'secondIdx', 'name_date']
new_sql_columns = ['sid', 'aid', 'atype', 'dname', 'vfolder_name', 'ssecond', 'svideo_id', 'vstart_write_file',
               'dplace', 'day_of_year', 'vchannel_id', 'image_name', 'secondIdx', 'name_date']

print(len(files_csv))
for csv_name in tqdm(sorted(files_csv)):
    _, year, day, _ = re.split('_|\.',csv_name)
    name_date = f'{year}_{day}'
    # if day != '21':
    #     continue
    csv_file_path_tozip = f'{dir_files}/tozip_{name_date}_files.csv'
    if os.path.isfile(csv_file_path_tozip):
        continue
    # print(csv_file_path_tozip)
    # with open(csv_file_path_tozip, 'r', newline='') as file_to_write:
    with open(csv_file_path_tozip, 'w', newline='') as file_to_write:
        csvwriter = csv.writer(file_to_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(new_sql_columns)

        with open(f'{dir_datas}/{csv_name}', newline='') as file_to_read:
            reader = csv.reader(file_to_read, delimiter=',')
            columns = next(reader, None)
            for row in reader:
                sid = row[0]
                aid = row[1]
                label = row[2]
                dev_name = row[3]
                folder_name = row[4]
                second = row[5]
                video_id = row[6]
                start_write_file = row[7]
                for secondIdx in range(1, 7):
                    new_sec = int(second) + secondIdx
                    imageName = f"{new_sec}_*.jpg"
                    # imageName = f"{new_sec}_*_{video_id}.jpg"
                    try:
                        base_dict = recclient_dict[dev_name][folder_name][new_sec]
                        secondFiles = fnmatch.filter(base_dict, imageName)
                        for file_second_name in secondFiles:
                            # print(f'csvwriter {file_second_name}')
                            file_base = os.path.basename(file_second_name)
                            new_row = row.copy()
                            new_row.append(file_base)
                            new_row.append(secondIdx)
                            new_row.append(name_date)
                            csvwriter.writerow(new_row)
                            # print(new_row)
                    except KeyError as err:
                        csv_file_err = f'{dir_errors}/err_{name_date}_files.csv'
                        with open(csv_file_err, 'a', newline='') as err_file:
                            err_writer = csv.writer(err_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            err_writer.writerow([*row, file_base])
                        # raise
                    # print()
                    # # print(f'set {dev_name} {folder_name} {new_sec} :: {err}')
                    # print(row, new_sec)
                    # raise


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