from scipy.integrate import odeint
import numpy as np
import pandas as pd

def buoy_ode(Y, t, params):
    x_buoy, v_buoy, x_mass, v_mass = Y
    M, m, m_a, k, C_d, C_wave, rho, g, A, F_wave_amp, omega = params

    # Calculate forces

    F_PTO = k * (-x_buoy + x_mass) + C_d * (-v_buoy + v_mass)
    F_wave_damping = -C_wave * v_buoy   #兴波阻尼力
    F_restoring = -rho * g * A * x_buoy #净水恢复力
    F_wave = F_wave_amp * np.cos(omega * t) #波浪激励力

    # Equations for buoy
    dx_buoy_dt = v_buoy
    dv_buoy_dt = ( F_PTO + F_wave_damping + F_restoring + F_wave) / (M + m_a)

    # Equation for mass
    dx_mass_dt = v_mass
    dv_mass_dt = -F_PTO / m

    return [dx_buoy_dt, dv_buoy_dt, dx_mass_dt, dv_mass_dt]


# Parameters from addition3.xlsx and addition4.xlsx
M = 4866.0 # 浮子重量 (kg)
m = 2433.0  # 振子重量 (kg)
m_a = 1335.535 # 附加惯性力 (kg)
k = 80000  # 弹簧刚度 (N/m), not given in the problem
C_d = 10000  # 阻尼器阻尼系数 (N·s/m)
C_wave = 656.3616  # 兴波阻尼系数 (N·s/m)
rho = 1025  # Density of water (kg/m^3)
g = 9.8  # Acceleration due to gravity (m/s^2)
A = np.pi  # Cross-sectional area of the sea level (m^2), assumed
F_wave_amp = 6250  # 波浪激励力振幅 (N)
omega = 1.4005  # 波浪激励力 (s^-1)

# Initial conditions
x_buoy_init = 0  # Initial displacement of buoy (m)
v_buoy_init = 0  # Initial velocity of buoy (m/s)
x_mass_init = 0  # Initial displacement of mass (m)
v_mass_init = 0  # Initial velocity of mass (m/s)

# Time settings
T = 2 * np.pi / omega  # Period of one wave cycle (s)
total_time = 40 * T  # Total simulation time for 40 wave cycles (s)
dt = 0.001  # Time step (s)
time_points = np.arange(0, total_time, dt)  # Time array

# Solve ODE using odeint
initial_conditions = [x_buoy_init, v_buoy_init, x_mass_init, v_mass_init]
params = [M, m, m_a, k, C_d, C_wave, rho, g, A, F_wave_amp, omega]
solution = odeint(buoy_ode, initial_conditions, time_points, args=(params,))

# Extract results
x_buoy, v_buoy, x_mass, v_mass = solution.T

# Show some of the results as a sample
print(x_buoy[:10], v_buoy[:10], x_mass[:10], v_mass[:10])


# Create a DataFrame to hold the results
result_df = pd.DataFrame({
    '时间': time_points,
    '浮子 (m)': x_buoy,
    '浮子 (m/s)': v_buoy,
    '振子 (m)': x_mass,
    '振子 (m/s)': v_mass
})

# Extract values at specific time points: 10 s, 20 s, 40 s, 60 s, 100 s
specific_times = [10, 20, 40, 60, 100]
specific_rows = result_df[result_df['时间'].apply(lambda x: any(np.isclose(x, specific_times, atol=dt/2)))]

# Save the entire result to Excel
result_path = '问题1.1数据.xlsx'
result_df.to_excel(result_path, index=False)

# Show specific rows
print(specific_rows)
