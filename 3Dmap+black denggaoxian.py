import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 初始化地图范围
mapRange = [500, 500, 500]  # 地图的长、宽、高范围

# 自定义山峰信息
peaksInfo = [
    {
        'center': [250, 250],  # 第一个山峰的中心位置 [x, y]
        'height': 2200,  # 第一个山峰的高度
        'range': [70, 50, 50]  # 第一个山峰的范围 [x范围, y范围, z范围]
    },
    {
        'center': [20, 80],  # 第二个山峰的中心位置 [x, y]
        'height': 60,  # 第二个山峰的高度
        'range': [30, 30, 40]  # 第二个山峰的范围 [x范围, y范围, z范围]
    },
    {
        'center': [400, 400],  # 第三个山峰的中心位置 [x, y]
        'height': 70,  # 第三个山峰的高度
        'range': [25, 25, 60]  # 第三个山峰的范围 [x范围, y范围, z范围]
    }
]

# 计算山峰曲面的值
peaksData = np.zeros((mapRange[0], mapRange[1]))
for x in range(mapRange[0]):
    for y in range(mapRange[1]):
        value = 0
        for peak in peaksInfo:
            h_i = peak['height']
            x_i, y_i = peak['center']
            x_si, y_si, _ = peak['range']
            value += h_i * np.exp(-((x - x_i) / x_si) ** 2 - ((y - y_i) / y_si) ** 2)
        peaksData[x, y] = value

# 计算最高峰的最大高度，用于缩放
max_peak_height = max([peak['height'] for peak in peaksInfo])

# 将Z值缩放为实际高度而非归一化处理
Z_scaled = np.reshape(peaksData, (mapRange[0], mapRange[1])) * max_peak_height / peaksData.max()

# 设置每层的高度
layer_height = 300  # 每层的高度（以米为单位）

# 根据新的最大高度计算层数
num_layers = int(max_peak_height / layer_height)

# 创建曲面网格
X, Y = np.meshgrid(np.linspace(1, mapRange[0], mapRange[0]), np.linspace(1, mapRange[1], mapRange[1]))

# 绘制带有高度层的山峰
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 使用实际高度绘制曲面
ax.plot_surface(X, Y, Z_scaled, cmap='terrain')

# 在每300米的高度处添加高度层
for i in range(1, num_layers + 1):
    current_layer_height = i * layer_height
    ax.contour(X, Y, Z_scaled, levels=[current_layer_height], colors='k', linestyles="solid")

plt.show()
