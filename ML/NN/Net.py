import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self, input_size, num_classes):
        super(Net, self).__init__()

        self.layer1 = nn.Sequential(
            nn.Linear(input_size, 50),
            nn.ReLU(),
            nn.Linear(50, 100),
            nn.ReLU(),
            nn.Linear(100, 300),
            nn.ReLU(),
            nn.Linear(300, 50),
            nn.ReLU(),
            nn.Linear(50, 10),
            nn.ReLU(),
        )
        self.head = nn.Linear(10, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.layer1(x)
        out = self.head(out)
        return out
   
