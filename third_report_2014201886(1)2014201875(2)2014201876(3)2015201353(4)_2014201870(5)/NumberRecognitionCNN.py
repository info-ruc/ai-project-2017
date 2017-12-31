#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf
import cv2
import numpy as np

FLAGS = None


def deepnn(x):
  """deepnn builds the graph for a deep net for classifying digits.

  Args:
    x: an input tensor with the dimensions (N_examples, 784), where 784 is the
    number of pixels in a standard MNIST image.

  Returns:
    A tuple (y, keep_prob). y is a tensor of shape (N_examples, 10), with values
    equal to the logits of classifying the digit into one of 10 classes (the
    digits 0-9). keep_prob is a scalar placeholder for the probability of
    dropout.
  """
  # Reshape to use within a convolutional neural net.
  # Last dimension is for "features" - there is only one here, since images are
  # grayscale -- it would be 3 for an RGB image, 4 for RGBA, etc.
  x_image = tf.reshape(x, [-1, 28, 28, 1])

  # First convolutional layer - maps one grayscale image to 32 feature maps.
  W_conv1 = weight_variable([5, 5, 1, 32])
  b_conv1 = bias_variable([32])
  h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

  # Pooling layer - downsamples by 2X.
  h_pool1 = max_pool_2x2(h_conv1)

  # Second convolutional layer -- maps 32 feature maps to 64.
  W_conv2 = weight_variable([5, 5, 32, 64])
  b_conv2 = bias_variable([64])
  h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

  # Second pooling layer.
  h_pool2 = max_pool_2x2(h_conv2)

  # Fully connected layer 1 -- after 2 round of downsampling, our 28x28 image
  # is down to 7x7x64 feature maps -- maps this to 1024 features.
  W_fc1 = weight_variable([7 * 7 * 64, 1024])
  b_fc1 = bias_variable([1024])

  h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
  h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

  # Dropout - controls the complexity of the model, prevents co-adaptation of
  # features.
  keep_prob = tf.placeholder(tf.float32)
  h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

  # Map the 1024 features to 10 classes, one for each digit
  W_fc2 = weight_variable([1024, 10])
  b_fc2 = bias_variable([10])

  y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

  return y_conv, keep_prob


def conv2d(x, W):
  """conv2d returns a 2d convolution layer with full stride."""
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
  """max_pool_2x2 downsamples a feature map by 2X."""
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')


def weight_variable(shape):
  """weight_variable generates a weight variable of a given shape."""
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)


def bias_variable(shape):
  """bias_variable generates a bias variable of a given shape."""
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)


def main(_):
  print("import data")
  # Import data
  #mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

  # Create the model
  x = tf.placeholder(tf.float32, [None, 784])


  # Define loss and optimizer
  y_ = tf.placeholder(tf.float32, [None, 10])

  # Build the graph for the deep net
  y_conv, keep_prob = deepnn(x)


  # this is trainning step
  #cross_entropy = tf.reduce_mean(
  #   tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))

  #train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

  #correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))

  #accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

  # print("start train")
  
  
  saver = tf.train.Saver()
  
  # with tf.Session() as sess:
  #   sess.run(tf.global_variables_initializer())
  #   #batch = mnist.train.next_batch(1)
  #   #print(y_conv.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0}))
  #   for i in range(1000):
  #     batch = mnist.train.next_batch(50)
  #     if i % 100 == 0:
  #       train_accuracy = accuracy.eval(feed_dict={
  #           x: batch[0], y_: batch[1], keep_prob: 1.0})
  #       print('step %d, training accuracy %g' % (i, train_accuracy))
  #     train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

  #   saver.save(sess,"./model/me")
  #   print('test accuracy %g' % accuracy.eval(feed_dict={
  #       x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))
  
  with tf.Session() as sess:
    saver.restore(sess,"./model/me")

    cap=cv2.VideoCapture(1)
    while(1): 
      ret, frame = cap.read()
      cv2.imshow("capture", frame)   
    # img = cv2.imread("none.bmp")
      Grayimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      Grayimg = cv2.resize(Grayimg,(28,28))

      b = np.array(cv2.split(Grayimg)[0])
      b = b.reshape(1,-1)
 

      #saver.save(sess,"./model/me")
      a = y_conv.eval(feed_dict={x: b, keep_prob: 1.0})
      predict = np.argmax(a)
      print(a[:,predict])
      print(predict)


    
    
if __name__ == '__main__':
  print("main run")
  # parser = argparse.ArgumentParser()
  # parser.add_argument('--data_dir', type=str,
  #                     default='mnist_test_10000',
  #                     help='Directory for storing input data')
  # FLAGS, unparsed = parser.parse_known_args()
  # tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
  tf.app.run(main=main)




