import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 初始化地图范围
mapRange = [750, 750, 750]  # 地图的长、宽、高范围

# 自定义山峰信息
peaksInfo = [
    {
        'center': [250, 250],  # 第一个山峰的中心位置 [x, y]
        'height': 80,  # 第一个山峰的高度
        'range': [20, 20, 50]  # 第一个山峰的范围 [x范围, y范围, z范围]
    },
    {
        'center': [20, 80],  # 第二个山峰的中心位置 [x, y]
        'height': 2700,  # 第二个山峰的高度
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

# 添加航迹的函数
def add_flight_path(ax, path_points, path_color='red'):
    """
    在地形图上添加航迹。
    :param ax: 3D坐标轴对象。
    :param path_points: 航迹点的列表，每个点为(x, y, z)格式。
    :param path_color: 航迹的颜色，默认为红色。
    """
    # 将路径点拆分为X, Y, Z坐标
    Xp, Yp, Zp = zip(*path_points)
    ax.plot(Xp, Yp, Zp, color=path_color, linewidth=2)

# 示例航迹坐标
sample_path = [
    (100, 100, 2700),  # 起点
    (200, 200, 1500), # 中间点
    (300, 300, 900)   # 终点
]

# 绘制带有高度层的山峰
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 使用实际高度绘制曲面
ax.plot_surface(X, Y, Z_scaled, cmap='terrain', alpha=0.3)

# 在每300米的高度处添加水平高度层
for i in range(1, num_layers + 1):
    current_layer_height = i * layer_height
    # 在当前高度层绘制一个水平平面
    ax.plot_surface(X, Y, np.full_like(X, current_layer_height), color='lightblue', alpha=0.5)

# 添加示例航迹
add_flight_path(ax, sample_path)

plt.show()

