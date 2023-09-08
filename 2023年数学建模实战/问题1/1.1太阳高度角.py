import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams [ 'font.sans-serif'] = [ 'SimHei']
# Given parameters

phi = 39.4  # Latitude (degrees), north is positive
H = 3  # Altitude (km)
D_values = [307,337,1,32,63,93,124,154,185,215,246,276]  # Days since vernal equinox for each month
ST_values = [9, 10.5, 12, 13.5, 15]     # 给定时间

plt.figure(figsize=(8,6)) # 设置画布大小
plt.title("太阳的高度角角和各月21号的时间关系") # 设置标题
plt.xlabel("时间") # 设置横轴标签
plt.ylabel("高度角") # 设置纵轴标签
plt.grid(True) # 显示网格线
# Calculate solar declination angle delta for each month

delta_values = np.arcsin(np.sin(2 * np.pi * np.array(D_values) / 365) * np.sin(np.radians(23.45)))



# Calculate solar hour angle omega for each time point
omega_values = [np.pi/12 * (ST - 12) for ST in ST_values]

# Calculate solar altitude angle alpha_s and azimuth angle gamma_s for each month and time point
alpha_s_values = {}
for D, delta in zip(D_values, delta_values):
    month = D_values.index(D) + 1
    alpha_s_values[month] = []
    for omega in omega_values:
        alpha_s = np.arcsin(np.cos(delta) * np.cos(np.radians(phi)) * np.cos(omega) + np.sin(delta) * np.sin(np.radians(phi)))
        #A=((np.sin(delta) - np.sin(alpha_s) * np.sin(np.radians(phi))) / (np.cos(alpha_s) * np.cos(np.radians(phi))))
        #gamma_s = np.arccos(A)
        alpha_s_values[month].append(np.degrees(alpha_s))
        #gamma_s_values[month].append(np.degrees(gamma_s))

    plt.plot(ST_values, alpha_s_values[month], label=f"月份={month}")  # 绘制折线图，并设置图例
    plt.scatter(ST_values,alpha_s_values[month], s=50, c='red')
plt.xticks(ST_values)
plt.legend(loc='upper right', fontsize=6)  # 显示图例
plt.show()  # 显示图像
