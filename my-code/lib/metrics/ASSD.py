import math
import torch
import torch.nn as nn
import numpy as np

import sys
sys.path.append(r"D:\Projects\Python\3D-tooth-segmentation\PMFS-Net：Polarized Multi-scale Feature Self-attention Network For CBCT Tooth Segmentation\my-code")
sys.path.append(r"/Users/yyk/Project/Python/PMFS-Net/my-code")
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


class AverageSymmetricSurfaceDistance_lib(object):
    def __init__(self, num_classes=33, sigmoid_normalization=False):
        """
        定义平均对称表面距离(ASSD)评价指标计算器
        Args:
            num_classes: 类别数
            sigmoid_normalization: 对网络输出采用sigmoid归一化方法，否则采用softmax
        """
        super(AverageSymmetricSurfaceDistance_lib, self).__init__()
        # 初始化参数
        self.num_classes = num_classes
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
        seg = seg.long()
        target = target.long()

        # 将分割图和标签图都进行one-hot处理
        seg = expand_as_one_hot(seg, self.num_classes)
        target = expand_as_one_hot(target, self.num_classes)

        # 转换seg和target数据类型为布尔型
        seg = seg.bool()
        target = target.bool()

        # 判断one-hot处理后标注图和分割图的维度是否都是5维
        assert seg.dim() == target.dim() == 5, "one-hot处理后标注图和分割图的维度不是都为5维！"
        # 判断one-hot处理后标注图和分割图的尺寸是否一致
        assert seg.size() == target.size(), "one-hot处理后分割图和标注图的尺寸不一致！"

        return compute_per_channel_assd_lib(seg, target, self.num_classes)



if __name__ == '__main__':
    pred = torch.randn((4, 33, 32, 32, 16))
    gt = torch.randint(33, (4, 32, 32, 16))

    # ASSD_metric = AverageSymmetricSurfaceDistance(num_classes=33, c=18, sigmoid_normalization=False)
    # t1 = time.time()
    # ASSD_per_channel = ASSD_metric(pred, gt)
    # t2 = time.time()
    # print("计算耗时不用库：{:.2f}秒".format(t2 - t1))
    # print(ASSD_per_channel)

    ASSD_metric = AverageSymmetricSurfaceDistance_lib(num_classes=33, sigmoid_normalization=False)
    t1 = time.time()
    ASSD_per_channel = ASSD_metric(pred, gt)
    t2 = time.time()
    print("计算耗时用库：{:.2f}秒".format(t2 - t1))
    print(ASSD_per_channel)




















