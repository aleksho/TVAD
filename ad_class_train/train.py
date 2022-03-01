import timm
import torch.nn as nn
import torch
import torch.nn.functional as F
import torchmetrics
import pytorch_lightning as pl
import time

class __AD_Net(pl.LightningModule):
    def __init__(self, model=None, lr=1e-4, batch_size=8):
        super().__init__()
        self.save_hyperparameters(ignore="model")
        self.model = model

        self.metric = torchmetrics.Accuracy()
        self.criterion = torch.nn.CrossEntropyLoss()


    def forward(self, x):
        out = self.model(x)
        return out

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        acc = self.metric(y_hat, y)

        # loss = self._shared_eval(batch, batch_idx, "train")
        # self.log("train_acc" ,acc,on_step=False ,on_epoch=True,prog_bar=True,logger=True),
        # self.log("train_loss",loss,on_step=False,on_epoch=True,prog_bar=True,logger=True)


        log_metric = {'train_loss': loss, 'train_acc': acc}
        self.log_dict(log_metric, prog_bar=True, logger=True, )


        return loss

    # def validation_step(self, batch, batch_idx):
    #     self._shared_eval(batch, batch_idx, "val")

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)

        loss = self.criterion(y_hat, y)
        acc = self.metric(y_hat, y)

        # acc = torchmetrics.Accuracy(y_hat,y)
        # logs metrics for each validation_step - [default:False]
        # the average across the epoch - [default:True]

        log_metric = {'val_loss': loss, 'val_acc': acc}
        self.log_dict(log_metric, prog_bar=True, logger=True)

    def test_step(self, batch, batch_idx):
        loss, acc = self._shared_eval_step(batch, batch_idx)
        metrics = {"test_acc": acc, "test_loss": loss}
        self.log_dict(metrics)
        return metrics

    # def test_step(self, batch, batch_idx):
    #     self._shared_eval(batch, batch_idx, "test")

    def _shared_eval(self, batch, batch_idx, prefix):
        x, y = batch
        y_hat = self.model(x)

        loss = self.criterion(y_hat, y)
        acc = torchmetrics.Accuracy(y_hat, y)

        self.log(f"{prefix}_loss", loss, prog_bar=True, logger=True),
        self.log(f"{prefix}_acc", acc, prog_bar=True, logger=True)
        # return loss

    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        x, y = batch
        y_hat = self.model(x)
        return torch.argmax(y_hat, dim=1)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.hparams.lr)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.2, patience=4,
                                                               verbose=True, eps=1e-06)
        return dict(
            optimizer=optimizer,
            lr_scheduler={
                "scheduler": scheduler,
                "monitor": "val_loss",  # metric_to_track" val_loss
                # "frequency" : "indicates how often the metric is updated"
                "name": 'ReduceLROnPlateau',
                # If "monitor" references validation metrics, then "frequency" should be set to a
                # multiple of "trainer.check_val_every_n_epoch".
            }
        )



