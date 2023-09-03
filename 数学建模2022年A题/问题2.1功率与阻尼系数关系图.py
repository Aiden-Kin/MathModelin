from matplotlib import pyplot as plt
from scipy.optimize import minimize_scalar
from scipy.integrate import odeint, simps
import numpy as np

# 给定参数
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

T = 2 * np.pi / omega  # 一个波浪周期的周期（s）
total_time = 40 * T  # 40个波浪周期的总模拟时间（s）
dt = 0.1  # 时间步长（s）
t_points = np.arange(0, total_time, dt)  # 时间点

# Set the font properties for UTF-8 characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei is a commonly used font for Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # This is to display the minus sign properly


# 使用修改后的阻尼力方程来计算浮子和质量的动力学的函数
def modified_buoy_ode(Y, t, C_d):
    x_buoy, v_buoy, x_mass, v_mass = Y

    # 计算力
    F_PTO = k * (-x_buoy + x_mass) + C_d * (-v_buoy + v_mass)
    F_wave_damping = -C_wave * v_buoy  # 兴波阻尼力
    F_restoring = -rho * g * A * x_buoy  # 净水恢复力
    F_wave = F_wave_amp * np.cos(omega * t)  # 波浪激励力

    # Equations for buoy
    dx_buoy_dt = v_buoy
    dv_buoy_dt = (F_PTO + F_wave_damping + F_restoring + F_wave) / (M + m_a)

    # Equation for mass
    dx_mass_dt = v_mass
    dv_mass_dt = -F_PTO / m

    return [dx_buoy_dt, dv_buoy_dt, dx_mass_dt, dv_mass_dt]


# 使用修改后的阻尼力方程来计算恒定阻尼下的平均功率输出的函数
def modified_average_power_constant_damping(C_d):
    initial_conditions = [0, 0, 0, 0]
    sol = odeint(modified_buoy_ode, initial_conditions, t_points, args=(C_d,))
    v_t = sol[:, 1] - sol[:, 3]
    P_t = C_d * np.square(v_t)
    last_10_cycles_time_points = int(10 * T / dt)
    avg_power = simps(P_t[-last_10_cycles_time_points:], dx=dt) / (10 * T)
    return avg_power  # 为了最大化，取负值


results = []
c_values = np.arange(0, 100000, 300)
for c in c_values:
    avg_power = modified_average_power_constant_damping(c)
    results.append(avg_power)


plt.plot(c_values,results,label='平均功率',color='b')
plt.xlabel('阻尼系数 (N·s/m)')
plt.ylabel('平均功率 (W)')
plt.title('平均功率与阻尼系数的关系')
plt.legend()
plt.show()