from scipy.integrate import odeint
import numpy as np
from scipy.integrate import simps

# 给定参数
m = 4866.0  # 浮子质量（kg）
m_a = 1165.992  # 附加质量（kg）
F_0 = 4890.0  # 波浪激励力振幅（N）
omega = 2.2143  # 波浪频率（s^-1）

# 时间设置
T = 2 * np.pi / omega  # 一个波浪周期（s）
t_points = np.linspace(0, T, 500)  # 波浪周期内的时间点


# 浮子的动态方程
def buoy_dynamics(Y, t, c):
    x, v = Y  # 位移和速度
    dxdt = v
    dvdt = (F_0 * np.cos(omega * t) - c * v) / (m + m_a)
    return [dxdt, dvdt]


# 解决给定阻尼系数 c 的动态方程
def solve_buoy_dynamics(c):
    # 初始条件：x(0) = 0，v(0) = 0
    initial_conditions = [0, 0]

    # 解决动态方程
    sol = odeint(buoy_dynamics, initial_conditions, t_points, args=(c,))

    # 提取位移 x(t) 和速度 v(t)
    x_t = sol[:, 0]
    v_t = sol[:, 1]

    return x_t, v_t


# 为 c = 10000 测试动态方程求解器（仅用于演示，不是最优值）
x_t_demo, v_t_demo = solve_buoy_dynamics(10000)

x_t_demo[:10], v_t_demo[:10]  # 显示解的前10个数据点




# 计算平均输出功率的函数
def average_power_output(c):
    # 解决浮子的动态方程以获取速度 v(t)
    _, v_t = solve_buoy_dynamics(c)

    # 计算瞬时功率 P(t) = c * v(t)^2
    P_t = c * np.square(v_t)

    # 使用辛普森积分法计算平均输出功率
    avg_power = simps(P_t, t_points) / T

    return avg_power


# 为 c = 10000 测试平均输出功率函数（仅用于演示，不是最优值）
avg_power_demo = average_power_output(10000)

print(avg_power_demo)

from scipy.optimize import minimize_scalar

# Perform the optimization to maximize the average power output
result = minimize_scalar(lambda c: -average_power_output(c), bounds=(0, 100000), method='bounded')

# Extract the optimal damping coefficient and the maximum average power output
optimal_c = result.x
max_avg_power = -result.fun

print(optimal_c, max_avg_power)

