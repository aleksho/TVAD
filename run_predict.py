import os
import argparse
from tqdm.auto import tqdm
# import warnings

import torch
import numpy as np
import pandas as pd

from ad_class_predict.config import ModelConfig
from ad_class_predict.transform import train_transform, pred_transform
from ad_class_predict.dataset import TrainDataset, PredDataset
from ad_class_predict.model import CustomModel_v2
from torch.utils.data import DataLoader
import timm

def predict():
    df = pd.read_csv(ModelConfig.input_file, usecols = [ModelConfig.img_name])
    pred_dataset = PredDataset(df, ModelConfig, transform=pred_transform)

    pred_loader  = DataLoader(pred_dataset,
                                    batch_size=ModelConfig.batch_size,
                                    shuffle=False,
                                    num_workers=ModelConfig.num_workers, pin_memory=True, drop_last=False)

    model = CustomModel_v2()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    state = torch.load(ModelConfig.model_weights, map_location=torch.device(device))
    model.load_state_dict( state['state_dict'])


    model.to(device)
    model.eval()
    print('ok')

    tk0 = tqdm(enumerate(pred_loader), total=len(pred_loader))
    preds = []
    for i, (images) in tk0:
        images = images.to(device)
        with torch.no_grad():
            y_preds = model(images)
        preds.append(np.argmax(y_preds.to('cpu').numpy(), axis=1))

    preds_list = np.concatenate(preds, axis=None)
    df['pred'] =preds_list

    df.to_csv(ModelConfig.output_file, index = False)

    print('Total:', len(df))

    print(df['pred'].value_counts())



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

    my_dict = vars(parser.parse_args())
    for key, val in my_dict.items():
        if val is not None:
            setattr(ModelConfig, key, val)


if __name__ == "__main__":
    parse_opt()
    predict()


