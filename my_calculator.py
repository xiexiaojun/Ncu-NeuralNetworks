import random
import numpy as np
from random import shuffle


class Calculaor():
    def __init__(self, train_picture, test_picture):
        self.train_picture = train_picture
        self.test_picture = test_picture

    def initialize(self, study_scale, converger_condition, fileManager):
        self.study_scale = study_scale
        self.converger_condition = converger_condition
        self.w0 = random.uniform(-1, 1)
        self.w1 = random.uniform(-1, 1)
        self.w2 = random.uniform(-1, 1)
        self.train1 = fileManager.train1
        self.train2 = fileManager.train2
        self.data_merge()

    def data_merge(self):
        self.train_data = []
        for i in range(len(self.train1["results"])):
            tmp = []
            tmp.append(-1)
            tmp.append(self.train1["xs"][i])
            tmp.append(self.train1["ys"][i])
            tmp.append(self.train1["results"][i])
            self.train_data.append(tmp)
        for i in range(len(self.train2["results"])):
            tmp = []
            tmp.append(-1)
            tmp.append(self.train2["xs"][i])
            tmp.append(self.train2["ys"][i])
            tmp.append(self.train2["results"][i])
            self.train_data.append(tmp)
        shuffle(self.train_data)

    def calculate(self, i):
        now = i % len(self.train_data)
        tmp_w = np.array([self.w0, self.w1, self.w2])
        tmp_x = np.array(self.train_data[now][0:3])
        if np.dot(tmp_w, tmp_x) >= 0:
            tmp_result = 1
        else:
            tmp_result = 2

        if tmp_result != self.train_data[now][3]:
            if tmp_result == 1:
                tmp_w = tmp_w - np.dot(tmp_x, self.study_scale)
            elif (tmp_result == 2) and (self.train_data[now][3] == 0):
                pass
            else:
                tmp_w = tmp_w + np.dot(tmp_x, self.study_scale)

            self.w0 = tmp_w[0]
            self.w1 = tmp_w[1]
            self.w2 = tmp_w[2]

        self.transfer_data_train()
        self.transfer_data_test()

    def after_calculate(self):
        self.transfer_data_train()
        self.transfer_data_test()

    def transfer_data_train(self):
        self.train_picture.get_weight_interval(
            self.w0, self.w1, self.w2)

    def transfer_data_test(self):
        self.test_picture.get_weight_interval(
            self.w0, self.w1, self.w2)