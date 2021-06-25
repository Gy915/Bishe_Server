from torch.utils.data import DataLoader,Dataset
import numpy as np
from torch import nn
import torch
import torch.nn.functional as F
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
class RegressionNet(nn.Module):
    def __init__(self, input_num, output_num):
        super(RegressionNet, self).__init__()
        self.hidden1 = nn.Linear(input_num, 10, bias=True)
        self.predict = nn.Linear(10, output_num)
    def forward(self, x):
        x = F.relu(self.hidden1(x))
        x = self.predict(x)
        return x



if __name__ == '__main__':

    df = pd.read_excel("./TrainData.xlsx")
    df = df.iloc[:,1:]
   # print(df)
    trainSetInput = df.iloc[:,0:6].values
    trainSetOutput = df.iloc[:,6].values.reshape(198,1)
    print(trainSetInput, trainSetOutput.shape)


    RegNet = RegressionNet(6, 1)
    cost = nn.MSELoss()
    optimizer = torch.optim.Adam(RegNet.parameters(), lr=0.01)
    max_epoch = 500
    for i in range(max_epoch):
        predict = RegNet(torch.FloatTensor(trainSetInput))
        l = cost(torch.FloatTensor(trainSetOutput), predict)
        optimizer.zero_grad()
        l.backward()
        optimizer.step()
        #print(predict.detach().numpy())
    predict = RegNet(torch.FloatTensor(trainSetInput)).detach().numpy()
    label = trainSetOutput
    print(label, predict)


