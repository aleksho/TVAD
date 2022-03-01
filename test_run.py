import yaml
from pprint import pprint
DIR_HOME  = '//'
IMAGEDIR = f'{DIR_HOME}/images'
DIR_MODEL = '//architecture'


DIR_IMAGE_TRAIN =f'{DIR_HOME}/images_train'
DIR_IMAGE_TEST =f'{DIR_HOME}/images_test'

DIR_LOG  = f'{DIR_HOME}/dir_log'
DIR_FILE = f'{DIR_HOME}/dir_file'

file_config  = f'{DIR_HOME}/ad_class_predict/config.yml'
file_config2 = f'{DIR_HOME}/ad_class_predict/config2.yml'
num_workers =20
conf_dir=dict(
dir_train  = f"{DIR_IMAGE_TRAIN}",
dir_test   = f"{DIR_IMAGE_TEST}",
dir_model  = f"{DIR_MODEL}",
dir_home   = f"{DIR_HOME}",
dir_log    = f"{DIR_LOG}",
dir_file   = f"{DIR_FILE}",
)
with open(file_config) as file:
    conf_def=yaml.safe_load(file)

pprint(conf_def)