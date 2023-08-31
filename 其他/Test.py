import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#定义函数
def func(y, t):
    return np.array(y)


t = np.linspace(0, 10, 100)
tt = np.linspace(5, 15, 100)
result = odeint(func, y0=1, t=tt)
y_real = np.exp(t)
plt.plot(t, result[:, 0], label='odient', marker='*')
plt.plot(t, y_real, label='real')
plt.legend()
plt.show()