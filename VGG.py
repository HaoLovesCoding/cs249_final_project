import tflearn
from tflearn.data_preprocessing import ImagePreprocessing
import os


def vgg16(input, num_class):

    x = tflearn.conv_2d(input, 64, 3, activation='relu', scope='conv1_1')
    x = tflearn.conv_2d(x, 64, 3, activation='relu', scope='conv1_2')
    x = tflearn.max_pool_2d(x, 2, strides=2, name='maxpool1')

    x = tflearn.conv_2d(x, 128, 3, activation='relu', scope='conv2_1')
    x = tflearn.conv_2d(x, 128, 3, activation='relu', scope='conv2_2')
    x = tflearn.max_pool_2d(x, 2, strides=2, name='maxpool2')

    x = tflearn.conv_2d(x, 256, 3, activation='relu', scope='conv3_1')
    x = tflearn.conv_2d(x, 256, 3, activation='relu', scope='conv3_2')
    x = tflearn.conv_2d(x, 256, 3, activation='relu', scope='conv3_3')
    x = tflearn.max_pool_2d(x, 2, strides=2, name='maxpool3')

    x = tflearn.conv_2d(x, 512, 3, activation='relu', scope='conv4_1')
    x = tflearn.conv_2d(x, 512, 3, activation='relu', scope='conv4_2')
    x = tflearn.conv_2d(x, 512, 3, activation='relu', scope='conv4_3')
    x = tflearn.max_pool_2d(x, 2, strides=2, name='maxpool4')

    x = tflearn.conv_2d(x, 512, 3, activation='relu', scope='conv5_1')
    x = tflearn.conv_2d(x, 512, 3, activation='relu', scope='conv5_2')
    x = tflearn.conv_2d(x, 512, 3, activation='relu', scope='conv5_3')
    x = tflearn.max_pool_2d(x, 2, strides=2, name='maxpool5')

    x = tflearn.fully_connected(x, 4096, activation='relu', scope='fc6')
    x = tflearn.dropout(x, 0.5, name='dropout1')

    x = tflearn.fully_connected(x, 4096, activation='relu', scope='fc7')
    x = tflearn.dropout(x, 0.5, name='dropout2')

    x = tflearn.fully_connected(x, num_class, activation='softmax', scope='fc8',
                                restore=False)

    return x

dataset_file = r'/Users/watermelon/Desktop/Courses/CS249Sun/prj/data/small'
#dataset_file = '/home/ubuntu/balance'

#model_path = '/Users/watermelon/Desktop/Courses/CS249Sun/prj/model'
model_path = '/home/ubuntu/model'

from tflearn.data_utils import image_preloader
print("Loading images...")
X, Y = image_preloader(dataset_file, image_shape=(300, 300), mode='folder',categorical_labels=True, normalize=False,files_extension=['.jpg', '.png'], filter_channel=True)

num_classes = 3 # num of your dataset

# VGG preprocessing
img_prep = ImagePreprocessing()
img_prep.add_featurewise_zero_center(mean=[123.68, 116.779, 103.939],per_channel=True)
# VGG Network
x = tflearn.input_data(shape=[None, 300, 300, 3], name='input',data_preprocessing=img_prep)
softmax = vgg16(x, num_classes)
regression = tflearn.regression(softmax, optimizer='adam',loss='categorical_crossentropy',learning_rate=0.001, restore=False)

model = tflearn.DNN(regression, checkpoint_path='vgg-finetuning',max_checkpoints=3, tensorboard_verbose=2,tensorboard_dir="./logs")

#model_file = os.path.join(model_path, "vgg16.tflearn")
#model.load(model_file, weights_only=True)

# Start finetuning
model.fit(X, Y, n_epoch=1000, validation_set=0.1, shuffle=True,
          show_metric=True, batch_size=32, snapshot_epoch=False,
          snapshot_step=100, run_id='vgg-finetuning')

model.save('your-task-model-retrained-by-vgg')
