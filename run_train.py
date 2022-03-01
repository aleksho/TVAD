import pytorch_lightning as pl
import shutil
import timm
from datetime import datetime
# sys.path.append("/home/alexander_nn/TVAD")
# sys.path.append("D:/0_Work/TVAD")
from pprint import pprint


from ad_class_train.transform import TVAD_DataModule
from ad_class_train.model import TVAD_Net, set_model_checkpoint
from utils.ad_config import *
from utils.ad_config import model_conf


model_dir = model_conf['dir']['dir_model']
dir_logs  = model_conf['dir']['dir_logs']

model_name = model_conf['model']['model_name']
# batch_size = model_conf['model']['batch_size']

batch_size = 16
key_dir = ['train_file', 'train_images_root',
                 'val_file',  'val_images_root',
                 'test_file', 'test_images_root',
                 'predict_file', 'predict_images_root']
base_dict_dir = {}
base_dict_dir.update((k, v) for k, v in model_conf['dir'].items() if k in key_dir)

# pprint(base_dict_dir)
num_workers= 4
# num_workers=os.cpu_count()


# add_train = True

import argparse

weigth = '/home/alexander_nn/TVAD/work/dir_logs/tf_efficientnet_b3_ns_300_b8_epoch=00_val_acc=1.00-v1.ckpt'



# %%

# def_model = CustomModel_v2()
# # def_model = def_model.load_from_checkpoint(checkpoint_path=weigth)
# my_callbacks, my_logger = set_model_checkpoint(model_name)
# model = TVAD_Net(model=def_model, lr=1e-3, batch_size=batch_size)

# %%

# def_model.load_state_dict(torch.load(weigth))



# %%
# dfk=EmptyModule.load_from_checkpoint(checkpoint_path=weigth,  strict = True)
# dfdf =9
# %%python

def model_set(add_train = False):
    # set_train_dataframe(**model_conf['dir'])
    # def_model = CustomModel_v2()
    def_model = timm.create_model(model_name, pretrained=True, num_classes=2)
    # def_model = def_model.load_from_checkpoint(checkpoint_path=weigth)
    my_callbacks, my_logger = set_model_checkpoint(model_name)
    model = TVAD_Net(model=def_model, lr=1e-3, batch_size=batch_size)
    # if add_train == True:
    #     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    #     state = torch.load(weigth, map_location=torch.device(device))
    #     pretrained_dict = {key.replace("model.", "", 1): value for key, value in state['state_dict'].items()}
    #     def_model.load_state_dict(pretrained_dict)
    #     model = TVAD_Net(model=def_model, lr=1e-3, batch_size=batch_size)



    data_batchs = TVAD_DataModule(batch_size=batch_size, num_workers=num_workers, **base_dict_dir)
    # r(strategy="dp" | "ddp" | "ddp2")
    #
    # `strategy = "ddp_spawn"
    logger_TB  = TensorBoardLogger("tb_logs", name=model_name)
    logger_CSV = CSVLogger("logs", name=model_name)
    logger = [logger_TB, logger_CSV]

    trainer = pl.Trainer(gpus=[0],
                        # auto_select_gpus=True,
                        # strategy='ddp_spawn',
                        # fast_dev_run=True,
                        # overfit_batches = .2,
                        max_epochs = 50,
                        callbacks = my_callbacks,
                        default_root_dir = dir_logs,
                        # logger=my_logger,
                        limit_train_batches=20,
                        limit_val_batches=10,
                        limit_test_batches = 10,
                        log_every_n_steps=1,
                         )
    return trainer, model, data_batchs

# persistent_workers=True,
def train_model(trainer, model, data_batchs):
    trainer.fit(model = model, datamodule = data_batchs)

    best_checkpoints = trainer.checkpoint_callback.best_model_path
    best_checkpoints_save = os.path.join(model_conf['dir']['dir_logs'],
             f"{model_conf['model_log']['model_label']}_{os.path.basename(best_checkpoints)}")

    print(best_checkpoints)
    print(best_checkpoints_save)

    src = best_checkpoints
    dst = best_checkpoints_save
    shutil.copyfile(src, dst)

def val_model(trainer, model, data_batchs):
    trainer.validate(model=model, datamodule=data_batchs)

def test_model(trainer, model, data_batchs):

    trainer.test(model=model, datamodule=data_batchs)

def predict_model(trainer, model, data_batchs):
    trainer.predict(model=model, datamodule=data_batchs)

def parse_opt():
    parser = argparse.ArgumentParser()
    # parser.add_argument('--model_weights',   type=str,  help='model weights path - .ckpt')
    # parser.add_argument('--model_name', type=str,  help='model name - tf_efficientnet_b1_ns_240')
    #
    # parser.add_argument('--model_full', type=str, help='full path to pre-trained model with weights')

    parser.add_argument('--image_dir', type=str, help='directory with images')
    parser.add_argument('--input_file',  type=str, help='''input: df_input.csv - img_name : label \n
                            data frame containing the names of the files in the image directory''')
    parser.add_argument('--output_file', type=str, help='result: df_output.csv - img_name : label')

    # my_dict = vars(parser.parse_args())
    # for key, val in my_dict.items():
    #     if val is not None:
    #         setattr(ModelConfig, key, val)


if __name__ == "__main__":
    start_time = datetime.now()
    parse_opt()
    trainer, model, data_batchs = model_set(add_train = False)
    train_model(trainer, model, data_batchs)

    # trainer, model, data_batchs = model_set(add_train=True)
    val_model(trainer, model, data_batchs)
    test_model(trainer, model, data_batchs)
    predict_model(trainer, model, data_batchs)
    print(f" Train end in {datetime.now() - start_time}")
