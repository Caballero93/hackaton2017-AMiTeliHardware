import tensorflow as tf
import numpy as np
from hackathon.utils.utils import ResultsMessage, PVMode

input_num = 9
fc1_num = 20
fc2_num = 30
fc3_num = 20
output_num = 5


def float_to_struct(data_msg, float_array):
    load_one = True if float_array[0] > 0.5 else False
    load_two = True if float_array[1] > 0.5 else False
    load_three = True if float_array[2] > 0.5 else False
    power_reference = float(float_array[3])
    pv_mode = PVMode.ON if float_array[4] > 0.5 else PVMode.OFF

    return ResultsMessage(data_msg, load_one, load_two, load_three, power_reference, pv_mode)


class TyphoonANN:

    def __init__(self):
        self.sess = tf.InteractiveSession()

        self.last_data = tf.Variable(tf.zeros([input_num]))

        self.input = tf.placeholder(tf.float32, [None, input_num])

        self.W1 = tf.Variable(tf.random_uniform([input_num, fc1_num], maxval=0.1))
        self.b1 = tf.Variable(tf.random_uniform([fc1_num], maxval=0.1))

        self.fc1 = tf.matmul(self.input, self.W1) + self.b1

        self.Wout = tf.Variable(tf.random_uniform([fc1_num, output_num], maxval=0.1))
        self.bout = tf.Variable(tf.random_uniform([output_num], maxval=0.1))

        self.output = tf.matmul(self.fc1, self.Wout) + self.bout

        self.cost_function = -self.output[0][0] - self.output[0][1] - self.output[0][2] \
            + self.last_data[0] - self.output[0][3] - self.output[0][4]

        self.train_step = tf.train.GradientDescentOptimizer(0.1).minimize(self.cost_function)

        tf.global_variables_initializer().run()

    def run_iteration(self, data):
        assign = self.last_data.assign(data)
        self.sess.run(assign)
        return self.sess.run(self.output, feed_dict={self.input: [data]})

    def ann_train(self, data):
        assign = self.last_data.assign(data)
        self.sess.run(assign)
        self.sess.run(self.train_step, feed_dict={self.input: [data]})

    def save_weights(self):
        np.save("weights/W1", self.sess.run(self.W1))
        np.save("weights/b1", self.sess.run(self.b1))
        np.save("weights/Wout", self.sess.run(self.Wout))
        np.save("weights/bout", self.sess.run(self.bout))

    def load_weights(self):
        assign = self.W1.assign(np.load("weights/W1.npy"))
        self.sess.run(assign)
        assign = self.Wout.assign(np.load("weights/Wout.npy"))
        self.sess.run(assign)
        assign = self.b1.assign(np.load("weights/b1.npy"))
        self.sess.run(assign)
        assign = self.bout.assign(np.load("weights/bout.npy"))
        self.sess.run(assign)




