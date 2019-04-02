# -*- coding: utf-8 -*-

from skimage import io, transform
import glob
import os
import tensorflow as tf
import numpy as np
import time

path = './sketches_png/png/'

# 将所有的图片resize成225*225
w = 225
h = 225
c = 1


# 读取图片
def read_img(path):
    cate=[path+'/'+x for x in os.listdir(path) if os.path.isdir(path+'/'+x)]
    imgs = []
    labels = []
    for idx, folder in enumerate(cate):
        for im in glob.glob(folder + '/*.png'):
            print('reading the images:%s' % (im))
            img = io.imread(im,as_grey=True)
            img = transform.resize(img, (w, h))
            imgs.append(img)
            labels.append(idx)
    return np.asarray(imgs, np.float32), np.asarray(labels, np.int32)


data, label = read_img(path)

# 打乱顺序
num_example = data.shape[0]
arr = np.arange(num_example)
np.random.shuffle(arr)
data = data[arr]
label = label[arr]

# 将所有数据分为训练集和验证集
ratio = 0.8
s = np.int(num_example * ratio)
x_train = data[:s]
y_train = label[:s]
x_val = data[s:]
y_val = label[s:]

# -----------------构建网络----------------------
# 占位符
x = tf.placeholder(tf.float32, shape=[None, w, h, c], name='x')
y_ = tf.placeholder(tf.int32, shape=[None, ], name='y_')

# 第一个卷积层（225——>71-->35)
conv1 = tf.layers.conv2d(
    inputs=x,
    filters=64,
    kernel_size=[15, 15],
    strides = 3,
    padding="VALID",
    activation=tf.nn.relu,
    kernel_initializer=tf.truncated_normal_initializer(stddev=0.01))
pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[3, 3], strides=2)

# 第二个卷积层(31-->15)
conv2 = tf.layers.conv2d(
    inputs=pool1,
    filters=128,
    kernel_size=[5, 5],
    padding="VALID",
    activation=tf.nn.relu,
    kernel_initializer=tf.truncated_normal_initializer(stddev=0.01))
pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[3, 3], strides=2)

# 第三个卷积层(15->15)
conv3 = tf.layers.conv2d(
    inputs=pool2,
    filters=256,
    kernel_size=[3, 3],
    padding="same",
    activation=tf.nn.relu,
    kernel_initializer=tf.truncated_normal_initializer(stddev=0.01))

# 第四个卷积层(15->15)
conv4 = tf.layers.conv2d(
    inputs=conv3,
    filters=256,
    kernel_size=[3, 3],
    padding="same",
    activation=tf.nn.relu,
    kernel_initializer=tf.truncated_normal_initializer(stddev=0.01))

# 第五个卷积层(15->15)
conv5 = tf.layers.conv2d(
    inputs=conv4,
    filters=256,
    kernel_size=[3, 3],
    padding="same",
    activation=tf.nn.relu,
    kernel_initializer=tf.truncated_normal_initializer(stddev=0.01))

pool5 = tf.layers.max_pooling2d(inputs=conv5, pool_size=[3, 3], strides=2)

re1 = tf.reshape(pool5, [-1, 7 * 7 * 256])

# 全连接层
dense1 = tf.layers.dense(inputs=re1,
                         units=512,
                         activation=tf.nn.relu,
                         kernel_initializer=tf.truncated_normal_initializer(stddev=0.01),
                         kernel_regularizer=tf.contrib.layers.l2_regularizer(0.003))
drop1 = tf.layers.dropout(inputs=dense1,rate=0.5)
dense2 = tf.layers.dense(inputs=drop1,
                         units=512,
                         activation=tf.nn.relu,
                         kernel_initializer=tf.truncated_normal_initializer(stddev=0.01),
                         kernel_regularizer=tf.contrib.layers.l2_regularizer(0.003))
drop2 = tf.layers.dropout(inputs=dense2,rate=0.5)

logits = tf.layers.dense(inputs=drop2,
                         units=250,
                         activation=None,
                         kernel_initializer=tf.truncated_normal_initializer(stddev=0.01),
                         kernel_regularizer=tf.contrib.layers.l2_regularizer(0.003))
# ---------------------------网络结束---------------------------

loss = tf.losses.sparse_softmax_cross_entropy(labels=y_, logits=logits)
train_op = tf.train.AdamOptimizer(learning_rate=0.01).minimize(loss)
correct_prediction = tf.equal(tf.cast(tf.argmax(logits, 1), tf.int32), y_)
acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


# 定义一个函数，按批次取数据
def minibatches(inputs=None, targets=None, batch_size=None, shuffle=False):
    assert len(inputs) == len(targets)
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)
    for start_idx in range(0, len(inputs) - batch_size + 1, batch_size):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batch_size]
        else:
            excerpt = slice(start_idx, start_idx + batch_size)
        yield inputs[excerpt], targets[excerpt]


# 训练和测试数据，可将n_epoch设置更大一些

n_epoch = 30
batch_size = 64
sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())
for epoch in range(n_epoch):
    print("   epoch: ", epoch + 1)
    start_time = time.time()
    # training
    train_loss, train_acc, n_batch = 0, 0, 0

    for x_train_a, y_train_a in minibatches(x_train, y_train, batch_size, shuffle=True):
        x_train_a = np.reshape(x_train_a, (batch_size, w, h, -1))
        _, err, ac = sess.run([train_op, loss, acc], feed_dict={x: x_train_a, y_: y_train_a})
        train_loss += err;
        train_acc += ac;
        n_batch += 1
    print("   train loss: %f" % (train_loss / n_batch))
    print("   train acc: %f" % (train_acc / n_batch))

    # validation
    val_loss, val_acc, n_batch = 0, 0, 0
    for x_val_a, y_val_a in minibatches(x_val, y_val, batch_size, shuffle=False):
        x_val_a = np.reshape(x_val_a, (batch_size, w, h, -1))
        err, ac = sess.run([loss, acc], feed_dict={x: x_val_a, y_: y_val_a})
        val_loss += err;
        val_acc += ac;
        n_batch += 1
    print("   validation loss: %f" % (val_loss / n_batch))
    print("   validation acc: %f" % (val_acc / n_batch))
    print("-----------------------------------------------------")
sess.close()