# (C) 2017 Leaf AI

import os
import time
import random
import numpy
import tensorflow as tf
from PIL import Image

specieslist = os.listdir("output/images")
num_class = len(specieslist)

def list_all_training_images():
	images = []
	labels = numpy.zeros((1, num_class))

	i = 0
	for species in specieslist:
		imagelist = os.listdir("output/images/" + species)
		for image_file in imagelist:
			images.append("output/images/" + species + "/" + image_file)
			
			# append label
			label = numpy.zeros((1, num_class))
			label[0][i] = 1
			labels = numpy.append(labels, label, axis=0)

		i = i+1
	
	#delete first row of labels, since it's junk
	labels = numpy.delete(labels, 0, axis=0)
	return (images, labels)


(images, labels) = list_all_training_images()
zipped = list(zip(images, labels))
random.shuffle(zipped)
images[:], labels[:] = zip(*zipped)

print("Shuffled the training data. Number of classes: " + str(num_class) + ", number of images: " + str(len(images)))

so_far = 0 # number of images returned so far
def get_training_images(num=10):
	global so_far
	global images
	global labels
	start = so_far
	end = so_far + num
	so_far = end
	image_subset = images[start:end]
	image_bytes = numpy.zeros((num, 3*1024*1024))

	i = 0
	for image in image_subset:
		im = Image.open(image)
		image_bytes[i] = numpy.asarray(im).flatten() / 127.5 - 1 # feature scaling
		i = i+1

	return (image_bytes, labels[start:end])



time.sleep(5)

sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32, shape=[None, 1024*1024*3]) #1024x1024 images
y_ = tf.placeholder(tf.float32, shape=[None, num_class])

W = tf.Variable(tf.zeros([1024*1024*3,num_class]))
b = tf.Variable(tf.zeros([num_class]))

sess.run(tf.global_variables_initializer())

y = tf.matmul(x,W) + b
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)

def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial)

def conv2d(x, W):
	return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
	return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

W_conv1 = weight_variable([3, 3, 3, 8])
b_conv1 = bias_variable([8])

x_image = tf.reshape(x, [-1, 1024, 1024, 3])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)


W_conv2 = weight_variable([3, 3, 8, 16])
b_conv2 = bias_variable([16])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)


W_conv3 = weight_variable([3, 3, 16, 32])
b_conv3 = bias_variable([32])

h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3) + b_conv3)
h_pool3 = max_pool_2x2(h_conv3)


W_conv4 = weight_variable([3, 3, 32, 64])
b_conv4 = bias_variable([64])

h_conv4 = tf.nn.relu(conv2d(h_pool3, W_conv4) + b_conv4)
h_pool4 = max_pool_2x2(h_conv4)


W_conv5 = weight_variable([3, 3, 64, 128])
b_conv5 = bias_variable([128])

h_conv5 = tf.nn.relu(conv2d(h_pool4, W_conv5) + b_conv5)
h_pool5 = max_pool_2x2(h_conv5)


W_conv6 = weight_variable([3, 3, 128, 256])
b_conv6 = bias_variable([256])

h_conv6 = tf.nn.relu(conv2d(h_pool5, W_conv6) + b_conv6)
h_pool6 = max_pool_2x2(h_conv6)


W_conv7 = weight_variable([3, 3, 256, 512])
b_conv7 = bias_variable([512])

h_conv7 = tf.nn.relu(conv2d(h_pool6, W_conv7) + b_conv7)
h_pool7 = max_pool_2x2(h_conv7)


W_conv8 = weight_variable([3, 3, 512, 1024])
b_conv8 = bias_variable([1024])

h_conv8 = tf.nn.relu(conv2d(h_pool7, W_conv8) + b_conv8)
h_pool8 = max_pool_2x2(h_conv8)


W_conv9 = weight_variable([3, 3, 1024, 2048])
b_conv9 = bias_variable([2048])

h_conv9 = tf.nn.relu(conv2d(h_pool8, W_conv9) + b_conv9)
h_pool9 = max_pool_2x2(h_conv9)






W_fc1 = weight_variable([2 * 2 * 2048, 8192]) #8192 = middle layer size
b_fc1 = bias_variable([8192])

h_pool9_flat = tf.reshape(h_pool9, [-1, 2 * 2 * 2048])
h_fc1 = tf.nn.relu(tf.matmul(h_pool9_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)


W_fc2 = weight_variable([8192, num_class])
b_fc2 = bias_variable([num_class])

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2






cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.global_variables_initializer())
for i in range(2000):
	batch = get_training_images(10)
	if i%10 == 0:
		train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
		print("step %d, training accuracy %g"%(i, train_accuracy))
	train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

# (all_images, all_labels) = get_training_images(10)
# print("test accuracy %g"%accuracy.eval(feed_dict={x: all_images, y_: all_labels, keep_prob: 1.0}))

