import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(12, 50)
        self.fc2 = nn.Linear(50, 100)
        self.fc3 = nn.Linear(100, 100)
        self.fc4 = nn.Linear(100, 50)
        self.fc5 = nn.Linear(50, 1)


    def forward(self, x):
       x = F.relu(self.fc1(x))
       x = F.relu(self.fc2(x))
       x = F.relu(self.fc3(x))
       x = F.relu(self.fc4(x))
       x = self.fc5(x)
       #return F.softmax(x, dim=0)
       return x