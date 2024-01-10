import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 初始化地形信息
mapRange = [100, 100, 100]  # 地图长、宽、高范围
N = 10  # 山峰个数
peaksInfo = []
for _ in range(N):
    peak = {}
    peak['center'] = [np.random.uniform(0.2, 1) * mapRange[0], np.random.uniform(0.2, 1) * mapRange[1]]
    peak['height'] = np.random.uniform(0.3, 1) * mapRange[2]
    peak['range'] = np.multiply(mapRange, 0.1) * np.random.uniform(0.3, 1)
    peaksInfo.append(peak)

# 计算山峰曲面值
peaksData = np.zeros((mapRange[0], mapRange[1]))
for x in range(mapRange[0]):
    for y in range(mapRange[1]):
        value = 0
        for peak in peaksInfo:
            h_i = peak['height']
            x_i, y_i = peak['center']
            x_si, y_si, _ = peak['range']  # 使用索引访问range列表
            value += h_i * np.exp(-((x - x_i) / x_si) ** 2 - ((y - y_i) / y_si) ** 2)
        peaksData[x, y] = value

# 构造曲面网格
x = np.tile(np.arange(1, mapRange[0] + 1), (mapRange[1], 1)).T
y = np.tile(np.arange(1, mapRange[1] + 1), (mapRange[0], 1))
peaksData = peaksData.flatten()

# 构造X/Y/Z网格数据
X, Y = np.meshgrid(np.linspace(1, mapRange[0], 100), np.linspace(1, mapRange[1], 100))
Z = np.reshape(peaksData, (mapRange[0], mapRange[1]))
Z = np.interp(Z, (Z.min(), Z.max()), (0, 1))

# 画山峰曲面
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='terrain')
plt.show()