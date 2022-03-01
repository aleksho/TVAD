import timm
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchmetrics
# import pytorch_lightning as pl

# from ad_class_predict.config import ModelConfig


class CustomModel_v2(nn.Module):
    def __init__(self, model_name='tf_efficientnet_b3_ns', pretrained=False,  num_classes = 2):
        super().__init__()
        self.model = timm.create_model(model_name, pretrained=pretrained, num_classes=num_classes)

    def forward(self, x):
        out = self.model(x)
        return out


#
# def model_load(model_path = ModelConfig.model_path, model_weights = ModelConfig.model_weights):
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     model = torch.jit.load(model_path)
#     state = torch.load(model_weights, map_location=torch.device(device))
#     pretrained_dict = {key.replace("model.", "", 1): value for key, value in state['state_dict'].items()}
#     model.load_state_dict(pretrained_dict)
#     print(f'model_load {model_path}')
#     return model
#
#
# def model_generate(model_name = ModelConfig.model_name, model_path = ModelConfig.model_path):
#     model = model_create(model_name= model_name, pretrained=False, num_classes=2)
#     model_scripted = torch.jit.script(model)  # Export to TorchScript
#     model_scripted.save(model_path)  # Save
#     print(f'model_generate: {model_name} to {model_path}')




# def_model = create_model(model_name=ModelConfig.model_name, pretrained=True, num_classes=2)




