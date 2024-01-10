import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 初始化地形信息
mapRange = [500, 500, 500]  # 地图长、宽、高范围

# 自定义山峰信息
peaksInfo = [
    {
        'center': [50, 50],  # 第一个山峰的中心位置 [x, y]
        'height': 80,  # 第一个山峰的高度
        'range': [20, 20, 50]  # 第一个山峰的范围 [x_range, y_range, z_range]
    },
    {
        'center': [20, 80],  # 第二个山峰的中心位置 [x, y]
        'height': 60,  # 第二个山峰的高度
        'range': [30, 30, 40]  # 第二个山峰的范围 [x_range, y_range, z_range]
    },
    {
        'center': [250, 2],  # 第三个山峰的中心位置 [x, y]
        'height': 70,  # 第三个山峰的高度
        'range': [25, 25, 60]  # 第三个山峰的范围 [x_range, y_range, z_range]
    }
]

# 计算山峰曲面值
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

# 构造曲面网格
x = np.tile(np.arange(1, mapRange[0] + 1), (mapRange[1], 1)).T
y = np.tile(np.arange(1, mapRange[1] + 1), (mapRange[0], 1))
peaksData = peaksData.flatten()

# 构造X/Y/Z网格数据，与前面定义一致
X, Y = np.meshgrid(np.linspace(1, mapRange[0], mapRange[0]), np.linspace(1, mapRange[1], mapRange[1]))
Z = np.reshape(peaksData, (mapRange[0], mapRange[1]))
Z = np.interp(Z, (Z.min(), Z.max()), (0, 1))

# 画山峰曲面
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='terrain')
plt.show()