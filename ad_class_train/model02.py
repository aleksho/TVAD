import timm
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchmetrics
import pytorch_lightning as pl

import time

class TVAD_Net(pl.LightningModule):
    def __init__(self, model=None, lr=1e-4, batch_size=8):
        super().__init__()
        self.save_hyperparameters(ignore="model")
        self.model = model
        self.metric = torchmetrics.Accuracy()
        self.criterion = torch.nn.CrossEntropyLoss()

    def forward(self,x):
        out = self.model(x)
        return out

    def training_step(self, batch, batch_idx):
        x,y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat,y)
        acc = self.metric(y_hat,y)
        # time.sleep(.1)

        # log_metric = {'acc/train': loss, 'acc/train': acc}
        #
        # log_metric = {'train_loss': loss, 'train_acc': acc}
        # self.log_dict(log_metric, prog_bar=True,logger=True, )

        loss2, acc = self._shared_eval_step(batch, batch_idx)
        metrics = {"acc/train": acc, "loss/train": loss2}
        self.log_dict(metrics, prog_bar=True, logger=True)

        return loss


    # def validation_step(self, batch, batch_idx):
    #     self._shared_eval(batch, batch_idx, "val")


    def validation_step(self,batch,batch_idx):
        x,y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat,y)
        acc = self.metric(y_hat,y)
        log_metric = {'val_loss': loss, 'val_acc': acc}
        self.log_dict(log_metric, prog_bar=True, logger=False )


        loss, acc = self._shared_eval_step(batch, batch_idx)
        metrics = {"acc/val": acc, "loss/val": loss}
        self.log_dict(metrics, prog_bar=True,logger=True)

        return metrics

        # self.log("val_loss", loss,prog_bar=True,logger=False),

        # self.log("acc/val", acc, prog_bar=False,logger=True),
        # self.log("loss/val",loss,prog_bar=False,logger=True)


    def test_step(self, batch, batch_idx):
        loss, acc = self._shared_eval_step(batch, batch_idx)
        metrics = {"acc/test": acc, "loss/test": loss}
        self.log_dict(metrics, prog_bar=False,logger=True)
        return metrics

    # def test_step(self, batch, batch_idx):
    #     self._shared_eval(batch, batch_idx, "test")

    def _shared_eval_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss  = F.cross_entropy(y_hat, y)
        acc = self.metric(y_hat,y)
        return loss, acc

    def _shared_eval(self, batch, batch_idx, prefix):
        x, y = batch
        y_hat = self.model(x)
        loss = F.cross_entropy(y_hat, y)
        acc = torchmetrics.Accuracy(y_hat, y)

        self.log(f"loss/{prefix}", loss, prog_bar=True,logger=True),
        self.log(f"acc/{prefix}" , acc,  prog_bar=True,logger=True)
        # return loss


    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        x = batch
        y_hat = self.model(x)
        return torch.argmax(y_hat, dim=1)
        # return y_hat

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr = self.hparams.lr)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.2, patience=2, verbose=True, eps=1e-06)
        return dict(
            optimizer=optimizer,
            lr_scheduler= {
                "scheduler" : scheduler,
                "monitor"   : "val_loss", #metric_to_track" val_loss
                # "frequency" : "indicates how often the metric is updated"
                "name": 'ReduceLROnPlateau',
                # If "monitor" references validation metrics, then "frequency" should be set to a
                # multiple of "trainer.check_val_every_n_epoch".
                }
        )


class CustomModel_v2(nn.Module):
    def __init__(self, model_name='tf_efficientnet_b3_ns', pretrained=False,  num_classes = 2):
        super().__init__()
        self.model = timm.create_model(model_name, pretrained=pretrained, num_classes=num_classes)

    def forward(self, x):
        out = self.model(x)
        return out

def set_model_checkpoint(model_name):
    model_checkpoint = pl.callbacks.ModelCheckpoint(monitor="val_loss",
                                                    verbose=True,
                                                    filename="{epoch:02d}_{val_acc:.2f}",
                                                    save_top_k=3,
                                                    mode="min",
                                                    save_weights_only=True,
                                                    )
    lr_loger = pl.callbacks.LearningRateMonitor()
    earlyStopping = pl.callbacks.EarlyStopping(monitor="val_loss", mode="min", patience=3)
    progress = pl.callbacks.TQDMProgressBar(refresh_rate=20, process_position=2)
    # status   = pl.callbacks.DeviceStatsMonitor()
    # summs    = pl.callbacks.ModelSummary()

    logger_TB  = pl.loggers.TensorBoardLogger("tb_logs", name=model_name)
    logger_CSV = pl.loggers.CSVLogger("logs", name=model_name)

    logger = [logger_TB, logger_CSV]

    my_callbacks = [lr_loger,
                    model_checkpoint,
                    earlyStopping,
                    progress,
                    # status,
                    # summs,
                    # PrintTableMetricsCallback(),

                    ]
    # filename   = "{epoch:02d}-{val_acc:.2f}",
    # ModelConfig.model_label
    return my_callbacks, logger

# def model_create(model_name=ModelConfig.model_name, pretrained=ModelConfig.pretrained, num_classes = ModelConfig.num_classes):
#     model = timm.create_model(model_name, pretrained=pretrained, num_classes=num_classes)
#     print('model_create')
#     return model
#
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




