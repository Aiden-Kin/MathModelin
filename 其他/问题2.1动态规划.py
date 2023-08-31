from scipy.integrate import odeint
import numpy as np
from scipy.optimize import minimize

# Given parameters
M = 60.0  # kg, mass of the buoy
ma = 30.0  # kg, added mass
m = 40.0  # kg, mass of the oscillator
cw = 1000.0  # N·s/m, hydrodynamic damping coefficient
F0 = 1000.0  # N, amplitude of wave excitation force
omega = 2.2143  # s^-1, frequency of wave excitation
g = 9.81  # m/s^2, acceleration due to gravity
k=80000

# Initial conditions
z0 = 0.0  # initial displacement of buoy
v0 = 0.0  # initial velocity of buoy
x0 = 0.0  # initial displacement of oscillator
u0 = 0.0  # initial velocity of oscillator
initial_conditions = [z0, v0, x0, u0]

# Time settings
T = 100  # total time
dt = 0.1  # time step
t = np.linspace(0, T, int(T / dt))  # time array


# Linear damping case
def linear_equations(y, t, c):
    z, v, x, u = y
    dzdt = v
    dvdt = (F0 * np.cos(omega * t) - cw * v - c * u - k * (z - x)) / (M + ma)
    dxdt = u
    dudt = (-c * u + k * (z - x)) / m
    return [dzdt, dvdt, dxdt, dudt]


def linear_objective(c):
    # Solve the ODEs
    sol = odeint(linear_equations, initial_conditions, t, args=(c,))

    # Extract the relative velocity u from the solution
    u = sol[:, 3]

    # Calculate the instantaneous power
    P = c * u ** 2

    # Calculate the negative average power (since we are using minimize)
    return -np.mean(P[-int(0.2 * len(P)):])  # Only considering the last 20% of the time for steady state


# Optimization for the linear damping case
linear_result = minimize(linear_objective, 50000, bounds=[(0, 100000)])
best_c_linear = linear_result.x[0]
max_avg_power_linear = -linear_result.fun

print(best_c_linear, max_avg_power_linear)
