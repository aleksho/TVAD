import matplotlib.pyplot as plt
import torchvision
image_path ='/mnt/disk1/alexander_nn/work/dir_images/2022_3/57686_1728852_5602.jpg'
# image_path ='/mnt/disk1/alexander_nn/work/dir_images/2022_3/57685_1728822_5602.jpg'

# %%
data = plt.imread(image_path)

plt.imshow(data)
plt.show()
# %%
data2 = torchvision.io.read_image(image_path)



