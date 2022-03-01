import os

MODELDIR = 'D:/0_Work/TVAD/architecture'
HOMEDIR  = 'D:/0_Work/TVAD/'
IMAGEDIR = f'{HOMEDIR}/images'

class SetModelConfig:
    image_dir = f"{IMAGEDIR}"
    model_dir = f"{MODELDIR}"
    home_dir = f"{HOMEDIR}"

    img_size = 300
    model_name = "tf_efficientnet_b3_ns"
    num_classes = 2
    batch_size = 8

    weight_name='tf_efficientnet_b3_ns_8_epoch=04_val_acc=0.96.ckpt'

    label = 'label'
    img_name = 'img_name'

    num_workers = 2

    pretrained = False
    lr = 1e-3
    epochs = 100
    seed = 42
    factor = 0.2  # ReduceLROnPlateau
    patience = 4  # ReduceLROnPlateau
    eps = 1e-6  # ReduceLROnPlateau

    list_model = [
        ['tf_efficientnet_b0_ns', 224],
        ['tf_efficientnet_b1_ns', 240],
        ['tf_efficientnet_b2_ns', 260],
        ['tf_efficientnet_b3_ns', 300],
        ['tf_efficientnet_b4_ns', 380],
        ['tf_efficientnet_b5_ns', 456],
        ['tf_efficientnet_b6_ns', 582],
        ['tf_efficientnet_b7_ns', 600],
    ]

    def __init__(self, **entries):
        self.__dict__.update(entries)
        self.set_dir()

    def set_dir(self):
        self.model_label = f"{self.model_name}_{self.img_size}"
        # self.model_dir = os.path.join(self.home_dir, self.model_label)

        self.model_path  = os.path.join(self.model_dir, f'{self.model_label}_model.pt')
        self.train_file  = f"{self.home_dir}/df_train.csv"
        self.val_file    = f"{self.home_dir}/df_val.csv"
        self.test_file   = f"{self.home_dir}/df_test.csv"
        self.pred_file   = f"{self.home_dir}/df_pred.csv"
        self.fold_file   = f"{self.home_dir}/train_folds.csv"

        self.input_file  = f"{self.image_dir}/df_input.csv"
        self.output_file = f"{self.image_dir}/df_output.csv"

        self.model_weights= f'{self.home_dir}/weights/{self.weight_name}'
        # os.makedirs(self.model_dir, exist_ok=True)

    def get_model(self, i):
        return self.list_model[i]

    def set_model(self, i):
        self.model_name = self.list_model[i][0]
        self.img_size = self.list_model[i][1]
        self.set_dir()
        print(self.model_label)

ModelConfig = SetModelConfig()