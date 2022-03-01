import timm
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchmetrics
# import pytorch_lightning as pl

from ad_class_predict.config import ModelConfig

class CustomModel(nn.Module):
    def __init__(self, model_name='tf_efficientnet_b3_ns', pretrained=False):
        super().__init__()
        self.model = timm.create_model(model_name, pretrained=pretrained)
        n_features = self.model.classifier.in_features
        self.model.global_pool = nn.Identity()
        self.model.classifier = nn.Identity()
        self.pooling = nn.AdaptiveAvgPool2d(1)
        self.classifier = nn.Linear(n_features, ModelConfig.num_classes)

    def forward(self, x):
        bs = x.size(0)
        features = self.model(x)
        pooled_features = self.pooling(features).view(bs, -1)
        output = self.classifier(pooled_features)
        return output






def_model = CustomModel(model_name=ModelConfig.model_name, pretrained=ModelConfig.pretrained)
