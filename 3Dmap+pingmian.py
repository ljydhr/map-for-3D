import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 初始化地图范围
mapRange = [500, 500, 500]  # 地图的长、宽、高范围

# 自定义山峰信息
peaksInfo = [
    {
        'center': [250, 250],  # 第一个山峰的中心位置 [x, y]
        'height': 2700,  # 第一个山峰的高度
        'range': [20, 20, 50]  # 第一个山峰的范围 [x范围, y范围, z范围]
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

# 将Z值缩放为实际高度
Z_scaled = np.reshape(peaksData, (mapRange[0], mapRange[1])) * max_peak_height / peaksData.max()

# 设置每层的高度
layer_height = 300  # 每层的高度（以米为单位）

# 根据新的最大高度计算层数
num_layers = int(max_peak_height / layer_height)

# 创建曲面网格
X, Y = np.meshgrid(np.linspace(1, mapRange[0], mapRange[0]), np.linspace(1, mapRange[1], mapRange[1]))

# 选择一种颜色用于高度层，例如淡蓝色
layer_color = 'lightblue'

# 绘制带有高度层的山峰
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 使用实际高度绘制曲面，透明度降低以更好地显示高度层
ax.plot_surface(X, Y, Z_scaled, cmap='terrain', alpha=0.3)

# 在每300米的高度处添加水平高度层
for i in range(1, num_layers + 1):
    current_layer_height = i * layer_height
    # 在当前高度层绘制一个水平平面，使用淡蓝色
    ax.plot_surface(X, Y, np.full_like(X, current_layer_height), color=layer_color, alpha=0.5)

plt.show()
