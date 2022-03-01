import os
DIR_HOME = '/home/alexander_nn/TVAD'
DIR_WORK = f'{DIR_HOME}/work2'

DIR_TOKIO = '/HDD1/TVAD'
# os.chdir(DIR_HOME)

DIR_MODEL=f'{DIR_WORK}/dir_model'
os.makedirs(DIR_MODEL, exist_ok=True)

DIR_LOGS = f'{DIR_WORK}/dir_logs'
os.makedirs(DIR_LOGS, exist_ok=True)

DIR_FILES = f'{DIR_WORK}/dir_files'
os.makedirs(DIR_FILES, exist_ok=True)


DIR_IMAGES = f'{DIR_TOKIO}/dir_images'
os.makedirs(DIR_IMAGES, exist_ok=True)

DIR_DATAS = f'{DIR_WORK}/dir_datas'
os.makedirs(DIR_DATAS, exist_ok=True)

DIR_ERR= f'{DIR_WORK}/dir_errors'
os.makedirs(DIR_ERR, exist_ok=True)

DIR_SQL   = f'{DIR_HOME}/ad_tokio2/sql_form'

import yaml
conf_dir=dict(
dir_images = f"{DIR_IMAGES}",
dir_model  = f"{DIR_MODEL}",
dir_work   = f"{DIR_WORK}",
dir_logs   = f"{DIR_LOGS}",
dir_files  = f"{DIR_FILES}",
dir_datas  = f"{DIR_DATAS}",
dir_sql    = f"{DIR_SQL}",
dir_errors = f"{DIR_ERR}",
dir_tokio  = f"{DIR_HOME}/ad_tokio2",
)
num_workers =2
# if device.type == 'cuda':
#     num_workers = os.cpu_count()


conf_def=yaml.safe_load("""
model:
    model_name: tf_efficientnet_b3_ns
    imgage_size : 300
    num_classes : 2
    batch_size : 8
    target_fields: label
    input_field  : image_name
    pretrained : True
    lr : 1e-3
    epochs : 10
    num_workers : {num_workers}

optimizer:
    name : Adam

scheduler:
    name: ReduceLROnPlateau
    factor   : 0.2
    patience : 2
    eps      : 1e-6

model_log:
    model_log   : '{model_name}_{imgage_size}'
    model_label : '{model_name}_{imgage_size}_b{batch_size}'
dir:
    dir_model  : '{dir_model}'
    dir_work   : '{dir_work}'
    dir_images : '{dir_images}'
    train_images_root  : '{dir_images}'
    val_images_root    : '{dir_images}'
    test_images_root   : '{dir_images}'
    predict_images_root: '{dir_images}'



    train_file    : '{dir_files}/train_file.csv'
    val_file      : '{dir_files}/val_file.csv'
    test_file     : '{dir_files}/test_file.csv'
    predict_file  : '{dir_files}/predict_file.csv'


    dir_logs   : '{dir_logs}'
    dir_files  : '{dir_files}'
    dir_datas  : '{dir_datas}'
    dir_sql    : '{dir_sql}'
    dir_tokio  : '{dir_tokio}'
    dir_errors : '{dir_errors}'
    
    input_file : '{dir_files}/input_file.csv'
    output_file: '{dir_files}/output_file.csv'
 """)

model_conf = conf_def.copy()
model_conf['model']['num_workers'] = num_workers


for key in model_conf['dir']:
    model_conf['dir'][key] = model_conf['dir'][key].format(**conf_dir)

for key in model_conf['model_log']:
    model_conf['model_log'][key] = model_conf['model_log'][key].format(**model_conf['model'])

# import pprint
# pprint.pprint(model_conf, width=1)