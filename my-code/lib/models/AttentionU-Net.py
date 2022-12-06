# -*- encoding: utf-8 -*-
"""
@author   :   yykzjh    
@Contact  :   yykzhjh@163.com
@DateTime :   2022/12/2 21:14
@Version  :   1.0
@License  :   (C)Copyright 2022
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))

import torch
import torch.nn as nn

from lib.models.modules.UpConv import UpConv
from lib.models.modules.ConvBlock import ConvBlock
from lib.models.modules.GridAttentionGate3d import GridAttentionGate3d


class AttentionU_Net(nn.Module):
    def __init__(self, in_channels=1, out_channels=35):
        super(AttentionU_Net, self).__init__()

        self.Maxpool = nn.MaxPool3d(kernel_size=2, stride=2)

        self.Conv1 = ConvBlock(ch_in=in_channels, ch_out=64)
        self.Conv2 = ConvBlock(ch_in=64, ch_out=128)
        self.Conv3 = ConvBlock(ch_in=128, ch_out=256)
        self.Conv4 = ConvBlock(ch_in=256, ch_out=512)
        self.Conv5 = ConvBlock(ch_in=512, ch_out=1024)

        self.Up4 = UpConv(ch_in=1024, ch_out=512)
        self.Att4 = GridAttentionGate3d(F_l=512, F_g=1024, F_int=256)
        self.Up_conv4 = ConvBlock(ch_in=1024, ch_out=512)

        self.Up3 = UpConv(ch_in=512, ch_out=256)
        self.Att3 = GridAttentionGate3d(F_l=256, F_g=512, F_int=128)
        self.Up_conv3 = ConvBlock(ch_in=512, ch_out=256)

        self.Up2 = UpConv(ch_in=256, ch_out=128)
        self.Att2 = GridAttentionGate3d(F_l=128, F_g=256, F_int=64)
        self.Up_conv2 = ConvBlock(ch_in=256, ch_out=128)

        self.Up1 = UpConv(ch_in=128, ch_out=64)
        self.Att1 = GridAttentionGate3d(F_l=64, F_g=128, F_int=32)
        self.Up_conv1 = ConvBlock(ch_in=128, ch_out=64)

        self.Conv_1x1 = nn.Conv3d(64, out_channels, kernel_size=1, stride=1, padding=0)

    def forward(self, x):
        # encoding path
        x1 = self.Conv1(x)

        x2 = self.Maxpool(x1)
        x2 = self.Conv2(x2)

        x3 = self.Maxpool(x2)
        x3 = self.Conv3(x3)

        x4 = self.Maxpool(x3)
        x4 = self.Conv4(x4)

        x5 = self.Maxpool(x4)
        x5 = self.Conv5(x5)

        # decoding + concat path
        d4 = self.Up4(x5)
        x4 = self.Att4(x=x4, g=x5)[0]
        d4 = torch.cat((x4, d4), dim=1)
        d4 = self.Up_conv4(d4)

        d3 = self.Up3(d4)
        x3 = self.Att3(x=x3, g=d4)[0]
        d3 = torch.cat((x3, d3), dim=1)
        d3 = self.Up_conv3(d3)

        d2 = self.Up2(d3)
        x2 = self.Att2(x=x2, g=d3)[0]
        d2 = torch.cat((x2, d2), dim=1)
        d2 = self.Up_conv2(d2)

        d1 = self.Up1(d2)
        x1 = self.Att1(x=x1, g=d2)[0]
        d1 = torch.cat((x1, d1), dim=1)
        d1 = self.Up_conv1(d1)

        out = self.Conv_1x1(d1)

        return out



if __name__ == '__main__':
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    x = torch.randn((1, 1, 96, 160, 160)).to(device)

    model = AttentionU_Net(in_channels=1, out_channels=35).to(device)

    output = model(x)

    print(x.size())
    print(output.size())





