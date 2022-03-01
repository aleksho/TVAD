import albumentations as A
from albumentations.pytorch import ToTensorV2

from ad_class_predict.config import ModelConfig

train_transform = A.Compose(
    [
    A.Resize(ModelConfig.img_size, ModelConfig.img_size),
    A.RandomBrightnessContrast(p=0.2, brightness_limit=(-0.2, 0.2), contrast_limit=(-0.2, 0.2)),
    A.HueSaturationValue(p=0.2, hue_shift_limit=0.2, sat_shift_limit=0.2, val_shift_limit=0.2),
    A.ShiftScaleRotate(p=0.2, shift_limit=0.2, scale_limit=0.2, rotate_limit=0),
    A.CoarseDropout(p=0.2),
    A.Transpose(p=0.5),
    A.HorizontalFlip(p=0.5),
    A.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
            ),
    ToTensorV2(),
    ]

)

pred_transform = A.Compose(
    [
    A.Resize(ModelConfig.img_size, ModelConfig.img_size),
    A.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
            ),
    ToTensorV2(),
    ]
)
