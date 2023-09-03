import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.optimize import minimize
from scipy.integrate import odeint, simps
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
matplotlib.rcParams['axes.unicode_minus'] = False

# 已给定的参数和之前定义的函数略去...
# 已给定的参数
M = 4866.0  # 浮子质量（kg）
m = 2433.0  # 振子质量（kg）
m_a = 1165.992  # 附加质量（kg）
F_wave_amp = 4890.0  # 波浪激励力振幅 (N)
omega = 2.2143  # 波浪频率 (s^-1)
C_wave = 167.8395  # 垂荡兴波阻尼系数 (N·s/m)
rho = 1025  # 水的密度 (kg/m^3)
g = 9.8  # 重力加速度 (m/s^2)
A = np.pi  # 海平面的横截面积 (m^2)，假设为圆形
k = 80000
0
T = 2 * np.pi / omega  # 一个波浪周期的周期（s）
total_time = 40 * T  # 40个波浪周期的总模拟时间（s）
dt = 0.01  # 时间步长（s）
t_points = np.arange(0, total_time, dt)  # 时间点


# 修改后的ODE函数，接受数组参数 [C_d, n]
def modified_buoy_ode(Y, t, params):
    C_d, n = params
    x_buoy, v_buoy, x_mass, v_mass = Y

    # 计算力
    a = abs(v_buoy - v_mass) ** n
    F_PTO = k * (x_mass - x_buoy) + C_d * a * (v_mass - v_buoy)
    F_wave_damping = -C_wave * v_buoy
    F_restoring = -rho * g * A * x_buoy
    F_wave = F_wave_amp * np.cos(omega * t)

    # 浮子方程
    dx_buoy_dt = v_buoy
    dv_buoy_dt = (F_PTO + F_wave_damping + F_restoring + F_wave) / (M + m_a)

    # 振子方程
    dx_mass_dt = v_mass
    dv_mass_dt = -F_PTO / m

    return [dx_buoy_dt, dv_buoy_dt, dx_mass_dt, dv_mass_dt]


# 修改后的用于计算平均功率输出的函数
def modified_average_power(params):
    initial_conditions = [0, 0, 0, 0]
    sol = odeint(modified_buoy_ode, initial_conditions, t_points, args=(params,))
    v_t = sol[:, 1] - sol[:, 3]
    P_t = params[0] * np.abs(v_t) ** (params[1] + 1)
    last_10_cycles_time_points = int(10 * T / dt)
    avg_power = simps(P_t[-last_10_cycles_time_points:], dx=dt) / (10 * T)
    return avg_power  # 为了最大化，取负值




# 重新计算每一组 (Cd, n) 的平均功率
Cd_range_short = np.linspace(0, 100000, 10)  # 阻尼系数范围
n_range_short = np.linspace(0, 1, 10)  # 幂指数范围

# 初始化一个空的数组来存储计算的平均功率
avg_power_values_short = np.zeros((len(Cd_range_short), len(n_range_short)))

# 计算每一组 (Cd, n) 的平均功率
for i, Cd in enumerate(Cd_range_short):
    for j, n in enumerate(n_range_short):
        avg_power_values_short[i, j] = modified_average_power([Cd, n])  # 取负值转换为最大化问题

# 创建一个新的网格
Cd_values_short, n_values_short = np.meshgrid(Cd_range_short, n_range_short)

# 创建一个新的三维图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 调整视角
ax.view_init(elev=30, azim=120)

# 重新画出平面
surf = ax.plot_surface(Cd_values_short, n_values_short, avg_power_values_short.T, cmap='viridis')

# 添加标签和标题
ax.set_xlabel('阻尼系数 $C_d$')
ax.set_ylabel('幂指数 $n$')
ax.set_zlabel('平均功率 (W)')
ax.set_title('平均功率作为阻尼系数和幂指数的函数')

# 添加颜色条
fig.colorbar(surf)

# 显示图
plt.show()
