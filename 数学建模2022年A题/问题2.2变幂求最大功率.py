from scipy.optimize import minimize
from scipy.integrate import odeint, simps
import numpy as np

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

T = 2 * np.pi / omega  # 一个波浪周期的周期（s）
total_time = 40 * T  # 40个波浪周期的总模拟时间（s）
dt = 0.01  # 时间步长（s）
t_points = np.arange(0, total_time, dt)  # 时间点


# 修改后的ODE函数，接受数组参数 [C_d, n]
def modified_buoy_ode(Y, t, params):
    C_d, n = params
    x_buoy, v_buoy, x_mass, v_mass = Y

    # 计算力
    a = pow(abs(-v_buoy + v_mass), n)
    F_PTO = k * (-x_buoy + x_mass) + C_d * (-v_buoy + v_mass) * a
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


# 修改后的用于计算平均功率输出的函数
def modified_average_power(params):
    initial_conditions = [0, 0, 0, 0]
    sol = odeint(modified_buoy_ode, initial_conditions, t_points, args=(params,))
    v_t = sol[:, 1] - sol[:, 3]

    app = pow(abs(v_t), params[1])
    P_t = params[0] * np.abs(v_t) * app
    last_10_cycles_time_points = int(10 * T / dt)
    avg_power = simps(P_t[-last_10_cycles_time_points:], dx=dt) / (10 * T)
    return -avg_power  # 为了最大化，取负值

param = [100000,0.3975]
print(modified_average_power(param))

# 初始猜测值和约束条件
initial_guess = [1, 0.5]  # [C_d, n]
bounds = [(0, 100000), (0, 1)]  # C_d 在 [0, 100000] 内，n 在 [0, 1] 内

# 使用 scipy 的 minimize 函数进行优化
result = minimize(modified_average_power, initial_guess, bounds=bounds)

# 获取最优解
optimal_params = result.x
max_avg_power = -result.fun

print("最优阻尼系数:", optimal_params[0])
print("最优幂指数:", optimal_params[1])
print("最大平均功率输出:", max_avg_power)
