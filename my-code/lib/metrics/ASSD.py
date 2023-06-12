import math
import torch
import torch.nn as nn
import numpy as np

import sys
sys.path.append(r"D:\Projects\Python\3D-tooth-segmentation\PMFS-Net：Polarized Multi-scale Feature Self-attention Network For CBCT Tooth Segmentation\my-code")
from lib.utils import *



class AverageSymmetricSurfaceDistance(object):
    def __init__(self, num_classes=33, c=6, sigmoid_normalization=False):
        """
        定义平均对称表面距离(ASSD)评价指标计算器
        Args:
            num_classes: 类别数
            c: 连通度
            sigmoid_normalization: 对网络输出采用sigmoid归一化方法，否则采用softmax
        """
        super(AverageSymmetricSurfaceDistance, self).__init__()
        # 初始化参数
        self.num_classes = num_classes
        self.c = c
        # 初始化sigmoid或者softmax归一化方法
        if sigmoid_normalization:
            self.normalization = nn.Sigmoid()
        else:
            self.normalization = nn.Softmax(dim=1)


    def __call__(self, input, target):
        """
        平均对称表面距离(ASSD)
        Args:
            input: 网络模型输出的预测图,(B, C, H, W, D)
            target: 标注图像,(B, H, W, D)

        Returns:
        """
        # 对预测图进行Sigmiod或者Sofmax归一化操作
        input = self.normalization(input)

        # 将预测图像进行分割
        seg = torch.argmax(input, dim=1)
        # 判断预测图和真是标签图的维度大小是否一致
        assert seg.shape == target.shape, "seg和target的维度大小不一致"
        # 转换seg和target数据类型为整型
        seg = seg.type(torch.uint8)
        target = target.type(torch.uint8)

        return compute_per_channel_assd(seg, target, self.num_classes, c=self.c)




if __name__ == '__main__':
    pred = torch.randn((4, 33, 32, 32, 16))
    gt = torch.randint(33, (4, 32, 32, 16))

    ASSD_metric = AverageSymmetricSurfaceDistance(c=6, num_classes=33)

    ASSD_per_channel = ASSD_metric(pred, gt)

    print(ASSD_per_channel)




















